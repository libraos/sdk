from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar

from attrs import define as _attrs_define
from attrs import field as _attrs_field

T = TypeVar("T", bound="ChatCompletionResponseFormat")


@_attrs_define
class ChatCompletionResponseFormat:
    """OpenAI-style response format. Must be an object with a non-empty `type` (otherwise 400); the value of `type` is not
    checked. Forwarded verbatim to OpenAI-compatible providers on the passthrough path; ignored on the agent path, where
    the agent's `output_type` decides the reply shape.

        Attributes:
            type_ (str): e.g. `text`, `json_object`, `json_schema`.
    """

    type_: str
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        type_ = self.type_

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "type": type_,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        type_ = d.pop("type")

        chat_completion_response_format = cls(
            type_=type_,
        )

        chat_completion_response_format.additional_properties = d
        return chat_completion_response_format

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
