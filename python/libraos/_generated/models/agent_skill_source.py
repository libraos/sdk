from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..models.agent_skill_source_kind import AgentSkillSourceKind
from ..types import UNSET, Unset

T = TypeVar("T", bound="AgentSkillSource")


@_attrs_define
class AgentSkillSource:
    """
    Attributes:
        kind (AgentSkillSourceKind):
        repo (str | Unset): `owner/repo` for GitHub imports.
        ref (str | Unset):
        commit (str | Unset):
        path (str | Unset):
    """

    kind: AgentSkillSourceKind
    repo: str | Unset = UNSET
    ref: str | Unset = UNSET
    commit: str | Unset = UNSET
    path: str | Unset = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        kind = self.kind.value

        repo = self.repo

        ref = self.ref

        commit = self.commit

        path = self.path

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "kind": kind,
            }
        )
        if repo is not UNSET:
            field_dict["repo"] = repo
        if ref is not UNSET:
            field_dict["ref"] = ref
        if commit is not UNSET:
            field_dict["commit"] = commit
        if path is not UNSET:
            field_dict["path"] = path

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        kind = AgentSkillSourceKind(d.pop("kind"))

        repo = d.pop("repo", UNSET)

        ref = d.pop("ref", UNSET)

        commit = d.pop("commit", UNSET)

        path = d.pop("path", UNSET)

        agent_skill_source = cls(
            kind=kind,
            repo=repo,
            ref=ref,
            commit=commit,
            path=path,
        )

        agent_skill_source.additional_properties = d
        return agent_skill_source

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
