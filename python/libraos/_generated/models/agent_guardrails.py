from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..models.agent_guardrails_date_normalizer import AgentGuardrailsDateNormalizer
from ..models.agent_guardrails_pii_redactor import AgentGuardrailsPiiRedactor
from ..types import UNSET, Unset

T = TypeVar("T", bound="AgentGuardrails")


@_attrs_define
class AgentGuardrails:
    """Per-agent opt-outs for the inbound guardrail chain. Each value is
    `enabled`, `disabled` or empty (inherit). On PUT/PATCH an omitted key
    keeps its value, a `null` key clears that override, and a top-level
    `guardrails: null` clears every override.

        Attributes:
            pii_redactor (AgentGuardrailsPiiRedactor | Unset):
            date_normalizer (AgentGuardrailsDateNormalizer | Unset):
    """

    pii_redactor: AgentGuardrailsPiiRedactor | Unset = UNSET
    date_normalizer: AgentGuardrailsDateNormalizer | Unset = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        pii_redactor: str | Unset = UNSET
        if not isinstance(self.pii_redactor, Unset):
            pii_redactor = self.pii_redactor.value

        date_normalizer: str | Unset = UNSET
        if not isinstance(self.date_normalizer, Unset):
            date_normalizer = self.date_normalizer.value

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if pii_redactor is not UNSET:
            field_dict["pii_redactor"] = pii_redactor
        if date_normalizer is not UNSET:
            field_dict["date_normalizer"] = date_normalizer

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        _pii_redactor = d.pop("pii_redactor", UNSET)
        pii_redactor: AgentGuardrailsPiiRedactor | Unset
        if isinstance(_pii_redactor, Unset):
            pii_redactor = UNSET
        else:
            pii_redactor = AgentGuardrailsPiiRedactor(_pii_redactor)

        _date_normalizer = d.pop("date_normalizer", UNSET)
        date_normalizer: AgentGuardrailsDateNormalizer | Unset
        if isinstance(_date_normalizer, Unset):
            date_normalizer = UNSET
        else:
            date_normalizer = AgentGuardrailsDateNormalizer(_date_normalizer)

        agent_guardrails = cls(
            pii_redactor=pii_redactor,
            date_normalizer=date_normalizer,
        )

        agent_guardrails.additional_properties = d
        return agent_guardrails

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
