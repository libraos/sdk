from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..models.agent_triage_default_brain import AgentTriageDefaultBrain
from ..types import UNSET, Unset

T = TypeVar("T", bound="AgentTriage")


@_attrs_define
class AgentTriage:
    """Persona planner routing pin. `triage` keeps the per-turn
    regex/LLM triage cascade, `always` runs the planner every turn,
    `never` skips it. Empty clears the pin (inherit the server default).
    Per-call `metadata.brain` still wins.

        Attributes:
            default_brain (AgentTriageDefaultBrain | Unset):
    """

    default_brain: AgentTriageDefaultBrain | Unset = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        default_brain: str | Unset = UNSET
        if not isinstance(self.default_brain, Unset):
            default_brain = self.default_brain.value

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if default_brain is not UNSET:
            field_dict["default_brain"] = default_brain

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        _default_brain = d.pop("default_brain", UNSET)
        default_brain: AgentTriageDefaultBrain | Unset
        if isinstance(_default_brain, Unset):
            default_brain = UNSET
        else:
            default_brain = AgentTriageDefaultBrain(_default_brain)

        agent_triage = cls(
            default_brain=default_brain,
        )

        agent_triage.additional_properties = d
        return agent_triage

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
