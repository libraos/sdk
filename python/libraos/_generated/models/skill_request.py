from __future__ import annotations

import datetime
from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, TypeVar

from attrs import define as _attrs_define
from attrs import field as _attrs_field
from dateutil.parser import isoparse

from ..models.skill_request_status import SkillRequestStatus
from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.approved_user_skill import ApprovedUserSkill


T = TypeVar("T", bound="SkillRequest")


@_attrs_define
class SkillRequest:
    """One person's request for a skill from a GitHub link.

    Attributes:
        id (str):
        user_id (str): The requester. An approval activates the skill for them only.
        url (str): The link as submitted.
        repo (str): `owner/repo`.
        status (SkillRequestStatus):
        created_at (datetime.datetime):
        ref (str | Unset): The branch, tag or commit the link names; omitted for the default branch.
        path (str | Unset): The folder the link names; omitted for the repository root.
        note (str | Unset):
        decided_by (str | Unset): Who approved, rejected or withdrew the request.
        decided_at (datetime.datetime | Unset):
        reason (str | Unset): The admin's reason for a rejection.
        commit (str | Unset): Set by an approval; the commit that was imported.
        license_ (str | Unset): Set by an approval; the repository licence that was recorded.
        skills (list[ApprovedUserSkill] | Unset): Set by an approval; the versions activated for the requester.
    """

    id: str
    user_id: str
    url: str
    repo: str
    status: SkillRequestStatus
    created_at: datetime.datetime
    ref: str | Unset = UNSET
    path: str | Unset = UNSET
    note: str | Unset = UNSET
    decided_by: str | Unset = UNSET
    decided_at: datetime.datetime | Unset = UNSET
    reason: str | Unset = UNSET
    commit: str | Unset = UNSET
    license_: str | Unset = UNSET
    skills: list[ApprovedUserSkill] | Unset = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        id = self.id

        user_id = self.user_id

        url = self.url

        repo = self.repo

        status = self.status.value

        created_at = self.created_at.isoformat()

        ref = self.ref

        path = self.path

        note = self.note

        decided_by = self.decided_by

        decided_at: str | Unset = UNSET
        if not isinstance(self.decided_at, Unset):
            decided_at = self.decided_at.isoformat()

        reason = self.reason

        commit = self.commit

        license_ = self.license_

        skills: list[dict[str, Any]] | Unset = UNSET
        if not isinstance(self.skills, Unset):
            skills = []
            for skills_item_data in self.skills:
                skills_item = skills_item_data.to_dict()
                skills.append(skills_item)

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "id": id,
                "user_id": user_id,
                "url": url,
                "repo": repo,
                "status": status,
                "created_at": created_at,
            }
        )
        if ref is not UNSET:
            field_dict["ref"] = ref
        if path is not UNSET:
            field_dict["path"] = path
        if note is not UNSET:
            field_dict["note"] = note
        if decided_by is not UNSET:
            field_dict["decided_by"] = decided_by
        if decided_at is not UNSET:
            field_dict["decided_at"] = decided_at
        if reason is not UNSET:
            field_dict["reason"] = reason
        if commit is not UNSET:
            field_dict["commit"] = commit
        if license_ is not UNSET:
            field_dict["license"] = license_
        if skills is not UNSET:
            field_dict["skills"] = skills

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.approved_user_skill import ApprovedUserSkill

        d = dict(src_dict)
        id = d.pop("id")

        user_id = d.pop("user_id")

        url = d.pop("url")

        repo = d.pop("repo")

        status = SkillRequestStatus(d.pop("status"))

        created_at = isoparse(d.pop("created_at"))

        ref = d.pop("ref", UNSET)

        path = d.pop("path", UNSET)

        note = d.pop("note", UNSET)

        decided_by = d.pop("decided_by", UNSET)

        _decided_at = d.pop("decided_at", UNSET)
        decided_at: datetime.datetime | Unset
        if isinstance(_decided_at, Unset):
            decided_at = UNSET
        else:
            decided_at = isoparse(_decided_at)

        reason = d.pop("reason", UNSET)

        commit = d.pop("commit", UNSET)

        license_ = d.pop("license", UNSET)

        _skills = d.pop("skills", UNSET)
        skills: list[ApprovedUserSkill] | Unset = UNSET
        if _skills is not UNSET:
            skills = []
            for skills_item_data in _skills:
                skills_item = ApprovedUserSkill.from_dict(skills_item_data)

                skills.append(skills_item)

        skill_request = cls(
            id=id,
            user_id=user_id,
            url=url,
            repo=repo,
            status=status,
            created_at=created_at,
            ref=ref,
            path=path,
            note=note,
            decided_by=decided_by,
            decided_at=decided_at,
            reason=reason,
            commit=commit,
            license_=license_,
            skills=skills,
        )

        skill_request.additional_properties = d
        return skill_request

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
