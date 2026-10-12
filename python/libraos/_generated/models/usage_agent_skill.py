from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

T = TypeVar("T", bound="UsageAgentSkill")


@_attrs_define
class UsageAgentSkill:
    """
    Attributes:
        skill (str | Unset):
        version (int | Unset):
        sha256 (str | Unset):
        source (str | Unset):
    """

    skill: str | Unset = UNSET
    version: int | Unset = UNSET
    sha256: str | Unset = UNSET
    source: str | Unset = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        skill = self.skill

        version = self.version

        sha256 = self.sha256

        source = self.source

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if skill is not UNSET:
            field_dict["skill"] = skill
        if version is not UNSET:
            field_dict["version"] = version
        if sha256 is not UNSET:
            field_dict["sha256"] = sha256
        if source is not UNSET:
            field_dict["source"] = source

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        skill = d.pop("skill", UNSET)

        version = d.pop("version", UNSET)

        sha256 = d.pop("sha256", UNSET)

        source = d.pop("source", UNSET)

        usage_agent_skill = cls(
            skill=skill,
            version=version,
            sha256=sha256,
            source=source,
        )

        usage_agent_skill.additional_properties = d
        return usage_agent_skill

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
