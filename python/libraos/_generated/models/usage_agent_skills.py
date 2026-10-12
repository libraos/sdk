from __future__ import annotations

from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, TypeVar, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.usage_agent_skill import UsageAgentSkill


T = TypeVar("T", bound="UsageAgentSkills")


@_attrs_define
class UsageAgentSkills:
    """Agent Skills attached to and loaded by this turn.

    Attributes:
        attached (list[UsageAgentSkill] | Unset):
        loaded (list[str] | Unset): Skills loaded during the turn, in order.
        inlined (bool | Unset):
        unresolved (list[str] | Unset):
    """

    attached: list[UsageAgentSkill] | Unset = UNSET
    loaded: list[str] | Unset = UNSET
    inlined: bool | Unset = UNSET
    unresolved: list[str] | Unset = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        attached: list[dict[str, Any]] | Unset = UNSET
        if not isinstance(self.attached, Unset):
            attached = []
            for attached_item_data in self.attached:
                attached_item = attached_item_data.to_dict()
                attached.append(attached_item)

        loaded: list[str] | Unset = UNSET
        if not isinstance(self.loaded, Unset):
            loaded = self.loaded

        inlined = self.inlined

        unresolved: list[str] | Unset = UNSET
        if not isinstance(self.unresolved, Unset):
            unresolved = self.unresolved

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if attached is not UNSET:
            field_dict["attached"] = attached
        if loaded is not UNSET:
            field_dict["loaded"] = loaded
        if inlined is not UNSET:
            field_dict["inlined"] = inlined
        if unresolved is not UNSET:
            field_dict["unresolved"] = unresolved

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.usage_agent_skill import UsageAgentSkill

        d = dict(src_dict)
        _attached = d.pop("attached", UNSET)
        attached: list[UsageAgentSkill] | Unset = UNSET
        if _attached is not UNSET:
            attached = []
            for attached_item_data in _attached:
                attached_item = UsageAgentSkill.from_dict(attached_item_data)

                attached.append(attached_item)

        loaded = cast(list[str], d.pop("loaded", UNSET))

        inlined = d.pop("inlined", UNSET)

        unresolved = cast(list[str], d.pop("unresolved", UNSET))

        usage_agent_skills = cls(
            attached=attached,
            loaded=loaded,
            inlined=inlined,
            unresolved=unresolved,
        )

        usage_agent_skills.additional_properties = d
        return usage_agent_skills

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
