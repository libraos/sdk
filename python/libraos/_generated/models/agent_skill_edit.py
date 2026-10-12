from __future__ import annotations

from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, TypeVar

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.agent_skill_edit_files import AgentSkillEditFiles


T = TypeVar("T", bound="AgentSkillEdit")


@_attrs_define
class AgentSkillEdit:
    """
    Attributes:
        files (AgentSkillEditFiles): The full file set; `SKILL.md` frontmatter `name` must equal the path name.
        base_version (int | Unset): Version this edit is based on. The new version keeps its source and licence and
            records `forked_from`.
    """

    files: AgentSkillEditFiles
    base_version: int | Unset = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        files = self.files.to_dict()

        base_version = self.base_version

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "files": files,
            }
        )
        if base_version is not UNSET:
            field_dict["base_version"] = base_version

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.agent_skill_edit_files import AgentSkillEditFiles

        d = dict(src_dict)
        files = AgentSkillEditFiles.from_dict(d.pop("files"))

        base_version = d.pop("base_version", UNSET)

        agent_skill_edit = cls(
            files=files,
            base_version=base_version,
        )

        agent_skill_edit.additional_properties = d
        return agent_skill_edit

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
