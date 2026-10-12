from __future__ import annotations

from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, TypeVar, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..models.model_recommendation_result_compatibility import ModelRecommendationResultCompatibility
from ..models.model_recommendation_result_matched_by import ModelRecommendationResultMatchedBy
from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.model_recommendation_result_evidence import ModelRecommendationResultEvidence
    from ..models.model_recommendation_result_figures import ModelRecommendationResultFigures
    from ..models.model_recommendation_result_measured import ModelRecommendationResultMeasured
    from ..models.model_recommendation_result_preference import ModelRecommendationResultPreference
    from ..models.model_recommendation_result_serving import ModelRecommendationResultServing
    from ..models.model_recommendation_result_settings_item import ModelRecommendationResultSettingsItem


T = TypeVar("T", bound="ModelRecommendationResult")


@_attrs_define
class ModelRecommendationResult:
    """
    Attributes:
        cell_id (str):
        model (str):
        hardware (str):
        task (str):
        compatibility (ModelRecommendationResultCompatibility):
        reasons (list[str]):
        evidence (ModelRecommendationResultEvidence):
        preference (ModelRecommendationResultPreference):
        matched_by (ModelRecommendationResultMatchedBy):
        served_name (str | Unset):
        hardware_label (str | Unset):
        task_label (str | Unset):
        status (str | Unset):
        status_text (str | Unset):
        dependencies (list[str] | Unset):
        settings (list[ModelRecommendationResultSettingsItem] | Unset):
        red_flags (list[str] | Unset):
        licence_notes (list[str] | Unset):
        served_locally (bool | Unset):
        measured (ModelRecommendationResultMeasured | Unset): Measured figures; present only on a `validated_match` from
            the scored catalog.
        figures (ModelRecommendationResultFigures | Unset): Catalog figures; present only on a `validated_match` from
            the scored catalog.
        serving (ModelRecommendationResultServing | Unset): Serving recipe (`engine`, `recipe`, `image`, `flags`).
    """

    cell_id: str
    model: str
    hardware: str
    task: str
    compatibility: ModelRecommendationResultCompatibility
    reasons: list[str]
    evidence: ModelRecommendationResultEvidence
    preference: ModelRecommendationResultPreference
    matched_by: ModelRecommendationResultMatchedBy
    served_name: str | Unset = UNSET
    hardware_label: str | Unset = UNSET
    task_label: str | Unset = UNSET
    status: str | Unset = UNSET
    status_text: str | Unset = UNSET
    dependencies: list[str] | Unset = UNSET
    settings: list[ModelRecommendationResultSettingsItem] | Unset = UNSET
    red_flags: list[str] | Unset = UNSET
    licence_notes: list[str] | Unset = UNSET
    served_locally: bool | Unset = UNSET
    measured: ModelRecommendationResultMeasured | Unset = UNSET
    figures: ModelRecommendationResultFigures | Unset = UNSET
    serving: ModelRecommendationResultServing | Unset = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        cell_id = self.cell_id

        model = self.model

        hardware = self.hardware

        task = self.task

        compatibility = self.compatibility.value

        reasons = self.reasons

        evidence = self.evidence.to_dict()

        preference = self.preference.to_dict()

        matched_by = self.matched_by.value

        served_name = self.served_name

        hardware_label = self.hardware_label

        task_label = self.task_label

        status = self.status

        status_text = self.status_text

        dependencies: list[str] | Unset = UNSET
        if not isinstance(self.dependencies, Unset):
            dependencies = self.dependencies

        settings: list[dict[str, Any]] | Unset = UNSET
        if not isinstance(self.settings, Unset):
            settings = []
            for settings_item_data in self.settings:
                settings_item = settings_item_data.to_dict()
                settings.append(settings_item)

        red_flags: list[str] | Unset = UNSET
        if not isinstance(self.red_flags, Unset):
            red_flags = self.red_flags

        licence_notes: list[str] | Unset = UNSET
        if not isinstance(self.licence_notes, Unset):
            licence_notes = self.licence_notes

        served_locally = self.served_locally

        measured: dict[str, Any] | Unset = UNSET
        if not isinstance(self.measured, Unset):
            measured = self.measured.to_dict()

        figures: dict[str, Any] | Unset = UNSET
        if not isinstance(self.figures, Unset):
            figures = self.figures.to_dict()

        serving: dict[str, Any] | Unset = UNSET
        if not isinstance(self.serving, Unset):
            serving = self.serving.to_dict()

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "cell_id": cell_id,
                "model": model,
                "hardware": hardware,
                "task": task,
                "compatibility": compatibility,
                "reasons": reasons,
                "evidence": evidence,
                "preference": preference,
                "matched_by": matched_by,
            }
        )
        if served_name is not UNSET:
            field_dict["served_name"] = served_name
        if hardware_label is not UNSET:
            field_dict["hardware_label"] = hardware_label
        if task_label is not UNSET:
            field_dict["task_label"] = task_label
        if status is not UNSET:
            field_dict["status"] = status
        if status_text is not UNSET:
            field_dict["status_text"] = status_text
        if dependencies is not UNSET:
            field_dict["dependencies"] = dependencies
        if settings is not UNSET:
            field_dict["settings"] = settings
        if red_flags is not UNSET:
            field_dict["red_flags"] = red_flags
        if licence_notes is not UNSET:
            field_dict["licence_notes"] = licence_notes
        if served_locally is not UNSET:
            field_dict["served_locally"] = served_locally
        if measured is not UNSET:
            field_dict["measured"] = measured
        if figures is not UNSET:
            field_dict["figures"] = figures
        if serving is not UNSET:
            field_dict["serving"] = serving

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.model_recommendation_result_evidence import ModelRecommendationResultEvidence
        from ..models.model_recommendation_result_figures import ModelRecommendationResultFigures
        from ..models.model_recommendation_result_measured import ModelRecommendationResultMeasured
        from ..models.model_recommendation_result_preference import ModelRecommendationResultPreference
        from ..models.model_recommendation_result_serving import ModelRecommendationResultServing
        from ..models.model_recommendation_result_settings_item import ModelRecommendationResultSettingsItem

        d = dict(src_dict)
        cell_id = d.pop("cell_id")

        model = d.pop("model")

        hardware = d.pop("hardware")

        task = d.pop("task")

        compatibility = ModelRecommendationResultCompatibility(d.pop("compatibility"))

        reasons = cast(list[str], d.pop("reasons"))

        evidence = ModelRecommendationResultEvidence.from_dict(d.pop("evidence"))

        preference = ModelRecommendationResultPreference.from_dict(d.pop("preference"))

        matched_by = ModelRecommendationResultMatchedBy(d.pop("matched_by"))

        served_name = d.pop("served_name", UNSET)

        hardware_label = d.pop("hardware_label", UNSET)

        task_label = d.pop("task_label", UNSET)

        status = d.pop("status", UNSET)

        status_text = d.pop("status_text", UNSET)

        dependencies = cast(list[str], d.pop("dependencies", UNSET))

        _settings = d.pop("settings", UNSET)
        settings: list[ModelRecommendationResultSettingsItem] | Unset = UNSET
        if _settings is not UNSET:
            settings = []
            for settings_item_data in _settings:
                settings_item = ModelRecommendationResultSettingsItem.from_dict(settings_item_data)

                settings.append(settings_item)

        red_flags = cast(list[str], d.pop("red_flags", UNSET))

        licence_notes = cast(list[str], d.pop("licence_notes", UNSET))

        served_locally = d.pop("served_locally", UNSET)

        _measured = d.pop("measured", UNSET)
        measured: ModelRecommendationResultMeasured | Unset
        if isinstance(_measured, Unset):
            measured = UNSET
        else:
            measured = ModelRecommendationResultMeasured.from_dict(_measured)

        _figures = d.pop("figures", UNSET)
        figures: ModelRecommendationResultFigures | Unset
        if isinstance(_figures, Unset):
            figures = UNSET
        else:
            figures = ModelRecommendationResultFigures.from_dict(_figures)

        _serving = d.pop("serving", UNSET)
        serving: ModelRecommendationResultServing | Unset
        if isinstance(_serving, Unset):
            serving = UNSET
        else:
            serving = ModelRecommendationResultServing.from_dict(_serving)

        model_recommendation_result = cls(
            cell_id=cell_id,
            model=model,
            hardware=hardware,
            task=task,
            compatibility=compatibility,
            reasons=reasons,
            evidence=evidence,
            preference=preference,
            matched_by=matched_by,
            served_name=served_name,
            hardware_label=hardware_label,
            task_label=task_label,
            status=status,
            status_text=status_text,
            dependencies=dependencies,
            settings=settings,
            red_flags=red_flags,
            licence_notes=licence_notes,
            served_locally=served_locally,
            measured=measured,
            figures=figures,
            serving=serving,
        )

        model_recommendation_result.additional_properties = d
        return model_recommendation_result

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
