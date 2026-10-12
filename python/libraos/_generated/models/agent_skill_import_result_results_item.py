from __future__ import annotations

from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, TypeVar

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.agent_skill_version import AgentSkillVersion


T = TypeVar("T", bound="AgentSkillImportResultResultsItem")


@_attrs_define
class AgentSkillImportResultResultsItem:
    """
    Attributes:
        path (str):
        created (bool):
        name (str | Unset):
        version (AgentSkillVersion | Unset):
        error (str | Unset):
    """

    path: str
    created: bool
    name: str | Unset = UNSET
    version: AgentSkillVersion | Unset = UNSET
    error: str | Unset = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        path = self.path

        created = self.created

        name = self.name

        version: dict[str, Any] | Unset = UNSET
        if not isinstance(self.version, Unset):
            version = self.version.to_dict()

        error = self.error

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "path": path,
                "created": created,
            }
        )
        if name is not UNSET:
            field_dict["name"] = name
        if version is not UNSET:
            field_dict["version"] = version
        if error is not UNSET:
            field_dict["error"] = error

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.agent_skill_version import AgentSkillVersion

        d = dict(src_dict)
        path = d.pop("path")

        created = d.pop("created")

        name = d.pop("name", UNSET)

        _version = d.pop("version", UNSET)
        version: AgentSkillVersion | Unset
        if isinstance(_version, Unset):
            version = UNSET
        else:
            version = AgentSkillVersion.from_dict(_version)

        error = d.pop("error", UNSET)

        agent_skill_import_result_results_item = cls(
            path=path,
            created=created,
            name=name,
            version=version,
            error=error,
        )

        agent_skill_import_result_results_item.additional_properties = d
        return agent_skill_import_result_results_item

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
