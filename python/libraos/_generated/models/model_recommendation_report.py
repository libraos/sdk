from __future__ import annotations

from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, TypeVar, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.model_recommendation_report_catalog import ModelRecommendationReportCatalog
    from ..models.model_recommendation_report_environment import ModelRecommendationReportEnvironment
    from ..models.model_recommendation_report_verification import ModelRecommendationReportVerification
    from ..models.model_recommendation_result import ModelRecommendationResult


T = TypeVar("T", bound="ModelRecommendationReport")


@_attrs_define
class ModelRecommendationReport:
    """
    Attributes:
        catalog (ModelRecommendationReportCatalog):
        verification (ModelRecommendationReportVerification):
        environment (ModelRecommendationReportEnvironment): The detected host (`os`, `arch`, `libraos_version`,
            `ram_gib`, `gpu`, `inference`, `embeddings`). Endpoint addresses are removed.
        results (list[ModelRecommendationResult]):
        task (str | Unset):
        warnings (list[str] | Unset):
    """

    catalog: ModelRecommendationReportCatalog
    verification: ModelRecommendationReportVerification
    environment: ModelRecommendationReportEnvironment
    results: list[ModelRecommendationResult]
    task: str | Unset = UNSET
    warnings: list[str] | Unset = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        catalog = self.catalog.to_dict()

        verification = self.verification.to_dict()

        environment = self.environment.to_dict()

        results = []
        for results_item_data in self.results:
            results_item = results_item_data.to_dict()
            results.append(results_item)

        task = self.task

        warnings: list[str] | Unset = UNSET
        if not isinstance(self.warnings, Unset):
            warnings = self.warnings

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "catalog": catalog,
                "verification": verification,
                "environment": environment,
                "results": results,
            }
        )
        if task is not UNSET:
            field_dict["task"] = task
        if warnings is not UNSET:
            field_dict["warnings"] = warnings

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.model_recommendation_report_catalog import ModelRecommendationReportCatalog
        from ..models.model_recommendation_report_environment import ModelRecommendationReportEnvironment
        from ..models.model_recommendation_report_verification import ModelRecommendationReportVerification
        from ..models.model_recommendation_result import ModelRecommendationResult

        d = dict(src_dict)
        catalog = ModelRecommendationReportCatalog.from_dict(d.pop("catalog"))

        verification = ModelRecommendationReportVerification.from_dict(d.pop("verification"))

        environment = ModelRecommendationReportEnvironment.from_dict(d.pop("environment"))

        results = []
        _results = d.pop("results")
        for results_item_data in _results:
            results_item = ModelRecommendationResult.from_dict(results_item_data)

            results.append(results_item)

        task = d.pop("task", UNSET)

        warnings = cast(list[str], d.pop("warnings", UNSET))

        model_recommendation_report = cls(
            catalog=catalog,
            verification=verification,
            environment=environment,
            results=results,
            task=task,
            warnings=warnings,
        )

        model_recommendation_report.additional_properties = d
        return model_recommendation_report

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
