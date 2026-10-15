"""Hello world — one message to an existing agent with ``libraos.Client``.

No agent setup: this talks to an agent that already exists on your LibraOS
server (``default`` is present on a stock install).

Prerequisites::

    pip install libraos-sdk
    export LIBRAOS_BASE_URL=https://libraos.partner.com
    export LIBRAOS_API_KEY=msk_live_...
    export LIBRAOS_AGENT_ID=default  # optional

Run::

    python 01_basic_chat.py
"""

from __future__ import annotations

import asyncio
import os

from libraos import Client


async def main() -> None:
    base_url = os.environ.get("LIBRAOS_BASE_URL", "https://libraos.partner.com")
    api_key = os.environ["LIBRAOS_API_KEY"]
    agent_id = os.environ.get("LIBRAOS_AGENT_ID", "default")

    async with Client(base_url=base_url, api_key=api_key) as c:
        msg = await c.messages.create(
            agent_id,
            messages=[{"role": "user", "content": "Hello, LibraOS!"}],
            model="anthropic/claude-opus-4-7",
            max_tokens=256,
        )

    print(f"Message ID : {msg.id}")
    print(f"Model used : {msg.model}")
    print(f"Stop reason: {msg.stop_reason}")
    if msg.usage is not None:
        print(f"Tokens     : {msg.usage.input_tokens} in / {msg.usage.output_tokens} out")
    print()
    print(msg.text)


if __name__ == "__main__":
    asyncio.run(main())
