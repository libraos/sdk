from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..models.model_recommendation_result_evidence_tier import ModelRecommendationResultEvidenceTier
from ..types import UNSET, Unset

T = TypeVar("T", bound="ModelRecommendationResultEvidence")


@_attrs_define
class ModelRecommendationResultEvidence:
    """
    Attributes:
        tier (ModelRecommendationResultEvidenceTier | Unset):
        stale (bool | Unset):
        stale_reason (str | Unset):
        date (str | Unset):
        libraos (str | Unset):
    """

    tier: ModelRecommendationResultEvidenceTier | Unset = UNSET
    stale: bool | Unset = UNSET
    stale_reason: str | Unset = UNSET
    date: str | Unset = UNSET
    libraos: str | Unset = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        tier: str | Unset = UNSET
        if not isinstance(self.tier, Unset):
            tier = self.tier.value

        stale = self.stale

        stale_reason = self.stale_reason

        date = self.date

        libraos = self.libraos

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if tier is not UNSET:
            field_dict["tier"] = tier
        if stale is not UNSET:
            field_dict["stale"] = stale
        if stale_reason is not UNSET:
            field_dict["stale_reason"] = stale_reason
        if date is not UNSET:
            field_dict["date"] = date
        if libraos is not UNSET:
            field_dict["libraos"] = libraos

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        _tier = d.pop("tier", UNSET)
        tier: ModelRecommendationResultEvidenceTier | Unset
        if isinstance(_tier, Unset):
            tier = UNSET
        else:
            tier = ModelRecommendationResultEvidenceTier(_tier)

        stale = d.pop("stale", UNSET)

        stale_reason = d.pop("stale_reason", UNSET)

        date = d.pop("date", UNSET)

        libraos = d.pop("libraos", UNSET)

        model_recommendation_result_evidence = cls(
            tier=tier,
            stale=stale,
            stale_reason=stale_reason,
            date=date,
            libraos=libraos,
        )

        model_recommendation_result_evidence.additional_properties = d
        return model_recommendation_result_evidence

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
