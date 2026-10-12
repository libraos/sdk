from __future__ import annotations

from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, TypeVar, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.decision_report_n_per_label import DecisionReportNPerLabel
    from ..models.decision_report_recall_per_label import DecisionReportRecallPerLabel


T = TypeVar("T", bound="DecisionReport")


@_attrs_define
class DecisionReport:
    """Held-out evaluation of a trained version.

    Attributes:
        labels (list[str] | Unset):
        n_train (int | Unset):
        n_calibrate (int | Unset):
        n_test (int | Unset):
        n_per_label (DecisionReportNPerLabel | Unset):
        gate (float | Unset): Confidence at or above which a prediction should be trusted.
        temperature (float | Unset): Calibration temperature.
        acc (float | Unset):
        ece (float | Unset): Expected calibration error.
        coverage (float | Unset): Share of test rows at or above the gate.
        acc_above_gate (float | Unset):
        acc_below_gate (float | Unset):
        n_above_gate (int | Unset):
        recall_per_label (DecisionReportRecallPerLabel | Unset):
        majority_share (float | Unset): Share of the most common label (the prior a model must beat).
        acc_above_gate_lower (float | Unset): 95% Wilson lower bound of the above-gate accuracy.
        control_above_gate (int | Unset): Shuffled-label control, rows above the gate (report only).
        control_acc_above_gate (float | Unset):
    """

    labels: list[str] | Unset = UNSET
    n_train: int | Unset = UNSET
    n_calibrate: int | Unset = UNSET
    n_test: int | Unset = UNSET
    n_per_label: DecisionReportNPerLabel | Unset = UNSET
    gate: float | Unset = UNSET
    temperature: float | Unset = UNSET
    acc: float | Unset = UNSET
    ece: float | Unset = UNSET
    coverage: float | Unset = UNSET
    acc_above_gate: float | Unset = UNSET
    acc_below_gate: float | Unset = UNSET
    n_above_gate: int | Unset = UNSET
    recall_per_label: DecisionReportRecallPerLabel | Unset = UNSET
    majority_share: float | Unset = UNSET
    acc_above_gate_lower: float | Unset = UNSET
    control_above_gate: int | Unset = UNSET
    control_acc_above_gate: float | Unset = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        labels: list[str] | Unset = UNSET
        if not isinstance(self.labels, Unset):
            labels = self.labels

        n_train = self.n_train

        n_calibrate = self.n_calibrate

        n_test = self.n_test

        n_per_label: dict[str, Any] | Unset = UNSET
        if not isinstance(self.n_per_label, Unset):
            n_per_label = self.n_per_label.to_dict()

        gate = self.gate

        temperature = self.temperature

        acc = self.acc

        ece = self.ece

        coverage = self.coverage

        acc_above_gate = self.acc_above_gate

        acc_below_gate = self.acc_below_gate

        n_above_gate = self.n_above_gate

        recall_per_label: dict[str, Any] | Unset = UNSET
        if not isinstance(self.recall_per_label, Unset):
            recall_per_label = self.recall_per_label.to_dict()

        majority_share = self.majority_share

        acc_above_gate_lower = self.acc_above_gate_lower

        control_above_gate = self.control_above_gate

        control_acc_above_gate = self.control_acc_above_gate

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if labels is not UNSET:
            field_dict["labels"] = labels
        if n_train is not UNSET:
            field_dict["n_train"] = n_train
        if n_calibrate is not UNSET:
            field_dict["n_calibrate"] = n_calibrate
        if n_test is not UNSET:
            field_dict["n_test"] = n_test
        if n_per_label is not UNSET:
            field_dict["n_per_label"] = n_per_label
        if gate is not UNSET:
            field_dict["gate"] = gate
        if temperature is not UNSET:
            field_dict["temperature"] = temperature
        if acc is not UNSET:
            field_dict["acc"] = acc
        if ece is not UNSET:
            field_dict["ece"] = ece
        if coverage is not UNSET:
            field_dict["coverage"] = coverage
        if acc_above_gate is not UNSET:
            field_dict["acc_above_gate"] = acc_above_gate
        if acc_below_gate is not UNSET:
            field_dict["acc_below_gate"] = acc_below_gate
        if n_above_gate is not UNSET:
            field_dict["n_above_gate"] = n_above_gate
        if recall_per_label is not UNSET:
            field_dict["recall_per_label"] = recall_per_label
        if majority_share is not UNSET:
            field_dict["majority_share"] = majority_share
        if acc_above_gate_lower is not UNSET:
            field_dict["acc_above_gate_lower"] = acc_above_gate_lower
        if control_above_gate is not UNSET:
            field_dict["control_above_gate"] = control_above_gate
        if control_acc_above_gate is not UNSET:
            field_dict["control_acc_above_gate"] = control_acc_above_gate

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.decision_report_n_per_label import DecisionReportNPerLabel
        from ..models.decision_report_recall_per_label import DecisionReportRecallPerLabel

        d = dict(src_dict)
        labels = cast(list[str], d.pop("labels", UNSET))

        n_train = d.pop("n_train", UNSET)

        n_calibrate = d.pop("n_calibrate", UNSET)

        n_test = d.pop("n_test", UNSET)

        _n_per_label = d.pop("n_per_label", UNSET)
        n_per_label: DecisionReportNPerLabel | Unset
        if isinstance(_n_per_label, Unset):
            n_per_label = UNSET
        else:
            n_per_label = DecisionReportNPerLabel.from_dict(_n_per_label)

        gate = d.pop("gate", UNSET)

        temperature = d.pop("temperature", UNSET)

        acc = d.pop("acc", UNSET)

        ece = d.pop("ece", UNSET)

        coverage = d.pop("coverage", UNSET)

        acc_above_gate = d.pop("acc_above_gate", UNSET)

        acc_below_gate = d.pop("acc_below_gate", UNSET)

        n_above_gate = d.pop("n_above_gate", UNSET)

        _recall_per_label = d.pop("recall_per_label", UNSET)
        recall_per_label: DecisionReportRecallPerLabel | Unset
        if isinstance(_recall_per_label, Unset):
            recall_per_label = UNSET
        else:
            recall_per_label = DecisionReportRecallPerLabel.from_dict(_recall_per_label)

        majority_share = d.pop("majority_share", UNSET)

        acc_above_gate_lower = d.pop("acc_above_gate_lower", UNSET)

        control_above_gate = d.pop("control_above_gate", UNSET)

        control_acc_above_gate = d.pop("control_acc_above_gate", UNSET)

        decision_report = cls(
            labels=labels,
            n_train=n_train,
            n_calibrate=n_calibrate,
            n_test=n_test,
            n_per_label=n_per_label,
            gate=gate,
            temperature=temperature,
            acc=acc,
            ece=ece,
            coverage=coverage,
            acc_above_gate=acc_above_gate,
            acc_below_gate=acc_below_gate,
            n_above_gate=n_above_gate,
            recall_per_label=recall_per_label,
            majority_share=majority_share,
            acc_above_gate_lower=acc_above_gate_lower,
            control_above_gate=control_above_gate,
            control_acc_above_gate=control_acc_above_gate,
        )

        decision_report.additional_properties = d
        return decision_report

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
