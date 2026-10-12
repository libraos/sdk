from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

T = TypeVar("T", bound="AgentSkillImportRequest")


@_attrs_define
class AgentSkillImportRequest:
    """
    Attributes:
        url (str): HTTPS link to a GitHub repository, a `tree`/`blob` folder or file in one, or a
            `raw.githubusercontent.com` file. A link to a `SKILL.md` means its folder.
        skills (list[str] | Unset): Import only these skill names; empty imports all found.
        dry_run (bool | Unset): Return what would be imported without writing anything.
    """

    url: str
    skills: list[str] | Unset = UNSET
    dry_run: bool | Unset = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        url = self.url

        skills: list[str] | Unset = UNSET
        if not isinstance(self.skills, Unset):
            skills = self.skills

        dry_run = self.dry_run

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "url": url,
            }
        )
        if skills is not UNSET:
            field_dict["skills"] = skills
        if dry_run is not UNSET:
            field_dict["dry_run"] = dry_run

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        url = d.pop("url")

        skills = cast(list[str], d.pop("skills", UNSET))

        dry_run = d.pop("dry_run", UNSET)

        agent_skill_import_request = cls(
            url=url,
            skills=skills,
            dry_run=dry_run,
        )

        agent_skill_import_request.additional_properties = d
        return agent_skill_import_request

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
