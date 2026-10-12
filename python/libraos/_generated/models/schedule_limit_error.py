from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..models.schedule_limit_error_error import ScheduleLimitErrorError

T = TypeVar("T", bound="ScheduleLimitError")


@_attrs_define
class ScheduleLimitError:
    """
    Attributes:
        error (ScheduleLimitErrorError):
        limit (int):
        message (str):
    """

    error: ScheduleLimitErrorError
    limit: int
    message: str
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        error = self.error.value

        limit = self.limit

        message = self.message

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "error": error,
                "limit": limit,
                "message": message,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        error = ScheduleLimitErrorError(d.pop("error"))

        limit = d.pop("limit")

        message = d.pop("message")

        schedule_limit_error = cls(
            error=error,
            limit=limit,
            message=message,
        )

        schedule_limit_error.additional_properties = d
        return schedule_limit_error

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
