from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

T = TypeVar("T", bound="UsageStage")


@_attrs_define
class UsageStage:
    """Token usage for one stage/sub-call of a turn.

    Attributes:
        stage (str | Unset): The stage/agent that made the sub-call.
        model (str | Unset): The model used for the sub-call.
        prompt_tokens (int | Unset):
        completion_tokens (int | Unset):
        cache_read_tokens (int | Unset):
        cache_write_tokens (int | Unset):
        duration_ms (int | Unset): Summed model wall time for this stage's calls.
        llm_calls (int | Unset): Number of model calls in this stage.
        first_token_ms (int | Unset): Time to first token of the stage's first streamed call.
        tool_calls (int | Unset): Tool calls made by this stage.
        tool_ms (int | Unset): Summed tool wall time for this stage.
    """

    stage: str | Unset = UNSET
    model: str | Unset = UNSET
    prompt_tokens: int | Unset = UNSET
    completion_tokens: int | Unset = UNSET
    cache_read_tokens: int | Unset = UNSET
    cache_write_tokens: int | Unset = UNSET
    duration_ms: int | Unset = UNSET
    llm_calls: int | Unset = UNSET
    first_token_ms: int | Unset = UNSET
    tool_calls: int | Unset = UNSET
    tool_ms: int | Unset = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        stage = self.stage

        model = self.model

        prompt_tokens = self.prompt_tokens

        completion_tokens = self.completion_tokens

        cache_read_tokens = self.cache_read_tokens

        cache_write_tokens = self.cache_write_tokens

        duration_ms = self.duration_ms

        llm_calls = self.llm_calls

        first_token_ms = self.first_token_ms

        tool_calls = self.tool_calls

        tool_ms = self.tool_ms

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if stage is not UNSET:
            field_dict["stage"] = stage
        if model is not UNSET:
            field_dict["model"] = model
        if prompt_tokens is not UNSET:
            field_dict["prompt_tokens"] = prompt_tokens
        if completion_tokens is not UNSET:
            field_dict["completion_tokens"] = completion_tokens
        if cache_read_tokens is not UNSET:
            field_dict["cache_read_tokens"] = cache_read_tokens
        if cache_write_tokens is not UNSET:
            field_dict["cache_write_tokens"] = cache_write_tokens
        if duration_ms is not UNSET:
            field_dict["duration_ms"] = duration_ms
        if llm_calls is not UNSET:
            field_dict["llm_calls"] = llm_calls
        if first_token_ms is not UNSET:
            field_dict["first_token_ms"] = first_token_ms
        if tool_calls is not UNSET:
            field_dict["tool_calls"] = tool_calls
        if tool_ms is not UNSET:
            field_dict["tool_ms"] = tool_ms

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        stage = d.pop("stage", UNSET)

        model = d.pop("model", UNSET)

        prompt_tokens = d.pop("prompt_tokens", UNSET)

        completion_tokens = d.pop("completion_tokens", UNSET)

        cache_read_tokens = d.pop("cache_read_tokens", UNSET)

        cache_write_tokens = d.pop("cache_write_tokens", UNSET)

        duration_ms = d.pop("duration_ms", UNSET)

        llm_calls = d.pop("llm_calls", UNSET)

        first_token_ms = d.pop("first_token_ms", UNSET)

        tool_calls = d.pop("tool_calls", UNSET)

        tool_ms = d.pop("tool_ms", UNSET)

        usage_stage = cls(
            stage=stage,
            model=model,
            prompt_tokens=prompt_tokens,
            completion_tokens=completion_tokens,
            cache_read_tokens=cache_read_tokens,
            cache_write_tokens=cache_write_tokens,
            duration_ms=duration_ms,
            llm_calls=llm_calls,
            first_token_ms=first_token_ms,
            tool_calls=tool_calls,
            tool_ms=tool_ms,
        )

        usage_stage.additional_properties = d
        return usage_stage

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
