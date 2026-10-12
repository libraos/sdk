from __future__ import annotations

from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, TypeVar

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.agent_skill_file_diff import AgentSkillFileDiff
    from ..models.agent_skill_source import AgentSkillSource


T = TypeVar("T", bound="AgentSkillUpstream")


@_attrs_define
class AgentSkillUpstream:
    """
    Attributes:
        version (int):
        source (AgentSkillSource):
        upstream_commit (str):
        up_to_date (bool):
        files (list[AgentSkillFileDiff] | Unset): Differences from upstream, when not up to date and the path still
            exists.
        license_ (str | Unset):
        removed_upstream (bool | Unset): True when the skill's path no longer exists upstream.
    """

    version: int
    source: AgentSkillSource
    upstream_commit: str
    up_to_date: bool
    files: list[AgentSkillFileDiff] | Unset = UNSET
    license_: str | Unset = UNSET
    removed_upstream: bool | Unset = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        version = self.version

        source = self.source.to_dict()

        upstream_commit = self.upstream_commit

        up_to_date = self.up_to_date

        files: list[dict[str, Any]] | Unset = UNSET
        if not isinstance(self.files, Unset):
            files = []
            for files_item_data in self.files:
                files_item = files_item_data.to_dict()
                files.append(files_item)

        license_ = self.license_

        removed_upstream = self.removed_upstream

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "version": version,
                "source": source,
                "upstream_commit": upstream_commit,
                "up_to_date": up_to_date,
            }
        )
        if files is not UNSET:
            field_dict["files"] = files
        if license_ is not UNSET:
            field_dict["license"] = license_
        if removed_upstream is not UNSET:
            field_dict["removed_upstream"] = removed_upstream

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.agent_skill_file_diff import AgentSkillFileDiff
        from ..models.agent_skill_source import AgentSkillSource

        d = dict(src_dict)
        version = d.pop("version")

        source = AgentSkillSource.from_dict(d.pop("source"))

        upstream_commit = d.pop("upstream_commit")

        up_to_date = d.pop("up_to_date")

        _files = d.pop("files", UNSET)
        files: list[AgentSkillFileDiff] | Unset = UNSET
        if _files is not UNSET:
            files = []
            for files_item_data in _files:
                files_item = AgentSkillFileDiff.from_dict(files_item_data)

                files.append(files_item)

        license_ = d.pop("license", UNSET)

        removed_upstream = d.pop("removed_upstream", UNSET)

        agent_skill_upstream = cls(
            version=version,
            source=source,
            upstream_commit=upstream_commit,
            up_to_date=up_to_date,
            files=files,
            license_=license_,
            removed_upstream=removed_upstream,
        )

        agent_skill_upstream.additional_properties = d
        return agent_skill_upstream

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
