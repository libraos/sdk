from __future__ import annotations

from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, TypeVar, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..models.native_chat_metadata_brain import NativeChatMetadataBrain
from ..models.native_chat_metadata_egress_guard import NativeChatMetadataEgressGuard
from ..models.native_chat_metadata_on_ambiguous_entity import NativeChatMetadataOnAmbiguousEntity
from ..models.native_chat_metadata_research_depth import NativeChatMetadataResearchDepth
from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.native_chat_metadata_thinking import NativeChatMetadataThinking


T = TypeVar("T", bound="NativeChatMetadata")


@_attrs_define
class NativeChatMetadata:
    """Opaque per-request metadata. LibraOS does not interpret arbitrary keys (they are threaded through tenant isolation
    and audit), but a few reserved keys control per-call behavior.

        Attributes:
            stream_events (bool | Unset): When true (and streaming), emit granular orchestration events (tool_use /
                tool_result / text / thinking) over SSE.
            stream_thinking (bool | Unset): When true, include model reasoning as `thinking` SSE events. Independent of
                stream_events; default off.
            max_tokens (int | Unset): Per-call output-token cap for the answer, overriding the agent's configured limit.
                Must be > 0; clamped to 32768.
            brain (NativeChatMetadataBrain | Unset): Per-call planning override. One of `always` or `never`; controls
                whether the multi-step planner runs for this turn.
            research_query (str | Unset): The research question as its own field, when the message is an assembled prompt.
                Overrides the query used for outbound search.
            research_query_only (bool | Unset): Fixed-query mode: every outbound search of the turn is exactly
                `research_query`, and fetches are limited to URLs those searches returned. Requires a non-empty, single-line
                `research_query` of at most 300 characters; otherwise 400.
            max_searches (int | Unset): Per-turn cap on outbound search calls across every tool of the turn. Absent or 0
                means unlimited.
            egress_guard (NativeChatMetadataEgressGuard | Unset): Adds the outbound query guard for this request. May only
                tighten: `off` never removes a guard set by the server or the agent. Any other value is a 400.
            allowed_skills (list[str] | Unset): Narrows a persona's planner to these skills for this turn. A name the
                persona does not have is a 400; ignored on non-persona agents.
            research_depth (NativeChatMetadataResearchDepth | Unset): Per-call research depth. `fast` skips the planner;
                `deep` runs it; `auto` runs it single-shot, without multi-wave skills such as `deep_research`. `brain` wins when
                both are set. Unknown values are ignored.
            on_ambiguous_entity (NativeChatMetadataOnAmbiguousEntity | Unset): Overrides the agent's handling of answers
                whose evidence spans several documents the question does not choose between. Invalid values are ignored.
            thinking (NativeChatMetadataThinking | Unset): Per-call native reasoning on the answer-tier call; overrides the
                agent's `thinking`. `off` sends no reasoning parameter, `none` asks the model not to reason. `budget_tokens` is
                clamped to 1024-32768. An invalid override is ignored.
            tool_choice (str | Unset): Per-call tool choice for the first model call: `auto`, `none`, `required`, or a tool
                name. Overrides the agent's `tool_choice`. Invalid values are ignored.
    """

    stream_events: bool | Unset = UNSET
    stream_thinking: bool | Unset = UNSET
    max_tokens: int | Unset = UNSET
    brain: NativeChatMetadataBrain | Unset = UNSET
    research_query: str | Unset = UNSET
    research_query_only: bool | Unset = UNSET
    max_searches: int | Unset = UNSET
    egress_guard: NativeChatMetadataEgressGuard | Unset = UNSET
    allowed_skills: list[str] | Unset = UNSET
    research_depth: NativeChatMetadataResearchDepth | Unset = UNSET
    on_ambiguous_entity: NativeChatMetadataOnAmbiguousEntity | Unset = UNSET
    thinking: NativeChatMetadataThinking | Unset = UNSET
    tool_choice: str | Unset = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        stream_events = self.stream_events

        stream_thinking = self.stream_thinking

        max_tokens = self.max_tokens

        brain: str | Unset = UNSET
        if not isinstance(self.brain, Unset):
            brain = self.brain.value

        research_query = self.research_query

        research_query_only = self.research_query_only

        max_searches = self.max_searches

        egress_guard: str | Unset = UNSET
        if not isinstance(self.egress_guard, Unset):
            egress_guard = self.egress_guard.value

        allowed_skills: list[str] | Unset = UNSET
        if not isinstance(self.allowed_skills, Unset):
            allowed_skills = self.allowed_skills

        research_depth: str | Unset = UNSET
        if not isinstance(self.research_depth, Unset):
            research_depth = self.research_depth.value

        on_ambiguous_entity: str | Unset = UNSET
        if not isinstance(self.on_ambiguous_entity, Unset):
            on_ambiguous_entity = self.on_ambiguous_entity.value

        thinking: dict[str, Any] | Unset = UNSET
        if not isinstance(self.thinking, Unset):
            thinking = self.thinking.to_dict()

        tool_choice = self.tool_choice

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if stream_events is not UNSET:
            field_dict["stream_events"] = stream_events
        if stream_thinking is not UNSET:
            field_dict["stream_thinking"] = stream_thinking
        if max_tokens is not UNSET:
            field_dict["max_tokens"] = max_tokens
        if brain is not UNSET:
            field_dict["brain"] = brain
        if research_query is not UNSET:
            field_dict["research_query"] = research_query
        if research_query_only is not UNSET:
            field_dict["research_query_only"] = research_query_only
        if max_searches is not UNSET:
            field_dict["max_searches"] = max_searches
        if egress_guard is not UNSET:
            field_dict["egress_guard"] = egress_guard
        if allowed_skills is not UNSET:
            field_dict["allowed_skills"] = allowed_skills
        if research_depth is not UNSET:
            field_dict["research_depth"] = research_depth
        if on_ambiguous_entity is not UNSET:
            field_dict["on_ambiguous_entity"] = on_ambiguous_entity
        if thinking is not UNSET:
            field_dict["thinking"] = thinking
        if tool_choice is not UNSET:
            field_dict["tool_choice"] = tool_choice

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.native_chat_metadata_thinking import NativeChatMetadataThinking

        d = dict(src_dict)
        stream_events = d.pop("stream_events", UNSET)

        stream_thinking = d.pop("stream_thinking", UNSET)

        max_tokens = d.pop("max_tokens", UNSET)

        _brain = d.pop("brain", UNSET)
        brain: NativeChatMetadataBrain | Unset
        if isinstance(_brain, Unset):
            brain = UNSET
        else:
            brain = NativeChatMetadataBrain(_brain)

        research_query = d.pop("research_query", UNSET)

        research_query_only = d.pop("research_query_only", UNSET)

        max_searches = d.pop("max_searches", UNSET)

        _egress_guard = d.pop("egress_guard", UNSET)
        egress_guard: NativeChatMetadataEgressGuard | Unset
        if isinstance(_egress_guard, Unset):
            egress_guard = UNSET
        else:
            egress_guard = NativeChatMetadataEgressGuard(_egress_guard)

        allowed_skills = cast(list[str], d.pop("allowed_skills", UNSET))

        _research_depth = d.pop("research_depth", UNSET)
        research_depth: NativeChatMetadataResearchDepth | Unset
        if isinstance(_research_depth, Unset):
            research_depth = UNSET
        else:
            research_depth = NativeChatMetadataResearchDepth(_research_depth)

        _on_ambiguous_entity = d.pop("on_ambiguous_entity", UNSET)
        on_ambiguous_entity: NativeChatMetadataOnAmbiguousEntity | Unset
        if isinstance(_on_ambiguous_entity, Unset):
            on_ambiguous_entity = UNSET
        else:
            on_ambiguous_entity = NativeChatMetadataOnAmbiguousEntity(_on_ambiguous_entity)

        _thinking = d.pop("thinking", UNSET)
        thinking: NativeChatMetadataThinking | Unset
        if isinstance(_thinking, Unset):
            thinking = UNSET
        else:
            thinking = NativeChatMetadataThinking.from_dict(_thinking)

        tool_choice = d.pop("tool_choice", UNSET)

        native_chat_metadata = cls(
            stream_events=stream_events,
            stream_thinking=stream_thinking,
            max_tokens=max_tokens,
            brain=brain,
            research_query=research_query,
            research_query_only=research_query_only,
            max_searches=max_searches,
            egress_guard=egress_guard,
            allowed_skills=allowed_skills,
            research_depth=research_depth,
            on_ambiguous_entity=on_ambiguous_entity,
            thinking=thinking,
            tool_choice=tool_choice,
        )

        native_chat_metadata.additional_properties = d
        return native_chat_metadata

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
