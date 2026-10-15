"""LibraAdk — control-plane + data-plane client.

``deploy`` writes the agent to ``/v1/agents``; ``run`` executes it on the
LibraOS managed runtime and streams events. v1 targets the durable jobs surface
(works today); the exact wire shapes are the documented mapping
(docs/design/agent-sdk-rfc.md §5) — confirm against the server before GA.
"""

from __future__ import annotations

import json
import os
from typing import Any, Callable, Iterator, Optional

import httpx

from .agent import Agent

# Value of the managed-agents beta header sent on /v1/agents (older servers
# require it; current ones accept and ignore it).
MANAGED_AGENTS_BETA = "managed-agents-2026-04-01"

RunEvent = dict[str, Any]


def _env(*keys: str) -> Optional[str]:
    for k in keys:
        v = os.environ.get(k)
        if v:
            return v
    return None


class LibraAdk:
    def __init__(self, base_url: Optional[str] = None, api_key: Optional[str] = None) -> None:
        base_url = base_url or _env("LIBRA_OS_URL")
        api_key = api_key or _env("LIBRA_OS_API_KEY")
        if not base_url:
            raise ValueError("LibraAdk: base_url (or $LIBRA_OS_URL) is required")
        if not api_key:
            raise ValueError("LibraAdk: api_key (or $LIBRA_OS_API_KEY) is required")
        self.base_url = base_url.rstrip("/")
        self.api_key = api_key

    def _headers(self) -> dict[str, str]:
        return {"authorization": f"Bearer {self.api_key}", "content-type": "application/json"}

    def _agent_headers(self) -> dict[str, str]:
        # Older servers require the managed-agents beta header on /v1/agents (426
        # without it); current ones accept and ignore it.
        return {**self._headers(), "anthropic-beta": MANAGED_AGENTS_BETA}

    def deploy(self, agent: Agent) -> dict[str, Any]:
        """Create or update the agent. Updates with ``PUT /v1/agents/:name``; a new
        agent (404) is created with ``POST /v1/agents``. Idempotent."""
        body = agent.to_managed_agent_body()
        with httpx.Client() as c:
            r = c.put(
                f"{self.base_url}/v1/agents/{agent.name}",
                headers=self._agent_headers(),
                json=body,
            )
            if r.status_code == 404:
                r = c.post(
                    f"{self.base_url}/v1/agents",
                    headers=self._agent_headers(),
                    json={"id": agent.name, **body},
                )
            if r.status_code >= 400:
                raise RuntimeError(f"deploy {agent.name}: {r.status_code} {r.text}")
            data = r.json() if r.content else {}
            out: dict[str, Any] = {"id": data.get("id", agent.name)}
            if "etag" in data:
                out["etag"] = data["etag"]
            return out

    def run(
        self,
        agent_name: str,
        message: str,
        on_event: Optional[Callable[[RunEvent], None]] = None,
    ) -> list[RunEvent]:
        """Run an agent on the LibraOS stack and stream its events.

        Targets the durable jobs surface (``POST /agents/v1/:key/jobs`` +
        ``…/jobs/:id/stream``). Once the P0 seam lands (libraos/libraos#840/#841)
        this can move to the session surface for full Managed-Agents compat.
        """
        events: list[RunEvent] = []
        with httpx.Client(timeout=None) as c:
            r = c.post(
                # The path names the agent; the API key goes in the Authorization header.
                f"{self.base_url}/agents/v1/{agent_name}/jobs",
                headers=self._headers(),
                json={"message": message},
            )
            if r.status_code >= 400:
                raise RuntimeError(f"run {agent_name}: submit {r.status_code} {r.text}")
            job_id = r.json().get("job_id")
            if not job_id:
                raise RuntimeError(f"run {agent_name}: server did not return a job_id")
            with c.stream(
                "GET",
                f"{self.base_url}/agents/v1/{agent_name}/jobs/{job_id}/stream",
                headers={"authorization": f"Bearer {self.api_key}", "accept": "text/event-stream"},
            ) as s:
                for ev in _iter_sse(s):
                    events.append(ev)
                    if on_event:
                        on_event(ev)
        return events


def _iter_sse(resp: "httpx.Response") -> Iterator[RunEvent]:
    buf = ""
    for chunk in resp.iter_text():
        buf += chunk
        while "\n\n" in buf:
            frame, buf = buf.split("\n\n", 1)
            ev = _frame_to_event(frame)
            if ev is not None:
                yield ev


def _frame_to_event(frame: str) -> Optional[RunEvent]:
    etype = "message"
    data: list[str] = []
    for line in frame.split("\n"):
        if line.startswith("event:"):
            etype = line[6:].strip()
        elif line.startswith("data:"):
            data.append(line[5:].strip())
    if not data:
        return None
    raw = "\n".join(data)
    try:
        parsed = json.loads(raw)
    except json.JSONDecodeError:
        return {"type": etype, "data": raw}
    if isinstance(parsed, dict):
        parsed.setdefault("type", etype)
        return parsed
    return {"type": etype, "data": parsed}
