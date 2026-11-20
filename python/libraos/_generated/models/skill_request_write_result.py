from __future__ import annotations

from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, TypeVar

from attrs import define as _attrs_define
from attrs import field as _attrs_field

if TYPE_CHECKING:
    from ..models.skill_request import SkillRequest


T = TypeVar("T", bound="SkillRequestWriteResult")


@_attrs_define
class SkillRequestWriteResult:
    """
    Attributes:
        request (SkillRequest): One person's request for a skill from a GitHub link.
        created (bool): False when the caller already had a pending request for the same link, which is returned
            instead.
    """

    request: SkillRequest
    created: bool
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        request = self.request.to_dict()

        created = self.created

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "request": request,
                "created": created,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.skill_request import SkillRequest

        d = dict(src_dict)
        request = SkillRequest.from_dict(d.pop("request"))

        created = d.pop("created")

        skill_request_write_result = cls(
            request=request,
            created=created,
        )

        skill_request_write_result.additional_properties = d
        return skill_request_write_result

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
