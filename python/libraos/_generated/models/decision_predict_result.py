from __future__ import annotations

from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, TypeVar

from attrs import define as _attrs_define
from attrs import field as _attrs_field

if TYPE_CHECKING:
    from ..models.decision_prediction import DecisionPrediction


T = TypeVar("T", bound="DecisionPredictResult")


@_attrs_define
class DecisionPredictResult:
    """
    Attributes:
        name (str):
        model_version (int):
        results (list[DecisionPrediction]): In the order of `texts`.
    """

    name: str
    model_version: int
    results: list[DecisionPrediction]
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        name = self.name

        model_version = self.model_version

        results = []
        for results_item_data in self.results:
            results_item = results_item_data.to_dict()
            results.append(results_item)

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "name": name,
                "model_version": model_version,
                "results": results,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.decision_prediction import DecisionPrediction

        d = dict(src_dict)
        name = d.pop("name")

        model_version = d.pop("model_version")

        results = []
        _results = d.pop("results")
        for results_item_data in _results:
            results_item = DecisionPrediction.from_dict(results_item_data)

            results.append(results_item)

        decision_predict_result = cls(
            name=name,
            model_version=model_version,
            results=results,
        )

        decision_predict_result.additional_properties = d
        return decision_predict_result

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
