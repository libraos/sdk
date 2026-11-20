from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

T = TypeVar("T", bound="SkillRequestCreate")


@_attrs_define
class SkillRequestCreate:
    """
    Attributes:
        url (str): HTTPS link to a GitHub repository, a `tree`/`blob` folder or file in one, or a
            `raw.githubusercontent.com` file: any form `POST /v1/skills/import` accepts. A link to a `SKILL.md` means its
            folder. At most 2048 characters.
        note (str | Unset): For the reviewing admin. At most 1000 characters.
    """

    url: str
    note: str | Unset = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        url = self.url

        note = self.note

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "url": url,
            }
        )
        if note is not UNSET:
            field_dict["note"] = note

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        url = d.pop("url")

        note = d.pop("note", UNSET)

        skill_request_create = cls(
            url=url,
            note=note,
        )

        skill_request_create.additional_properties = d
        return skill_request_create

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
