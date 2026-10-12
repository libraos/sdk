from __future__ import annotations

from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, TypeVar

from attrs import define as _attrs_define
from attrs import field as _attrs_field

if TYPE_CHECKING:
    from ..models.agent_skill_file_diff import AgentSkillFileDiff


T = TypeVar("T", bound="AgentSkillDiff")


@_attrs_define
class AgentSkillDiff:
    """
    Attributes:
        from_ (int):
        to (int):
        files (list[AgentSkillFileDiff]): Changed files only; empty when the versions are identical.
    """

    from_: int
    to: int
    files: list[AgentSkillFileDiff]
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        from_ = self.from_

        to = self.to

        files = []
        for files_item_data in self.files:
            files_item = files_item_data.to_dict()
            files.append(files_item)

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "from": from_,
                "to": to,
                "files": files,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.agent_skill_file_diff import AgentSkillFileDiff

        d = dict(src_dict)
        from_ = d.pop("from")

        to = d.pop("to")

        files = []
        _files = d.pop("files")
        for files_item_data in _files:
            files_item = AgentSkillFileDiff.from_dict(files_item_data)

            files.append(files_item)

        agent_skill_diff = cls(
            from_=from_,
            to=to,
            files=files,
        )

        agent_skill_diff.additional_properties = d
        return agent_skill_diff

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
