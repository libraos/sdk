from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

T = TypeVar("T", bound="DecisionPredictionOod")


@_attrs_define
class DecisionPredictionOod:
    """Corpus-drift signals (present when the version carries them). Not a per-request out-of-distribution detector.

    Attributes:
        oov_mass (float | Unset):
        centroid_cos (float | Unset):
    """

    oov_mass: float | Unset = UNSET
    centroid_cos: float | Unset = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        oov_mass = self.oov_mass

        centroid_cos = self.centroid_cos

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if oov_mass is not UNSET:
            field_dict["oov_mass"] = oov_mass
        if centroid_cos is not UNSET:
            field_dict["centroid_cos"] = centroid_cos

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        oov_mass = d.pop("oov_mass", UNSET)

        centroid_cos = d.pop("centroid_cos", UNSET)

        decision_prediction_ood = cls(
            oov_mass=oov_mass,
            centroid_cos=centroid_cos,
        )

        decision_prediction_ood.additional_properties = d
        return decision_prediction_ood

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
