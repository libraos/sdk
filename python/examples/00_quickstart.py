"""Quickstart — fastest path from zero to a digital agent answering you.

Three SDK calls: create an employee (it owns agents and their model routing),
create an agent bound to it, and send it a message.

There is no separate session or environment object:
- Sessions are implicit. LibraOS scopes per-user memory automatically — pass
  ``X-End-User`` on the request and you get isolation equivalent to a session.
- Environment is the LibraOS server itself. Need a per-tenant filesystem? Add
  ``filesystem.enabled: true`` to the agent's frontmatter — six FS tools auto-
  register. No container plumbing on the partner side.

Total surface to go from nothing to a working digital agent: 3 SDK calls.

Prerequisites::

    pip install libraos-sdk
    export LIBRAOS_BASE_URL=https://libraos.your-company.example
    export LIBRAOS_API_KEY=msk_live_...

Run::

    python 00_quickstart.py
"""

from __future__ import annotations

import asyncio
import os

from libraos import Client


async def main() -> None:
    base_url = os.environ.get("LIBRAOS_BASE_URL", "https://libraos.your-company.example")
    api_key = os.environ["LIBRAOS_API_KEY"]

    async with Client(base_url=base_url, api_key=api_key) as c:
        # 1. Create the employee — the owner of one or more agents, and of
        #    their model routing.
        await c.employees.create(
            id="my-first-employee",
            display_name="My First Employee",
            model_config={
                "answer": {
                    "primary": "anthropic/claude-opus-4-7",
                    "fallback": ["gemini/gemini-2.5-flash"],
                }
            },
        )

        # 2. Create the agent — the runnable behavior bound to that employee.
        #    "type" tells the registry what loop to run (skill = single-call,
        #    persona = multi-turn, etc.).
        await c.agents.create(
            id="my-first-agent",
            type="skill",
            owner_employee="my-first-employee",
            instructions="You are a helpful assistant. Answer concisely.",
        )

        # 3. Send the first message. No session ID needed — observational memory is keyed on the
        #    (API key, end_user, agent) triple automatically. Pass the
        #    ``X-End-User`` header to scope memory per end-user; omit it for
        #    a single shared scope (fine for evaluation).
        resp = await c.messages.create(
            agent_id="my-first-agent",
            messages=[{"role": "user", "content": "What are you good at?"}],
            metadata={"agent_id": "my-first-agent"},
        )
        print(resp)

        # Cleanup (optional). Production code keeps these objects around.
        await c.agents.delete("my-first-agent")
        await c.employees.delete("my-first-employee")


if __name__ == "__main__":
    asyncio.run(main())
