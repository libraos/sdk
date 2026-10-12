from __future__ import annotations

from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, TypeVar

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..models.chat_completion_request_reasoning_effort import ChatCompletionRequestReasoningEffort
from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.chat_completion_request_metadata import ChatCompletionRequestMetadata
    from ..models.chat_completion_response_format import ChatCompletionResponseFormat
    from ..models.chat_message import ChatMessage


T = TypeVar("T", bound="ChatCompletionRequest")


@_attrs_define
class ChatCompletionRequest:
    """OpenAI-compatible chat completion request.

    Attributes:
        messages (list[ChatMessage]):
        model (str | Unset): Target model/agent id. When gateway mode is enabled, a value of the form
            `llm:<provider>/<model>` selects raw provider passthrough.
        stream (bool | Unset): When true the response is an SSE stream terminated by `[DONE]`.
        max_tokens (int | Unset): Output-token cap (folded into the per-call answer limit).
        max_completion_tokens (int | Unset): Newer OpenAI field for the output-token cap; preferred over max_tokens when
            both are set. On the agent path it becomes the per-call answer cap (clamped to 32768) unless
            `metadata.max_tokens` is set.
        temperature (float | Unset): Sampling temperature, 0-2 (otherwise 400). On the passthrough path it is sent to
            the provider; on the agent path it becomes the per-call answer temperature unless `metadata.temperature` is set.
        reasoning_effort (ChatCompletionRequestReasoningEffort | Unset): Native reasoning effort for the answer call
            (otherwise 400). `off` or empty sends no reasoning parameter (the model's default); `none` asks the model not to
            reason. On the agent path it becomes `metadata.thinking.effort` unless `metadata.thinking` is set.
        response_format (ChatCompletionResponseFormat | Unset): OpenAI-style response format. Must be an object with a
            non-empty `type` (otherwise 400); the value of `type` is not checked. Forwarded verbatim to OpenAI-compatible
            providers on the passthrough path; ignored on the agent path, where the agent's `output_type` decides the reply
            shape.
        metadata (ChatCompletionRequestMetadata | Unset): Nova OS extension channel for per-call fields (e.g. a per-call
            model override). The documented keys below are honoured on this surface the same way as on native chat.
    """

    messages: list[ChatMessage]
    model: str | Unset = UNSET
    stream: bool | Unset = UNSET
    max_tokens: int | Unset = UNSET
    max_completion_tokens: int | Unset = UNSET
    temperature: float | Unset = UNSET
    reasoning_effort: ChatCompletionRequestReasoningEffort | Unset = UNSET
    response_format: ChatCompletionResponseFormat | Unset = UNSET
    metadata: ChatCompletionRequestMetadata | Unset = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        messages = []
        for messages_item_data in self.messages:
            messages_item = messages_item_data.to_dict()
            messages.append(messages_item)

        model = self.model

        stream = self.stream

        max_tokens = self.max_tokens

        max_completion_tokens = self.max_completion_tokens

        temperature = self.temperature

        reasoning_effort: str | Unset = UNSET
        if not isinstance(self.reasoning_effort, Unset):
            reasoning_effort = self.reasoning_effort.value

        response_format: dict[str, Any] | Unset = UNSET
        if not isinstance(self.response_format, Unset):
            response_format = self.response_format.to_dict()

        metadata: dict[str, Any] | Unset = UNSET
        if not isinstance(self.metadata, Unset):
            metadata = self.metadata.to_dict()

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "messages": messages,
            }
        )
        if model is not UNSET:
            field_dict["model"] = model
        if stream is not UNSET:
            field_dict["stream"] = stream
        if max_tokens is not UNSET:
            field_dict["max_tokens"] = max_tokens
        if max_completion_tokens is not UNSET:
            field_dict["max_completion_tokens"] = max_completion_tokens
        if temperature is not UNSET:
            field_dict["temperature"] = temperature
        if reasoning_effort is not UNSET:
            field_dict["reasoning_effort"] = reasoning_effort
        if response_format is not UNSET:
            field_dict["response_format"] = response_format
        if metadata is not UNSET:
            field_dict["metadata"] = metadata

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.chat_completion_request_metadata import ChatCompletionRequestMetadata
        from ..models.chat_completion_response_format import ChatCompletionResponseFormat
        from ..models.chat_message import ChatMessage

        d = dict(src_dict)
        messages = []
        _messages = d.pop("messages")
        for messages_item_data in _messages:
            messages_item = ChatMessage.from_dict(messages_item_data)

            messages.append(messages_item)

        model = d.pop("model", UNSET)

        stream = d.pop("stream", UNSET)

        max_tokens = d.pop("max_tokens", UNSET)

        max_completion_tokens = d.pop("max_completion_tokens", UNSET)

        temperature = d.pop("temperature", UNSET)

        _reasoning_effort = d.pop("reasoning_effort", UNSET)
        reasoning_effort: ChatCompletionRequestReasoningEffort | Unset
        if isinstance(_reasoning_effort, Unset):
            reasoning_effort = UNSET
        else:
            reasoning_effort = ChatCompletionRequestReasoningEffort(_reasoning_effort)

        _response_format = d.pop("response_format", UNSET)
        response_format: ChatCompletionResponseFormat | Unset
        if isinstance(_response_format, Unset):
            response_format = UNSET
        else:
            response_format = ChatCompletionResponseFormat.from_dict(_response_format)

        _metadata = d.pop("metadata", UNSET)
        metadata: ChatCompletionRequestMetadata | Unset
        if isinstance(_metadata, Unset):
            metadata = UNSET
        else:
            metadata = ChatCompletionRequestMetadata.from_dict(_metadata)

        chat_completion_request = cls(
            messages=messages,
            model=model,
            stream=stream,
            max_tokens=max_tokens,
            max_completion_tokens=max_completion_tokens,
            temperature=temperature,
            reasoning_effort=reasoning_effort,
            response_format=response_format,
            metadata=metadata,
        )

        chat_completion_request.additional_properties = d
        return chat_completion_request

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
