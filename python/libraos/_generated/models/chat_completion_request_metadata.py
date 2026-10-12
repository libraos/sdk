from __future__ import annotations

from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, TypeVar, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..models.chat_completion_request_metadata_brain import ChatCompletionRequestMetadataBrain
from ..models.chat_completion_request_metadata_egress_guard import ChatCompletionRequestMetadataEgressGuard
from ..models.chat_completion_request_metadata_on_ambiguous_entity import ChatCompletionRequestMetadataOnAmbiguousEntity
from ..models.chat_completion_request_metadata_research_depth import ChatCompletionRequestMetadataResearchDepth
from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.chat_completion_request_metadata_thinking import ChatCompletionRequestMetadataThinking


T = TypeVar("T", bound="ChatCompletionRequestMetadata")


@_attrs_define
class ChatCompletionRequestMetadata:
    """Nova OS extension channel for per-call fields (e.g. a per-call model override). The documented keys below are
    honoured on this surface the same way as on native chat.

        Attributes:
            max_tokens (int | Unset): Per-call answer output-token cap; wins over the top-level fields.
            temperature (float | Unset): Per-call answer temperature; wins over the top-level field.
            brain (ChatCompletionRequestMetadataBrain | Unset): Per-call planning override.
            stream_events (bool | Unset): Per-call orchestration event streaming toggle.
            research_query (str | Unset): The research question as its own field, when the message is an assembled prompt.
                Overrides the query used for outbound search.
            research_query_only (bool | Unset): Fixed-query mode: every outbound search of the turn is exactly
                `research_query`, and fetches are limited to URLs those searches returned. Requires a non-empty, single-line
                `research_query` of at most 300 characters; otherwise 400.
            max_searches (int | Unset): Per-turn cap on outbound search calls across every tool of the turn. Absent or 0
                means unlimited.
            egress_guard (ChatCompletionRequestMetadataEgressGuard | Unset): Adds the outbound query guard for this request.
                May only tighten: `off` never removes a guard set by the server or the agent. Any other value is a 400.
            allowed_skills (list[str] | Unset): Narrows a persona's planner to these skills for this turn. A name the
                persona does not have is a 400; ignored on non-persona agents.
            research_depth (ChatCompletionRequestMetadataResearchDepth | Unset): Per-call research depth. `fast` skips the
                planner; `deep` runs it; `auto` runs it single-shot, without multi-wave skills such as `deep_research`. `brain`
                wins when both are set. Unknown values are ignored.
            on_ambiguous_entity (ChatCompletionRequestMetadataOnAmbiguousEntity | Unset): Overrides the agent's handling of
                answers whose evidence spans several documents the question does not choose between. Invalid values are ignored.
            thinking (ChatCompletionRequestMetadataThinking | Unset): Per-call native reasoning on the answer-tier call;
                overrides the agent's `thinking`. `off` sends no reasoning parameter, `none` asks the model not to reason.
                `budget_tokens` is clamped to 1024-32768. An invalid override is ignored.
            tool_choice (str | Unset): Per-call tool choice for the first model call: `auto`, `none`, `required`, or a tool
                name. Overrides the agent's `tool_choice`. Invalid values are ignored.
    """

    max_tokens: int | Unset = UNSET
    temperature: float | Unset = UNSET
    brain: ChatCompletionRequestMetadataBrain | Unset = UNSET
    stream_events: bool | Unset = UNSET
    research_query: str | Unset = UNSET
    research_query_only: bool | Unset = UNSET
    max_searches: int | Unset = UNSET
    egress_guard: ChatCompletionRequestMetadataEgressGuard | Unset = UNSET
    allowed_skills: list[str] | Unset = UNSET
    research_depth: ChatCompletionRequestMetadataResearchDepth | Unset = UNSET
    on_ambiguous_entity: ChatCompletionRequestMetadataOnAmbiguousEntity | Unset = UNSET
    thinking: ChatCompletionRequestMetadataThinking | Unset = UNSET
    tool_choice: str | Unset = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        max_tokens = self.max_tokens

        temperature = self.temperature

        brain: str | Unset = UNSET
        if not isinstance(self.brain, Unset):
            brain = self.brain.value

        stream_events = self.stream_events

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
        if max_tokens is not UNSET:
            field_dict["max_tokens"] = max_tokens
        if temperature is not UNSET:
            field_dict["temperature"] = temperature
        if brain is not UNSET:
            field_dict["brain"] = brain
        if stream_events is not UNSET:
            field_dict["stream_events"] = stream_events
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
        from ..models.chat_completion_request_metadata_thinking import ChatCompletionRequestMetadataThinking

        d = dict(src_dict)
        max_tokens = d.pop("max_tokens", UNSET)

        temperature = d.pop("temperature", UNSET)

        _brain = d.pop("brain", UNSET)
        brain: ChatCompletionRequestMetadataBrain | Unset
        if isinstance(_brain, Unset):
            brain = UNSET
        else:
            brain = ChatCompletionRequestMetadataBrain(_brain)

        stream_events = d.pop("stream_events", UNSET)

        research_query = d.pop("research_query", UNSET)

        research_query_only = d.pop("research_query_only", UNSET)

        max_searches = d.pop("max_searches", UNSET)

        _egress_guard = d.pop("egress_guard", UNSET)
        egress_guard: ChatCompletionRequestMetadataEgressGuard | Unset
        if isinstance(_egress_guard, Unset):
            egress_guard = UNSET
        else:
            egress_guard = ChatCompletionRequestMetadataEgressGuard(_egress_guard)

        allowed_skills = cast(list[str], d.pop("allowed_skills", UNSET))

        _research_depth = d.pop("research_depth", UNSET)
        research_depth: ChatCompletionRequestMetadataResearchDepth | Unset
        if isinstance(_research_depth, Unset):
            research_depth = UNSET
        else:
            research_depth = ChatCompletionRequestMetadataResearchDepth(_research_depth)

        _on_ambiguous_entity = d.pop("on_ambiguous_entity", UNSET)
        on_ambiguous_entity: ChatCompletionRequestMetadataOnAmbiguousEntity | Unset
        if isinstance(_on_ambiguous_entity, Unset):
            on_ambiguous_entity = UNSET
        else:
            on_ambiguous_entity = ChatCompletionRequestMetadataOnAmbiguousEntity(_on_ambiguous_entity)

        _thinking = d.pop("thinking", UNSET)
        thinking: ChatCompletionRequestMetadataThinking | Unset
        if isinstance(_thinking, Unset):
            thinking = UNSET
        else:
            thinking = ChatCompletionRequestMetadataThinking.from_dict(_thinking)

        tool_choice = d.pop("tool_choice", UNSET)

        chat_completion_request_metadata = cls(
            max_tokens=max_tokens,
            temperature=temperature,
            brain=brain,
            stream_events=stream_events,
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

        chat_completion_request_metadata.additional_properties = d
        return chat_completion_request_metadata

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
