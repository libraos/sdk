from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..models.usage_working_set_mode import UsageWorkingSetMode
from ..types import UNSET, Unset

T = TypeVar("T", bound="UsageWorkingSet")


@_attrs_define
class UsageWorkingSet:
    """The conversation working set (documents attached in chat) carried by this turn.

    Attributes:
        mode (UsageWorkingSetMode | Unset): `full` injects the documents' text; `manifest` lists them and the model
            reads them with `read_document`.
        docs (int | Unset):
        chars (int | Unset):
        share_limit_tokens (int | Unset): Token limit from the share of the context window.
        max_tokens (int | Unset): Absolute token ceiling for full mode; omitted when none.
        web_gate (str | Unset): `locked`, or `unlocked:<via>` when web retrieval was unlocked on a working-set turn.
    """

    mode: UsageWorkingSetMode | Unset = UNSET
    docs: int | Unset = UNSET
    chars: int | Unset = UNSET
    share_limit_tokens: int | Unset = UNSET
    max_tokens: int | Unset = UNSET
    web_gate: str | Unset = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        mode: str | Unset = UNSET
        if not isinstance(self.mode, Unset):
            mode = self.mode.value

        docs = self.docs

        chars = self.chars

        share_limit_tokens = self.share_limit_tokens

        max_tokens = self.max_tokens

        web_gate = self.web_gate

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if mode is not UNSET:
            field_dict["mode"] = mode
        if docs is not UNSET:
            field_dict["docs"] = docs
        if chars is not UNSET:
            field_dict["chars"] = chars
        if share_limit_tokens is not UNSET:
            field_dict["share_limit_tokens"] = share_limit_tokens
        if max_tokens is not UNSET:
            field_dict["max_tokens"] = max_tokens
        if web_gate is not UNSET:
            field_dict["web_gate"] = web_gate

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        _mode = d.pop("mode", UNSET)
        mode: UsageWorkingSetMode | Unset
        if isinstance(_mode, Unset):
            mode = UNSET
        else:
            mode = UsageWorkingSetMode(_mode)

        docs = d.pop("docs", UNSET)

        chars = d.pop("chars", UNSET)

        share_limit_tokens = d.pop("share_limit_tokens", UNSET)

        max_tokens = d.pop("max_tokens", UNSET)

        web_gate = d.pop("web_gate", UNSET)

        usage_working_set = cls(
            mode=mode,
            docs=docs,
            chars=chars,
            share_limit_tokens=share_limit_tokens,
            max_tokens=max_tokens,
            web_gate=web_gate,
        )

        usage_working_set.additional_properties = d
        return usage_working_set

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
