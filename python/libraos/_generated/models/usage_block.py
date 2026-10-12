from __future__ import annotations

from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, TypeVar

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.usage_agent_skills import UsageAgentSkills
    from ..models.usage_block_tool_calls import UsageBlockToolCalls
    from ..models.usage_context_budget import UsageContextBudget
    from ..models.usage_phase import UsagePhase
    from ..models.usage_span import UsageSpan
    from ..models.usage_stage import UsageStage
    from ..models.usage_working_set import UsageWorkingSet


T = TypeVar("T", bound="UsageBlock")


@_attrs_define
class UsageBlock:
    """Aggregated token usage across all of the turn's model sub-calls, with a per-stage breakdown. Omitted on non-
    model/zero-usage turns. Excludes embedding calls.

        Attributes:
            prompt_tokens (int | Unset):
            completion_tokens (int | Unset):
            total_tokens (int | Unset):
            cache_read_tokens (int | Unset):
            cache_write_tokens (int | Unset):
            by_stage (list[UsageStage] | Unset):
            tool_calls (UsageBlockToolCalls | Unset): Tool calls this turn, by tool name.
            phases (list[UsagePhase] | Unset):
            timeline (list[UsageSpan] | Unset):
            context_budget (list[UsageContextBudget] | Unset):
            working_set (UsageWorkingSet | Unset): The conversation working set (documents attached in chat) carried by this
                turn.
            agent_skills (UsageAgentSkills | Unset): Agent Skills attached to and loaded by this turn.
    """

    prompt_tokens: int | Unset = UNSET
    completion_tokens: int | Unset = UNSET
    total_tokens: int | Unset = UNSET
    cache_read_tokens: int | Unset = UNSET
    cache_write_tokens: int | Unset = UNSET
    by_stage: list[UsageStage] | Unset = UNSET
    tool_calls: UsageBlockToolCalls | Unset = UNSET
    phases: list[UsagePhase] | Unset = UNSET
    timeline: list[UsageSpan] | Unset = UNSET
    context_budget: list[UsageContextBudget] | Unset = UNSET
    working_set: UsageWorkingSet | Unset = UNSET
    agent_skills: UsageAgentSkills | Unset = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        prompt_tokens = self.prompt_tokens

        completion_tokens = self.completion_tokens

        total_tokens = self.total_tokens

        cache_read_tokens = self.cache_read_tokens

        cache_write_tokens = self.cache_write_tokens

        by_stage: list[dict[str, Any]] | Unset = UNSET
        if not isinstance(self.by_stage, Unset):
            by_stage = []
            for by_stage_item_data in self.by_stage:
                by_stage_item = by_stage_item_data.to_dict()
                by_stage.append(by_stage_item)

        tool_calls: dict[str, Any] | Unset = UNSET
        if not isinstance(self.tool_calls, Unset):
            tool_calls = self.tool_calls.to_dict()

        phases: list[dict[str, Any]] | Unset = UNSET
        if not isinstance(self.phases, Unset):
            phases = []
            for phases_item_data in self.phases:
                phases_item = phases_item_data.to_dict()
                phases.append(phases_item)

        timeline: list[dict[str, Any]] | Unset = UNSET
        if not isinstance(self.timeline, Unset):
            timeline = []
            for timeline_item_data in self.timeline:
                timeline_item = timeline_item_data.to_dict()
                timeline.append(timeline_item)

        context_budget: list[dict[str, Any]] | Unset = UNSET
        if not isinstance(self.context_budget, Unset):
            context_budget = []
            for context_budget_item_data in self.context_budget:
                context_budget_item = context_budget_item_data.to_dict()
                context_budget.append(context_budget_item)

        working_set: dict[str, Any] | Unset = UNSET
        if not isinstance(self.working_set, Unset):
            working_set = self.working_set.to_dict()

        agent_skills: dict[str, Any] | Unset = UNSET
        if not isinstance(self.agent_skills, Unset):
            agent_skills = self.agent_skills.to_dict()

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if prompt_tokens is not UNSET:
            field_dict["prompt_tokens"] = prompt_tokens
        if completion_tokens is not UNSET:
            field_dict["completion_tokens"] = completion_tokens
        if total_tokens is not UNSET:
            field_dict["total_tokens"] = total_tokens
        if cache_read_tokens is not UNSET:
            field_dict["cache_read_tokens"] = cache_read_tokens
        if cache_write_tokens is not UNSET:
            field_dict["cache_write_tokens"] = cache_write_tokens
        if by_stage is not UNSET:
            field_dict["by_stage"] = by_stage
        if tool_calls is not UNSET:
            field_dict["tool_calls"] = tool_calls
        if phases is not UNSET:
            field_dict["phases"] = phases
        if timeline is not UNSET:
            field_dict["timeline"] = timeline
        if context_budget is not UNSET:
            field_dict["context_budget"] = context_budget
        if working_set is not UNSET:
            field_dict["working_set"] = working_set
        if agent_skills is not UNSET:
            field_dict["agent_skills"] = agent_skills

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.usage_agent_skills import UsageAgentSkills
        from ..models.usage_block_tool_calls import UsageBlockToolCalls
        from ..models.usage_context_budget import UsageContextBudget
        from ..models.usage_phase import UsagePhase
        from ..models.usage_span import UsageSpan
        from ..models.usage_stage import UsageStage
        from ..models.usage_working_set import UsageWorkingSet

        d = dict(src_dict)
        prompt_tokens = d.pop("prompt_tokens", UNSET)

        completion_tokens = d.pop("completion_tokens", UNSET)

        total_tokens = d.pop("total_tokens", UNSET)

        cache_read_tokens = d.pop("cache_read_tokens", UNSET)

        cache_write_tokens = d.pop("cache_write_tokens", UNSET)

        _by_stage = d.pop("by_stage", UNSET)
        by_stage: list[UsageStage] | Unset = UNSET
        if _by_stage is not UNSET:
            by_stage = []
            for by_stage_item_data in _by_stage:
                by_stage_item = UsageStage.from_dict(by_stage_item_data)

                by_stage.append(by_stage_item)

        _tool_calls = d.pop("tool_calls", UNSET)
        tool_calls: UsageBlockToolCalls | Unset
        if isinstance(_tool_calls, Unset):
            tool_calls = UNSET
        else:
            tool_calls = UsageBlockToolCalls.from_dict(_tool_calls)

        _phases = d.pop("phases", UNSET)
        phases: list[UsagePhase] | Unset = UNSET
        if _phases is not UNSET:
            phases = []
            for phases_item_data in _phases:
                phases_item = UsagePhase.from_dict(phases_item_data)

                phases.append(phases_item)

        _timeline = d.pop("timeline", UNSET)
        timeline: list[UsageSpan] | Unset = UNSET
        if _timeline is not UNSET:
            timeline = []
            for timeline_item_data in _timeline:
                timeline_item = UsageSpan.from_dict(timeline_item_data)

                timeline.append(timeline_item)

        _context_budget = d.pop("context_budget", UNSET)
        context_budget: list[UsageContextBudget] | Unset = UNSET
        if _context_budget is not UNSET:
            context_budget = []
            for context_budget_item_data in _context_budget:
                context_budget_item = UsageContextBudget.from_dict(context_budget_item_data)

                context_budget.append(context_budget_item)

        _working_set = d.pop("working_set", UNSET)
        working_set: UsageWorkingSet | Unset
        if isinstance(_working_set, Unset):
            working_set = UNSET
        else:
            working_set = UsageWorkingSet.from_dict(_working_set)

        _agent_skills = d.pop("agent_skills", UNSET)
        agent_skills: UsageAgentSkills | Unset
        if isinstance(_agent_skills, Unset):
            agent_skills = UNSET
        else:
            agent_skills = UsageAgentSkills.from_dict(_agent_skills)

        usage_block = cls(
            prompt_tokens=prompt_tokens,
            completion_tokens=completion_tokens,
            total_tokens=total_tokens,
            cache_read_tokens=cache_read_tokens,
            cache_write_tokens=cache_write_tokens,
            by_stage=by_stage,
            tool_calls=tool_calls,
            phases=phases,
            timeline=timeline,
            context_budget=context_budget,
            working_set=working_set,
            agent_skills=agent_skills,
        )

        usage_block.additional_properties = d
        return usage_block

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
