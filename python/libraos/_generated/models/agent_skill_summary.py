from __future__ import annotations

from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, TypeVar

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..models.agent_skill_summary_latest_status import AgentSkillSummaryLatestStatus
from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.agent_skill_source import AgentSkillSource


T = TypeVar("T", bound="AgentSkillSummary")


@_attrs_define
class AgentSkillSummary:
    """
    Attributes:
        name (str):
        description (str):
        latest_version (int):
        latest_status (AgentSkillSummaryLatestStatus):
        versions (int): Number of versions.
        source (AgentSkillSource):
        published_version (int | Unset): Highest published version; omitted when none is published.
        license_ (str | Unset):
    """

    name: str
    description: str
    latest_version: int
    latest_status: AgentSkillSummaryLatestStatus
    versions: int
    source: AgentSkillSource
    published_version: int | Unset = UNSET
    license_: str | Unset = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        name = self.name

        description = self.description

        latest_version = self.latest_version

        latest_status = self.latest_status.value

        versions = self.versions

        source = self.source.to_dict()

        published_version = self.published_version

        license_ = self.license_

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "name": name,
                "description": description,
                "latest_version": latest_version,
                "latest_status": latest_status,
                "versions": versions,
                "source": source,
            }
        )
        if published_version is not UNSET:
            field_dict["published_version"] = published_version
        if license_ is not UNSET:
            field_dict["license"] = license_

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.agent_skill_source import AgentSkillSource

        d = dict(src_dict)
        name = d.pop("name")

        description = d.pop("description")

        latest_version = d.pop("latest_version")

        latest_status = AgentSkillSummaryLatestStatus(d.pop("latest_status"))

        versions = d.pop("versions")

        source = AgentSkillSource.from_dict(d.pop("source"))

        published_version = d.pop("published_version", UNSET)

        license_ = d.pop("license", UNSET)

        agent_skill_summary = cls(
            name=name,
            description=description,
            latest_version=latest_version,
            latest_status=latest_status,
            versions=versions,
            source=source,
            published_version=published_version,
            license_=license_,
        )

        agent_skill_summary.additional_properties = d
        return agent_skill_summary

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
