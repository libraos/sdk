from __future__ import annotations

from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, TypeVar

from attrs import define as _attrs_define
from attrs import field as _attrs_field

if TYPE_CHECKING:
    from ..models.agent_skill_files_files import AgentSkillFilesFiles


T = TypeVar("T", bound="AgentSkillFiles")


@_attrs_define
class AgentSkillFiles:
    """
    Attributes:
        files (AgentSkillFilesFiles): Path to text content. Must include `SKILL.md` with `name` and `description`
            frontmatter; at most 200 other files and 4 MiB in total, clean relative paths, UTF-8 text.
    """

    files: AgentSkillFilesFiles
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        files = self.files.to_dict()

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "files": files,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.agent_skill_files_files import AgentSkillFilesFiles

        d = dict(src_dict)
        files = AgentSkillFilesFiles.from_dict(d.pop("files"))

        agent_skill_files = cls(
            files=files,
        )

        agent_skill_files.additional_properties = d
        return agent_skill_files

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
