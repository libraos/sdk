"""Streaming messages — minimum-lines example.

Demonstrates ``c.messages.stream(...)`` for cases that don't need custom-tool
callbacks. Just open the stream, iterate events, print text deltas as they
arrive — useful for chat UIs and any partner that wants tokens-on-the-wire
latency rather than waiting for the full reply.

Custom tools are not answered over the stream: serve them from a webhook
(``05_custom_tool_webhook.py``).

Prerequisites::

    pip install libraos-sdk
    export LIBRA_OS_URL=https://libraos.your-company.example
    export LIBRA_OS_API_KEY=msk_live_...

Run::

    python 09_streaming_messages.py
"""

from __future__ import annotations

import asyncio
import os

from libraos import Client


async def main() -> None:
    base_url = os.environ.get("LIBRA_OS_URL", "https://libraos.your-company.example")
    api_key = os.environ["LIBRA_OS_API_KEY"]
    agent_id = os.environ.get("LIBRA_OS_AGENT_ID", "default-assistant")

    async with Client(base_url=base_url, api_key=api_key) as c:
        async with c.messages.stream(
            agent_id=agent_id,
            messages=[{"role": "user", "content": "Tell me a 3-sentence story about an octopus."}],
        ) as s:
            async for event in s:
                kind = event.get("type")
                if kind == "text_delta":
                    print(event.get("content", ""), end="", flush=True)
                elif kind == "done":
                    print()  # newline after the streamed text
                    break


if __name__ == "__main__":
    asyncio.run(main())
