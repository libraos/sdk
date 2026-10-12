from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..models.usage_context_budget_turn_budget_source import UsageContextBudgetTurnBudgetSource
from ..models.usage_context_budget_window_source import UsageContextBudgetWindowSource
from ..types import UNSET, Unset

T = TypeVar("T", bound="UsageContextBudget")


@_attrs_define
class UsageContextBudget:
    """Context window and turn budget applied to the model calls of one model in this turn.

    Attributes:
        model (str | Unset):
        window (int | Unset): Context window in tokens; omitted when unbounded.
        window_source (UsageContextBudgetWindowSource | Unset):
        turn_budget (int | Unset): Per-turn token budget; omitted when none applies.
        turn_budget_source (UsageContextBudgetTurnBudgetSource | Unset):
        budget (int | Unset): Effective budget (the tighter of window and turn budget).
        calls (int | Unset):
        trimmed (int | Unset): Calls whose conversation was trimmed to fit.
    """

    model: str | Unset = UNSET
    window: int | Unset = UNSET
    window_source: UsageContextBudgetWindowSource | Unset = UNSET
    turn_budget: int | Unset = UNSET
    turn_budget_source: UsageContextBudgetTurnBudgetSource | Unset = UNSET
    budget: int | Unset = UNSET
    calls: int | Unset = UNSET
    trimmed: int | Unset = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        model = self.model

        window = self.window

        window_source: str | Unset = UNSET
        if not isinstance(self.window_source, Unset):
            window_source = self.window_source.value

        turn_budget = self.turn_budget

        turn_budget_source: str | Unset = UNSET
        if not isinstance(self.turn_budget_source, Unset):
            turn_budget_source = self.turn_budget_source.value

        budget = self.budget

        calls = self.calls

        trimmed = self.trimmed

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if model is not UNSET:
            field_dict["model"] = model
        if window is not UNSET:
            field_dict["window"] = window
        if window_source is not UNSET:
            field_dict["window_source"] = window_source
        if turn_budget is not UNSET:
            field_dict["turn_budget"] = turn_budget
        if turn_budget_source is not UNSET:
            field_dict["turn_budget_source"] = turn_budget_source
        if budget is not UNSET:
            field_dict["budget"] = budget
        if calls is not UNSET:
            field_dict["calls"] = calls
        if trimmed is not UNSET:
            field_dict["trimmed"] = trimmed

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        model = d.pop("model", UNSET)

        window = d.pop("window", UNSET)

        _window_source = d.pop("window_source", UNSET)
        window_source: UsageContextBudgetWindowSource | Unset
        if isinstance(_window_source, Unset):
            window_source = UNSET
        else:
            window_source = UsageContextBudgetWindowSource(_window_source)

        turn_budget = d.pop("turn_budget", UNSET)

        _turn_budget_source = d.pop("turn_budget_source", UNSET)
        turn_budget_source: UsageContextBudgetTurnBudgetSource | Unset
        if isinstance(_turn_budget_source, Unset):
            turn_budget_source = UNSET
        else:
            turn_budget_source = UsageContextBudgetTurnBudgetSource(_turn_budget_source)

        budget = d.pop("budget", UNSET)

        calls = d.pop("calls", UNSET)

        trimmed = d.pop("trimmed", UNSET)

        usage_context_budget = cls(
            model=model,
            window=window,
            window_source=window_source,
            turn_budget=turn_budget,
            turn_budget_source=turn_budget_source,
            budget=budget,
            calls=calls,
            trimmed=trimmed,
        )

        usage_context_budget.additional_properties = d
        return usage_context_budget

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
