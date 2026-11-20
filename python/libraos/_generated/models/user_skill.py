from __future__ import annotations

import datetime
from collections.abc import Mapping
from typing import Any, TypeVar

from attrs import define as _attrs_define
from attrs import field as _attrs_field
from dateutil.parser import isoparse

from ..models.user_skill_status import UserSkillStatus
from ..types import UNSET, Unset

T = TypeVar("T", bound="UserSkill")


@_attrs_define
class UserSkill:
    """One of a person's active skills, pinned to a catalog version and its SHA-256. A later import or publish of the same
    name does not change it.

        Attributes:
            name (str):
            version (int):
            sha256 (str):
            activated_at (datetime.datetime):
            status (UserSkillStatus): `unavailable` when the version is no longer published (for example archived) or no
                longer has the approved content. An unavailable skill is not used on the person's turns.
            request_id (str | Unset): The approved request that activated it.
            activated_by (str | Unset): The admin who approved it.
            reason (str | Unset): Why the skill is unavailable.
            description (str | Unset): The catalog version's description; omitted when the version cannot be read.
            source (str | Unset): Where the version came from, e.g. `github.com/<owner>/<repo>@<commit>/<path>`; omitted
                when the version cannot be read.
    """

    name: str
    version: int
    sha256: str
    activated_at: datetime.datetime
    status: UserSkillStatus
    request_id: str | Unset = UNSET
    activated_by: str | Unset = UNSET
    reason: str | Unset = UNSET
    description: str | Unset = UNSET
    source: str | Unset = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        name = self.name

        version = self.version

        sha256 = self.sha256

        activated_at = self.activated_at.isoformat()

        status = self.status.value

        request_id = self.request_id

        activated_by = self.activated_by

        reason = self.reason

        description = self.description

        source = self.source

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "name": name,
                "version": version,
                "sha256": sha256,
                "activated_at": activated_at,
                "status": status,
            }
        )
        if request_id is not UNSET:
            field_dict["request_id"] = request_id
        if activated_by is not UNSET:
            field_dict["activated_by"] = activated_by
        if reason is not UNSET:
            field_dict["reason"] = reason
        if description is not UNSET:
            field_dict["description"] = description
        if source is not UNSET:
            field_dict["source"] = source

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        name = d.pop("name")

        version = d.pop("version")

        sha256 = d.pop("sha256")

        activated_at = isoparse(d.pop("activated_at"))

        status = UserSkillStatus(d.pop("status"))

        request_id = d.pop("request_id", UNSET)

        activated_by = d.pop("activated_by", UNSET)

        reason = d.pop("reason", UNSET)

        description = d.pop("description", UNSET)

        source = d.pop("source", UNSET)

        user_skill = cls(
            name=name,
            version=version,
            sha256=sha256,
            activated_at=activated_at,
            status=status,
            request_id=request_id,
            activated_by=activated_by,
            reason=reason,
            description=description,
            source=source,
        )

        user_skill.additional_properties = d
        return user_skill

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
