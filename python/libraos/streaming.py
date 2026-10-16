"""Streaming context manager for /v1/messages.

Custom tools are not answered over this stream: declare them with a
`callback` and serve them with :class:`libraos.callbacks.WebhookRouter`
(webhooks, "Mode B").

Implementation note: httpx's MockTransport is fully buffered — it doesn't
stream `aiter_lines()` chunk-by-chunk. For real network usage, the
underlying `client.stream()` opens a chunked response and yields lines
as they arrive. The same code path works for both.
"""

from __future__ import annotations

from typing import TYPE_CHECKING, Any, AsyncIterator

from libraos._sse import parse_lines

if TYPE_CHECKING:
    from libraos.client import Client


class MessageStream:
    """Async context manager exposing the SSE event stream.

    Use:
        async with c.messages.stream(agent_id, messages=...) as s:
            async for event in s:
                ...
    """

    def __init__(
        self,
        client: "Client",
        agent_id: str,
        body: dict[str, Any],
    ) -> None:
        self._client = client
        self._agent_id = agent_id
        self._body = body
        self._response_cm = None
        self._response = None

    async def __aenter__(self) -> "MessageStream":
        self._response_cm = self._client._http.stream(
            "POST",
            "/v1/messages",
            json=self._body,
        )
        self._response = await self._response_cm.__aenter__()
        if self._response.status_code >= 400:
            # Surface as typed error; consume body first so the connection
            # is released cleanly before raising.
            try:
                content = await self._response.aread()
                from libraos.errors import parse_error_response
                import json as _json
                try:
                    payload = _json.loads(content)
                except (_json.JSONDecodeError, ValueError):
                    payload = content.decode("utf-8", errors="replace")
                raise parse_error_response(self._response.status_code, payload)
            finally:
                await self._response_cm.__aexit__(None, None, None)
                self._response_cm = None
        return self

    async def __aexit__(self, *exc_info: Any) -> None:
        if self._response_cm is not None:
            await self._response_cm.__aexit__(*exc_info)
            self._response_cm = None

    def __aiter__(self) -> AsyncIterator[dict[str, Any]]:
        return self._iter_events()

    async def _iter_events(self) -> AsyncIterator[dict[str, Any]]:
        if self._response is None:
            raise RuntimeError("MessageStream used outside of `async with`")

        async def lines() -> AsyncIterator[str]:
            async for line in self._response.aiter_lines():
                yield line

        async for event in parse_lines(lines()):
            yield event


__all__ = ["MessageStream"]
