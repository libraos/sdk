from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..models.agent_skill_file_diff_change import AgentSkillFileDiffChange
from ..types import UNSET, Unset

T = TypeVar("T", bound="AgentSkillFileDiff")


@_attrs_define
class AgentSkillFileDiff:
    """
    Attributes:
        path (str):
        change (AgentSkillFileDiffChange):
        diff (str | Unset): Unified diff; omitted for very large files.
    """

    path: str
    change: AgentSkillFileDiffChange
    diff: str | Unset = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        path = self.path

        change = self.change.value

        diff = self.diff

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "path": path,
                "change": change,
            }
        )
        if diff is not UNSET:
            field_dict["diff"] = diff

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        path = d.pop("path")

        change = AgentSkillFileDiffChange(d.pop("change"))

        diff = d.pop("diff", UNSET)

        agent_skill_file_diff = cls(
            path=path,
            change=change,
            diff=diff,
        )

        agent_skill_file_diff.additional_properties = d
        return agent_skill_file_diff

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
