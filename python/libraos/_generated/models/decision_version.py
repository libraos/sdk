from __future__ import annotations

import datetime
from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, TypeVar, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field
from dateutil.parser import isoparse

from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.decision_report import DecisionReport


T = TypeVar("T", bound="DecisionVersion")


@_attrs_define
class DecisionVersion:
    """
    Attributes:
        name (str):
        version (int):
        labels (list[str]):
        report (DecisionReport): Held-out evaluation of a trained version.
        active (bool):
        created_at (datetime.datetime):
        created_by (str | Unset):
        activated_at (datetime.datetime | Unset):
    """

    name: str
    version: int
    labels: list[str]
    report: DecisionReport
    active: bool
    created_at: datetime.datetime
    created_by: str | Unset = UNSET
    activated_at: datetime.datetime | Unset = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        name = self.name

        version = self.version

        labels = self.labels

        report = self.report.to_dict()

        active = self.active

        created_at = self.created_at.isoformat()

        created_by = self.created_by

        activated_at: str | Unset = UNSET
        if not isinstance(self.activated_at, Unset):
            activated_at = self.activated_at.isoformat()

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "name": name,
                "version": version,
                "labels": labels,
                "report": report,
                "active": active,
                "created_at": created_at,
            }
        )
        if created_by is not UNSET:
            field_dict["created_by"] = created_by
        if activated_at is not UNSET:
            field_dict["activated_at"] = activated_at

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.decision_report import DecisionReport

        d = dict(src_dict)
        name = d.pop("name")

        version = d.pop("version")

        labels = cast(list[str], d.pop("labels"))

        report = DecisionReport.from_dict(d.pop("report"))

        active = d.pop("active")

        created_at = isoparse(d.pop("created_at"))

        created_by = d.pop("created_by", UNSET)

        _activated_at = d.pop("activated_at", UNSET)
        activated_at: datetime.datetime | Unset
        if isinstance(_activated_at, Unset):
            activated_at = UNSET
        else:
            activated_at = isoparse(_activated_at)

        decision_version = cls(
            name=name,
            version=version,
            labels=labels,
            report=report,
            active=active,
            created_at=created_at,
            created_by=created_by,
            activated_at=activated_at,
        )

        decision_version.additional_properties = d
        return decision_version

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
