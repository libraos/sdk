"""Streaming context manager — SSE consumption."""

from __future__ import annotations

from typing import Any

import httpx
import pytest

from libraos import Client


def _sse_body(*events: tuple[str, str]) -> bytes:
    """Build a fake SSE response body from (event, data) tuples."""
    out = []
    for ev, data in events:
        out.append(f"event: {ev}\ndata: {data}\n\n")
    return "".join(out).encode()


@pytest.mark.asyncio
async def test_stream_yields_events() -> None:
    body = _sse_body(
        ("text", '{"type":"text","content":"hello"}'),
        ("text", '{"type":"text","content":" world"}'),
        ("done", '{"type":"done","status":"completed","message_id":"msg_1"}'),
    )

    def handler(req: httpx.Request) -> httpx.Response:
        assert req.method == "POST"
        assert req.url.path == "/v1/messages"
        return httpx.Response(
            200,
            headers={"Content-Type": "text/event-stream"},
            content=body,
        )

    transport = httpx.MockTransport(handler)
    async with Client("https://t.local", "k", transport=transport) as c:
        events = []
        async with c.messages.stream(
            agent_id="invoice-bot",
            messages=[{"role": "user", "content": "hi"}],
        ) as s:
            async for e in s:
                events.append(e)

    types = [e["data"]["type"] for e in events]
    assert types == ["text", "text", "done"]


def test_mode_a_submit_is_gone() -> None:
    """Mode A (answering custom tools over the stream) was removed; use webhooks."""
    from libraos.streaming import MessageStream

    assert not hasattr(MessageStream, "submit_tool_result")
