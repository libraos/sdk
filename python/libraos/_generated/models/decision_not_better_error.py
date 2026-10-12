from __future__ import annotations

from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, TypeVar

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..models.decision_not_better_error_error import DecisionNotBetterErrorError

if TYPE_CHECKING:
    from ..models.decision_report import DecisionReport


T = TypeVar("T", bound="DecisionNotBetterError")


@_attrs_define
class DecisionNotBetterError:
    """
    Attributes:
        error (DecisionNotBetterErrorError):
        message (str):
        report (DecisionReport): Held-out evaluation of a trained version.
    """

    error: DecisionNotBetterErrorError
    message: str
    report: DecisionReport
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        error = self.error.value

        message = self.message

        report = self.report.to_dict()

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "error": error,
                "message": message,
                "report": report,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.decision_report import DecisionReport

        d = dict(src_dict)
        error = DecisionNotBetterErrorError(d.pop("error"))

        message = d.pop("message")

        report = DecisionReport.from_dict(d.pop("report"))

        decision_not_better_error = cls(
            error=error,
            message=message,
            report=report,
        )

        decision_not_better_error.additional_properties = d
        return decision_not_better_error

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
