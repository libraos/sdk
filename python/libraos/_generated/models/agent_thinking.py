from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..models.agent_thinking_effort import AgentThinkingEffort
from ..types import UNSET, Unset

T = TypeVar("T", bound="AgentThinking")


@_attrs_define
class AgentThinking:
    """Native model reasoning on the agent's answer-tier call only (never the
    planner, triage or skill sub-tasks). `off` (the default) sends no
    reasoning parameter, so a model that reasons by default keeps
    reasoning; `none` asks the model not to reason. Per-call
    `metadata.thinking` wins. On PUT/PATCH send `{}` (or `effort: ""`) to
    clear; `null` keeps the current value.

        Attributes:
            effort (AgentThinkingEffort | Unset):
            budget_tokens (int | Unset): Explicit thinking-token budget; 0 derives it from `effort`.
    """

    effort: AgentThinkingEffort | Unset = UNSET
    budget_tokens: int | Unset = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        effort: str | Unset = UNSET
        if not isinstance(self.effort, Unset):
            effort = self.effort.value

        budget_tokens = self.budget_tokens

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if effort is not UNSET:
            field_dict["effort"] = effort
        if budget_tokens is not UNSET:
            field_dict["budget_tokens"] = budget_tokens

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        _effort = d.pop("effort", UNSET)
        effort: AgentThinkingEffort | Unset
        if isinstance(_effort, Unset):
            effort = UNSET
        else:
            effort = AgentThinkingEffort(_effort)

        budget_tokens = d.pop("budget_tokens", UNSET)

        agent_thinking = cls(
            effort=effort,
            budget_tokens=budget_tokens,
        )

        agent_thinking.additional_properties = d
        return agent_thinking

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
