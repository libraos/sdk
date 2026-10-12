from __future__ import annotations

from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, TypeVar

from attrs import define as _attrs_define
from attrs import field as _attrs_field

if TYPE_CHECKING:
    from ..models.decision_version import DecisionVersion


T = TypeVar("T", bound="DecisionModel")


@_attrs_define
class DecisionModel:
    """
    Attributes:
        name (str):
        versions (list[DecisionVersion]): Newest first.
    """

    name: str
    versions: list[DecisionVersion]
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        name = self.name

        versions = []
        for versions_item_data in self.versions:
            versions_item = versions_item_data.to_dict()
            versions.append(versions_item)

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "name": name,
                "versions": versions,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.decision_version import DecisionVersion

        d = dict(src_dict)
        name = d.pop("name")

        versions = []
        _versions = d.pop("versions")
        for versions_item_data in _versions:
            versions_item = DecisionVersion.from_dict(versions_item_data)

            versions.append(versions_item)

        decision_model = cls(
            name=name,
            versions=versions,
        )

        decision_model.additional_properties = d
        return decision_model

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
