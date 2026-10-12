from __future__ import annotations

import datetime
from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, TypeVar, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field
from dateutil.parser import isoparse

from ..models.agent_skill_version_status import AgentSkillVersionStatus
from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.agent_skill_source import AgentSkillSource
    from ..models.agent_skill_version_files import AgentSkillVersionFiles


T = TypeVar("T", bound="AgentSkillVersion")


@_attrs_define
class AgentSkillVersion:
    """
    Attributes:
        name (str):
        version (int):
        description (str):
        sha256 (str):
        source (AgentSkillSource):
        status (AgentSkillVersionStatus):
        created_at (datetime.datetime):
        license_ (str | Unset):
        forked_from (int | Unset): The version this edit was based on.
        created_by (str | Unset):
        status_by (str | Unset):
        status_at (datetime.datetime | Unset):
        file_list (list[str] | Unset): Files other than `SKILL.md`, sorted. May be null when there are none.
        files (AgentSkillVersionFiles | Unset): Path to text content, `SKILL.md` included. Only on single-version reads.
    """

    name: str
    version: int
    description: str
    sha256: str
    source: AgentSkillSource
    status: AgentSkillVersionStatus
    created_at: datetime.datetime
    license_: str | Unset = UNSET
    forked_from: int | Unset = UNSET
    created_by: str | Unset = UNSET
    status_by: str | Unset = UNSET
    status_at: datetime.datetime | Unset = UNSET
    file_list: list[str] | Unset = UNSET
    files: AgentSkillVersionFiles | Unset = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        name = self.name

        version = self.version

        description = self.description

        sha256 = self.sha256

        source = self.source.to_dict()

        status = self.status.value

        created_at = self.created_at.isoformat()

        license_ = self.license_

        forked_from = self.forked_from

        created_by = self.created_by

        status_by = self.status_by

        status_at: str | Unset = UNSET
        if not isinstance(self.status_at, Unset):
            status_at = self.status_at.isoformat()

        file_list: list[str] | Unset = UNSET
        if not isinstance(self.file_list, Unset):
            file_list = self.file_list

        files: dict[str, Any] | Unset = UNSET
        if not isinstance(self.files, Unset):
            files = self.files.to_dict()

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "name": name,
                "version": version,
                "description": description,
                "sha256": sha256,
                "source": source,
                "status": status,
                "created_at": created_at,
            }
        )
        if license_ is not UNSET:
            field_dict["license"] = license_
        if forked_from is not UNSET:
            field_dict["forked_from"] = forked_from
        if created_by is not UNSET:
            field_dict["created_by"] = created_by
        if status_by is not UNSET:
            field_dict["status_by"] = status_by
        if status_at is not UNSET:
            field_dict["status_at"] = status_at
        if file_list is not UNSET:
            field_dict["file_list"] = file_list
        if files is not UNSET:
            field_dict["files"] = files

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.agent_skill_source import AgentSkillSource
        from ..models.agent_skill_version_files import AgentSkillVersionFiles

        d = dict(src_dict)
        name = d.pop("name")

        version = d.pop("version")

        description = d.pop("description")

        sha256 = d.pop("sha256")

        source = AgentSkillSource.from_dict(d.pop("source"))

        status = AgentSkillVersionStatus(d.pop("status"))

        created_at = isoparse(d.pop("created_at"))

        license_ = d.pop("license", UNSET)

        forked_from = d.pop("forked_from", UNSET)

        created_by = d.pop("created_by", UNSET)

        status_by = d.pop("status_by", UNSET)

        _status_at = d.pop("status_at", UNSET)
        status_at: datetime.datetime | Unset
        if isinstance(_status_at, Unset):
            status_at = UNSET
        else:
            status_at = isoparse(_status_at)

        file_list = cast(list[str], d.pop("file_list", UNSET))

        _files = d.pop("files", UNSET)
        files: AgentSkillVersionFiles | Unset
        if isinstance(_files, Unset):
            files = UNSET
        else:
            files = AgentSkillVersionFiles.from_dict(_files)

        agent_skill_version = cls(
            name=name,
            version=version,
            description=description,
            sha256=sha256,
            source=source,
            status=status,
            created_at=created_at,
            license_=license_,
            forked_from=forked_from,
            created_by=created_by,
            status_by=status_by,
            status_at=status_at,
            file_list=file_list,
            files=files,
        )

        agent_skill_version.additional_properties = d
        return agent_skill_version

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
