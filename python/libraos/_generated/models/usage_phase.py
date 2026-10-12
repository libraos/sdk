from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

T = TypeVar("T", bound="UsagePhase")


@_attrs_define
class UsagePhase:
    """Wall time of one phase of the turn. Phases are interval unions, so parallel tasks count once. A final `turn` row is
    always present.

        Attributes:
            phase (str | Unset): One of `triage`, `planner`, `skills`, `tools`, `synthesis`, `direct`, `llm`, `turn`.
            duration_ms (int | Unset):
            count (int | Unset):
    """

    phase: str | Unset = UNSET
    duration_ms: int | Unset = UNSET
    count: int | Unset = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        phase = self.phase

        duration_ms = self.duration_ms

        count = self.count

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if phase is not UNSET:
            field_dict["phase"] = phase
        if duration_ms is not UNSET:
            field_dict["duration_ms"] = duration_ms
        if count is not UNSET:
            field_dict["count"] = count

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        phase = d.pop("phase", UNSET)

        duration_ms = d.pop("duration_ms", UNSET)

        count = d.pop("count", UNSET)

        usage_phase = cls(
            phase=phase,
            duration_ms=duration_ms,
            count=count,
        )

        usage_phase.additional_properties = d
        return usage_phase

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
