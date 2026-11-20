from __future__ import annotations

from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, TypeVar

from attrs import define as _attrs_define
from attrs import field as _attrs_field

if TYPE_CHECKING:
    from ..models.skill_request import SkillRequest
    from ..models.skill_request_candidate import SkillRequestCandidate


T = TypeVar("T", bound="SkillRequestPreview")


@_attrs_define
class SkillRequestPreview:
    """
    Attributes:
        request (SkillRequest): One person's request for a skill from a GitHub link.
        repo (str):
        ref (str): The ref the link names; empty for the default branch.
        commit (str): The 40-character commit the ref resolved to. Approve with this value.
        license_ (str): The repository's root licence, e.g. `MIT`, or `LicenseRef-see-LICENSE`.
        skills (list[SkillRequestCandidate]):
    """

    request: SkillRequest
    repo: str
    ref: str
    commit: str
    license_: str
    skills: list[SkillRequestCandidate]
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        request = self.request.to_dict()

        repo = self.repo

        ref = self.ref

        commit = self.commit

        license_ = self.license_

        skills = []
        for skills_item_data in self.skills:
            skills_item = skills_item_data.to_dict()
            skills.append(skills_item)

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "request": request,
                "repo": repo,
                "ref": ref,
                "commit": commit,
                "license": license_,
                "skills": skills,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.skill_request import SkillRequest
        from ..models.skill_request_candidate import SkillRequestCandidate

        d = dict(src_dict)
        request = SkillRequest.from_dict(d.pop("request"))

        repo = d.pop("repo")

        ref = d.pop("ref")

        commit = d.pop("commit")

        license_ = d.pop("license")

        skills = []
        _skills = d.pop("skills")
        for skills_item_data in _skills:
            skills_item = SkillRequestCandidate.from_dict(skills_item_data)

            skills.append(skills_item)

        skill_request_preview = cls(
            request=request,
            repo=repo,
            ref=ref,
            commit=commit,
            license_=license_,
            skills=skills,
        )

        skill_request_preview.additional_properties = d
        return skill_request_preview

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
