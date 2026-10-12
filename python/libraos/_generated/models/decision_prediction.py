from __future__ import annotations

from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, TypeVar

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.decision_prediction_distribution import DecisionPredictionDistribution
    from ..models.decision_prediction_ood import DecisionPredictionOod


T = TypeVar("T", bound="DecisionPrediction")


@_attrs_define
class DecisionPrediction:
    """
    Attributes:
        label (str):
        confidence (float): Calibrated probability of `label`. Compare with the version's `report.gate`.
        distribution (DecisionPredictionDistribution):
        ood (DecisionPredictionOod | Unset): Corpus-drift signals (present when the version carries them). Not a per-
            request out-of-distribution detector.
    """

    label: str
    confidence: float
    distribution: DecisionPredictionDistribution
    ood: DecisionPredictionOod | Unset = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        label = self.label

        confidence = self.confidence

        distribution = self.distribution.to_dict()

        ood: dict[str, Any] | Unset = UNSET
        if not isinstance(self.ood, Unset):
            ood = self.ood.to_dict()

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "label": label,
                "confidence": confidence,
                "distribution": distribution,
            }
        )
        if ood is not UNSET:
            field_dict["ood"] = ood

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.decision_prediction_distribution import DecisionPredictionDistribution
        from ..models.decision_prediction_ood import DecisionPredictionOod

        d = dict(src_dict)
        label = d.pop("label")

        confidence = d.pop("confidence")

        distribution = DecisionPredictionDistribution.from_dict(d.pop("distribution"))

        _ood = d.pop("ood", UNSET)
        ood: DecisionPredictionOod | Unset
        if isinstance(_ood, Unset):
            ood = UNSET
        else:
            ood = DecisionPredictionOod.from_dict(_ood)

        decision_prediction = cls(
            label=label,
            confidence=confidence,
            distribution=distribution,
            ood=ood,
        )

        decision_prediction.additional_properties = d
        return decision_prediction

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
