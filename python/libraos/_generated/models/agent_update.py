from __future__ import annotations

from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, TypeVar, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..models.agent_type import AgentType
from ..models.agent_update_egress_guard import AgentUpdateEgressGuard
from ..models.agent_update_on_ambiguous_entity import AgentUpdateOnAmbiguousEntity
from ..models.agent_update_tool_scope import AgentUpdateToolScope
from ..models.agent_update_visibility import AgentUpdateVisibility
from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.agent_guardrails import AgentGuardrails
    from ..models.agent_thinking import AgentThinking
    from ..models.agent_triage import AgentTriage
    from ..models.agent_update_filesystem import AgentUpdateFilesystem
    from ..models.output_type_contract import OutputTypeContract


T = TypeVar("T", bound="AgentUpdate")


@_attrs_define
class AgentUpdate:
    """Partial update; only the fields supplied are changed.

    Attributes:
        name (str | Unset):
        model (str | Unset):
        system (str | Unset):
        tools (list[str] | Unset):
        owner (str | Unset):
        visibility (AgentUpdateVisibility | Unset):
        filesystem (AgentUpdateFilesystem | Unset):
        agent_type (AgentType | Unset): Whether this agent dispatches to other skill agents (persona) or
            executes one skill directly (skill). Maps to nova-os internals;
            partners only see the discriminator.
        brain (bool | Unset):
        capabilities (list[str] | Unset):
        max_turns (int | Unset):
        output_type (OutputTypeContract | Unset): Structured-output contract for agent replies. When set, Nova OS
            validates every assistant reply against `schema` before return.
            Server-side since v0.1.4.
        knowledge_bindings (list[str] | Unset):
        guardrails (AgentGuardrails | Unset): Per-agent opt-outs for the inbound guardrail chain. Each value is
            `enabled`, `disabled` or empty (inherit). On PUT/PATCH an omitted key
            keeps its value, a `null` key clears that override, and a top-level
            `guardrails: null` clears every override.
        thinking (AgentThinking | Unset): Native model reasoning on the agent's answer-tier call only (never the
            planner, triage or skill sub-tasks). `off` (the default) sends no
            reasoning parameter, so a model that reasons by default keeps
            reasoning; `none` asks the model not to reason. Per-call
            `metadata.thinking` wins. On PUT/PATCH send `{}` (or `effort: ""`) to
            clear; `null` keeps the current value.
        tool_choice (str | Unset): Forces (or forbids) a tool call on the first model call of the
            agent loop: `auto` (default), `none`, `required`, or a tool name.
            Per-call `metadata.tool_choice` wins. A named tool the request does
            not carry is dropped with a server-side warning.
        direct_tools (list[str] | Unset): Persona only. Tools offered on the persona's direct (non-planner)
            answer path. Names are validated against the live tool registry.
            Together with `tools`, this is the persona's declared tool scope;
            declaring neither keeps the whole catalog.
        tool_scope (AgentUpdateToolScope | Unset): `none` declares an agent that needs no catalog tools. Rejected
            (400) together with a non-empty `tools` or `direct_tools`.
        triage (AgentTriage | Unset): Persona planner routing pin. `triage` keeps the per-turn
            regex/LLM triage cascade, `always` runs the planner every turn,
            `never` skips it. Empty clears the pin (inherit the server default).
            Per-call `metadata.brain` still wins.
        turn_budget_tokens (int | Unset): Per-agent token budget for each model call of the agent's turn
            (overrides the server-wide turn budget). `0` means unset. When
            the agent is the outermost agent of a turn, its value also governs
            the skill agents it dispatches.
        agent_skills (list[str] | Unset): Agent Skills attached to this agent, as `name` (latest published
            catalog version) or `name@N` (pinned version). No duplicate names.
            Every entry must resolve for the caller's organization at write
            time (a published `/v1/skills` version, or for unpinned names a
            server-side skills folder); otherwise 400 with `field:
            agent_skills`.
        on_ambiguous_entity (AgentUpdateOnAmbiguousEntity | Unset): What a persona does when the documents its answer
            relies on span
            several sources the question does not choose between: `state`
            names the document the answer is based on, `ask` returns a
            clarifying question instead of an answer, `off` does nothing.
            Per-call `metadata.on_ambiguous_entity` wins; empty inherits the
            server default.
        egress_guard (AgentUpdateEgressGuard | Unset): Outbound search-query guard for this agent's turns. Guards only
            tighten: the server-wide, agent and per-call settings are combined,
            and `off` never removes a guard set elsewhere.
        clear_triage (bool | Unset): When true, clears the agent's `triage` pin (same as `triage: null`).
    """

    name: str | Unset = UNSET
    model: str | Unset = UNSET
    system: str | Unset = UNSET
    tools: list[str] | Unset = UNSET
    owner: str | Unset = UNSET
    visibility: AgentUpdateVisibility | Unset = UNSET
    filesystem: AgentUpdateFilesystem | Unset = UNSET
    agent_type: AgentType | Unset = UNSET
    brain: bool | Unset = UNSET
    capabilities: list[str] | Unset = UNSET
    max_turns: int | Unset = UNSET
    output_type: OutputTypeContract | Unset = UNSET
    knowledge_bindings: list[str] | Unset = UNSET
    guardrails: AgentGuardrails | Unset = UNSET
    thinking: AgentThinking | Unset = UNSET
    tool_choice: str | Unset = UNSET
    direct_tools: list[str] | Unset = UNSET
    tool_scope: AgentUpdateToolScope | Unset = UNSET
    triage: AgentTriage | Unset = UNSET
    turn_budget_tokens: int | Unset = UNSET
    agent_skills: list[str] | Unset = UNSET
    on_ambiguous_entity: AgentUpdateOnAmbiguousEntity | Unset = UNSET
    egress_guard: AgentUpdateEgressGuard | Unset = UNSET
    clear_triage: bool | Unset = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        name = self.name

        model = self.model

        system = self.system

        tools: list[str] | Unset = UNSET
        if not isinstance(self.tools, Unset):
            tools = self.tools

        owner = self.owner

        visibility: str | Unset = UNSET
        if not isinstance(self.visibility, Unset):
            visibility = self.visibility.value

        filesystem: dict[str, Any] | Unset = UNSET
        if not isinstance(self.filesystem, Unset):
            filesystem = self.filesystem.to_dict()

        agent_type: str | Unset = UNSET
        if not isinstance(self.agent_type, Unset):
            agent_type = self.agent_type.value

        brain = self.brain

        capabilities: list[str] | Unset = UNSET
        if not isinstance(self.capabilities, Unset):
            capabilities = self.capabilities

        max_turns = self.max_turns

        output_type: dict[str, Any] | Unset = UNSET
        if not isinstance(self.output_type, Unset):
            output_type = self.output_type.to_dict()

        knowledge_bindings: list[str] | Unset = UNSET
        if not isinstance(self.knowledge_bindings, Unset):
            knowledge_bindings = self.knowledge_bindings

        guardrails: dict[str, Any] | Unset = UNSET
        if not isinstance(self.guardrails, Unset):
            guardrails = self.guardrails.to_dict()

        thinking: dict[str, Any] | Unset = UNSET
        if not isinstance(self.thinking, Unset):
            thinking = self.thinking.to_dict()

        tool_choice = self.tool_choice

        direct_tools: list[str] | Unset = UNSET
        if not isinstance(self.direct_tools, Unset):
            direct_tools = self.direct_tools

        tool_scope: str | Unset = UNSET
        if not isinstance(self.tool_scope, Unset):
            tool_scope = self.tool_scope.value

        triage: dict[str, Any] | Unset = UNSET
        if not isinstance(self.triage, Unset):
            triage = self.triage.to_dict()

        turn_budget_tokens = self.turn_budget_tokens

        agent_skills: list[str] | Unset = UNSET
        if not isinstance(self.agent_skills, Unset):
            agent_skills = self.agent_skills

        on_ambiguous_entity: str | Unset = UNSET
        if not isinstance(self.on_ambiguous_entity, Unset):
            on_ambiguous_entity = self.on_ambiguous_entity.value

        egress_guard: str | Unset = UNSET
        if not isinstance(self.egress_guard, Unset):
            egress_guard = self.egress_guard.value

        clear_triage = self.clear_triage

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if name is not UNSET:
            field_dict["name"] = name
        if model is not UNSET:
            field_dict["model"] = model
        if system is not UNSET:
            field_dict["system"] = system
        if tools is not UNSET:
            field_dict["tools"] = tools
        if owner is not UNSET:
            field_dict["owner"] = owner
        if visibility is not UNSET:
            field_dict["visibility"] = visibility
        if filesystem is not UNSET:
            field_dict["filesystem"] = filesystem
        if agent_type is not UNSET:
            field_dict["agent_type"] = agent_type
        if brain is not UNSET:
            field_dict["brain"] = brain
        if capabilities is not UNSET:
            field_dict["capabilities"] = capabilities
        if max_turns is not UNSET:
            field_dict["max_turns"] = max_turns
        if output_type is not UNSET:
            field_dict["output_type"] = output_type
        if knowledge_bindings is not UNSET:
            field_dict["knowledge_bindings"] = knowledge_bindings
        if guardrails is not UNSET:
            field_dict["guardrails"] = guardrails
        if thinking is not UNSET:
            field_dict["thinking"] = thinking
        if tool_choice is not UNSET:
            field_dict["tool_choice"] = tool_choice
        if direct_tools is not UNSET:
            field_dict["direct_tools"] = direct_tools
        if tool_scope is not UNSET:
            field_dict["tool_scope"] = tool_scope
        if triage is not UNSET:
            field_dict["triage"] = triage
        if turn_budget_tokens is not UNSET:
            field_dict["turn_budget_tokens"] = turn_budget_tokens
        if agent_skills is not UNSET:
            field_dict["agent_skills"] = agent_skills
        if on_ambiguous_entity is not UNSET:
            field_dict["on_ambiguous_entity"] = on_ambiguous_entity
        if egress_guard is not UNSET:
            field_dict["egress_guard"] = egress_guard
        if clear_triage is not UNSET:
            field_dict["clear_triage"] = clear_triage

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.agent_guardrails import AgentGuardrails
        from ..models.agent_thinking import AgentThinking
        from ..models.agent_triage import AgentTriage
        from ..models.agent_update_filesystem import AgentUpdateFilesystem
        from ..models.output_type_contract import OutputTypeContract

        d = dict(src_dict)
        name = d.pop("name", UNSET)

        model = d.pop("model", UNSET)

        system = d.pop("system", UNSET)

        tools = cast(list[str], d.pop("tools", UNSET))

        owner = d.pop("owner", UNSET)

        _visibility = d.pop("visibility", UNSET)
        visibility: AgentUpdateVisibility | Unset
        if isinstance(_visibility, Unset):
            visibility = UNSET
        else:
            visibility = AgentUpdateVisibility(_visibility)

        _filesystem = d.pop("filesystem", UNSET)
        filesystem: AgentUpdateFilesystem | Unset
        if isinstance(_filesystem, Unset):
            filesystem = UNSET
        else:
            filesystem = AgentUpdateFilesystem.from_dict(_filesystem)

        _agent_type = d.pop("agent_type", UNSET)
        agent_type: AgentType | Unset
        if isinstance(_agent_type, Unset):
            agent_type = UNSET
        else:
            agent_type = AgentType(_agent_type)

        brain = d.pop("brain", UNSET)

        capabilities = cast(list[str], d.pop("capabilities", UNSET))

        max_turns = d.pop("max_turns", UNSET)

        _output_type = d.pop("output_type", UNSET)
        output_type: OutputTypeContract | Unset
        if isinstance(_output_type, Unset):
            output_type = UNSET
        else:
            output_type = OutputTypeContract.from_dict(_output_type)

        knowledge_bindings = cast(list[str], d.pop("knowledge_bindings", UNSET))

        _guardrails = d.pop("guardrails", UNSET)
        guardrails: AgentGuardrails | Unset
        if isinstance(_guardrails, Unset):
            guardrails = UNSET
        else:
            guardrails = AgentGuardrails.from_dict(_guardrails)

        _thinking = d.pop("thinking", UNSET)
        thinking: AgentThinking | Unset
        if isinstance(_thinking, Unset):
            thinking = UNSET
        else:
            thinking = AgentThinking.from_dict(_thinking)

        tool_choice = d.pop("tool_choice", UNSET)

        direct_tools = cast(list[str], d.pop("direct_tools", UNSET))

        _tool_scope = d.pop("tool_scope", UNSET)
        tool_scope: AgentUpdateToolScope | Unset
        if isinstance(_tool_scope, Unset):
            tool_scope = UNSET
        else:
            tool_scope = AgentUpdateToolScope(_tool_scope)

        _triage = d.pop("triage", UNSET)
        triage: AgentTriage | Unset
        if isinstance(_triage, Unset):
            triage = UNSET
        else:
            triage = AgentTriage.from_dict(_triage)

        turn_budget_tokens = d.pop("turn_budget_tokens", UNSET)

        agent_skills = cast(list[str], d.pop("agent_skills", UNSET))

        _on_ambiguous_entity = d.pop("on_ambiguous_entity", UNSET)
        on_ambiguous_entity: AgentUpdateOnAmbiguousEntity | Unset
        if isinstance(_on_ambiguous_entity, Unset):
            on_ambiguous_entity = UNSET
        else:
            on_ambiguous_entity = AgentUpdateOnAmbiguousEntity(_on_ambiguous_entity)

        _egress_guard = d.pop("egress_guard", UNSET)
        egress_guard: AgentUpdateEgressGuard | Unset
        if isinstance(_egress_guard, Unset):
            egress_guard = UNSET
        else:
            egress_guard = AgentUpdateEgressGuard(_egress_guard)

        clear_triage = d.pop("clear_triage", UNSET)

        agent_update = cls(
            name=name,
            model=model,
            system=system,
            tools=tools,
            owner=owner,
            visibility=visibility,
            filesystem=filesystem,
            agent_type=agent_type,
            brain=brain,
            capabilities=capabilities,
            max_turns=max_turns,
            output_type=output_type,
            knowledge_bindings=knowledge_bindings,
            guardrails=guardrails,
            thinking=thinking,
            tool_choice=tool_choice,
            direct_tools=direct_tools,
            tool_scope=tool_scope,
            triage=triage,
            turn_budget_tokens=turn_budget_tokens,
            agent_skills=agent_skills,
            on_ambiguous_entity=on_ambiguous_entity,
            egress_guard=egress_guard,
            clear_triage=clear_triage,
        )

        agent_update.additional_properties = d
        return agent_update

    @property
    def additional_keys(self) -> list[str]:
        return list(self.additional_properties.keys())

    def __getitem__(self, key: str) -> Any:
        return self.additional_properties[key]

    def __setitem__(self, key: str, value: Any) -> None:
        self.additional_properties[key] = value

    def __delitem__(self, key: str) -> None:
        del self.additional_properties[key]

    def __contains__(self, key: str) -> bool:
        return key in self.additional_properties
