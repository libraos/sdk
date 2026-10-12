from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..models.retrieval_ambiguity_ambiguity_action import RetrievalAmbiguityAmbiguityAction

T = TypeVar("T", bound="RetrievalAmbiguity")


@_attrs_define
class RetrievalAmbiguity:
    """Present only when the evidence the answer relied on spanned several documents the conversation did not choose
    between and the agent's ambiguous-entity handling is `state` or `ask`.

        Attributes:
            ambiguous_sources (list[str]): Source ids of the candidate documents.
            ambiguity_action (RetrievalAmbiguityAmbiguityAction):
    """

    ambiguous_sources: list[str]
    ambiguity_action: RetrievalAmbiguityAmbiguityAction
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        ambiguous_sources = self.ambiguous_sources

        ambiguity_action = self.ambiguity_action.value

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "ambiguous_sources": ambiguous_sources,
                "ambiguity_action": ambiguity_action,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        ambiguous_sources = cast(list[str], d.pop("ambiguous_sources"))

        ambiguity_action = RetrievalAmbiguityAmbiguityAction(d.pop("ambiguity_action"))

        retrieval_ambiguity = cls(
            ambiguous_sources=ambiguous_sources,
            ambiguity_action=ambiguity_action,
        )

        retrieval_ambiguity.additional_properties = d
        return retrieval_ambiguity

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
