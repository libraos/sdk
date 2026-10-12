from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

T = TypeVar("T", bound="UsageSpan")


@_attrs_define
class UsageSpan:
    """One span of the turn timeline, relative to the turn start.

    Attributes:
        kind (str | Unset): One of `triage`, `planner`, `task`, `aspect`, `tool`, `llm`, `synthesis`, `direct`, `phase`.
        name (str | Unset):
        start_ms (int | Unset):
        duration_ms (int | Unset):
        first_token_ms (int | Unset):
        phase (str | Unset):
        stage (str | Unset):
        model (str | Unset):
        task_id (str | Unset):
        capability (str | Unset):
        skill (str | Unset):
        level (int | Unset): DAG level of a planner task.
        tool (str | Unset):
        status (str | Unset):
    """

    kind: str | Unset = UNSET
    name: str | Unset = UNSET
    start_ms: int | Unset = UNSET
    duration_ms: int | Unset = UNSET
    first_token_ms: int | Unset = UNSET
    phase: str | Unset = UNSET
    stage: str | Unset = UNSET
    model: str | Unset = UNSET
    task_id: str | Unset = UNSET
    capability: str | Unset = UNSET
    skill: str | Unset = UNSET
    level: int | Unset = UNSET
    tool: str | Unset = UNSET
    status: str | Unset = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        kind = self.kind

        name = self.name

        start_ms = self.start_ms

        duration_ms = self.duration_ms

        first_token_ms = self.first_token_ms

        phase = self.phase

        stage = self.stage

        model = self.model

        task_id = self.task_id

        capability = self.capability

        skill = self.skill

        level = self.level

        tool = self.tool

        status = self.status

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if kind is not UNSET:
            field_dict["kind"] = kind
        if name is not UNSET:
            field_dict["name"] = name
        if start_ms is not UNSET:
            field_dict["start_ms"] = start_ms
        if duration_ms is not UNSET:
            field_dict["duration_ms"] = duration_ms
        if first_token_ms is not UNSET:
            field_dict["first_token_ms"] = first_token_ms
        if phase is not UNSET:
            field_dict["phase"] = phase
        if stage is not UNSET:
            field_dict["stage"] = stage
        if model is not UNSET:
            field_dict["model"] = model
        if task_id is not UNSET:
            field_dict["task_id"] = task_id
        if capability is not UNSET:
            field_dict["capability"] = capability
        if skill is not UNSET:
            field_dict["skill"] = skill
        if level is not UNSET:
            field_dict["level"] = level
        if tool is not UNSET:
            field_dict["tool"] = tool
        if status is not UNSET:
            field_dict["status"] = status

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        kind = d.pop("kind", UNSET)

        name = d.pop("name", UNSET)

        start_ms = d.pop("start_ms", UNSET)

        duration_ms = d.pop("duration_ms", UNSET)

        first_token_ms = d.pop("first_token_ms", UNSET)

        phase = d.pop("phase", UNSET)

        stage = d.pop("stage", UNSET)

        model = d.pop("model", UNSET)

        task_id = d.pop("task_id", UNSET)

        capability = d.pop("capability", UNSET)

        skill = d.pop("skill", UNSET)

        level = d.pop("level", UNSET)

        tool = d.pop("tool", UNSET)

        status = d.pop("status", UNSET)

        usage_span = cls(
            kind=kind,
            name=name,
            start_ms=start_ms,
            duration_ms=duration_ms,
            first_token_ms=first_token_ms,
            phase=phase,
            stage=stage,
            model=model,
            task_id=task_id,
            capability=capability,
            skill=skill,
            level=level,
            tool=tool,
            status=status,
        )

        usage_span.additional_properties = d
        return usage_span

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
