from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

T = TypeVar("T", bound="ModelRecommendationReportCatalog")


@_attrs_define
class ModelRecommendationReportCatalog:
    """
    Attributes:
        path (str | Unset): Empty over HTTP unless the built-in starter profiles are in use.
        tier (str | Unset):
        schema_version (int | Unset):
        as_of (str | Unset):
        current_release (str | Unset):
        notice (str | Unset):
    """

    path: str | Unset = UNSET
    tier: str | Unset = UNSET
    schema_version: int | Unset = UNSET
    as_of: str | Unset = UNSET
    current_release: str | Unset = UNSET
    notice: str | Unset = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        path = self.path

        tier = self.tier

        schema_version = self.schema_version

        as_of = self.as_of

        current_release = self.current_release

        notice = self.notice

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if path is not UNSET:
            field_dict["path"] = path
        if tier is not UNSET:
            field_dict["tier"] = tier
        if schema_version is not UNSET:
            field_dict["schema_version"] = schema_version
        if as_of is not UNSET:
            field_dict["as_of"] = as_of
        if current_release is not UNSET:
            field_dict["current_release"] = current_release
        if notice is not UNSET:
            field_dict["notice"] = notice

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        path = d.pop("path", UNSET)

        tier = d.pop("tier", UNSET)

        schema_version = d.pop("schema_version", UNSET)

        as_of = d.pop("as_of", UNSET)

        current_release = d.pop("current_release", UNSET)

        notice = d.pop("notice", UNSET)

        model_recommendation_report_catalog = cls(
            path=path,
            tier=tier,
            schema_version=schema_version,
            as_of=as_of,
            current_release=current_release,
            notice=notice,
        )

        model_recommendation_report_catalog.additional_properties = d
        return model_recommendation_report_catalog

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
