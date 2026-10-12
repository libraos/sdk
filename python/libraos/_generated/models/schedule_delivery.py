from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

T = TypeVar("T", bound="ScheduleDelivery")


@_attrs_define
class ScheduleDelivery:
    """Where each run's answer is appended. Exactly one of the two.

    Attributes:
        conversation_id (str | Unset): An existing conversation owned by the schedule's owner.
        new_conversation (bool | Unset): Create a dedicated conversation on the first run.
    """

    conversation_id: str | Unset = UNSET
    new_conversation: bool | Unset = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        conversation_id = self.conversation_id

        new_conversation = self.new_conversation

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if conversation_id is not UNSET:
            field_dict["conversation_id"] = conversation_id
        if new_conversation is not UNSET:
            field_dict["new_conversation"] = new_conversation

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        conversation_id = d.pop("conversation_id", UNSET)

        new_conversation = d.pop("new_conversation", UNSET)

        schedule_delivery = cls(
            conversation_id=conversation_id,
            new_conversation=new_conversation,
        )

        schedule_delivery.additional_properties = d
        return schedule_delivery

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
