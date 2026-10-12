from __future__ import annotations

from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, TypeVar

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.schedule_delivery import ScheduleDelivery
    from ..models.schedule_write_metadata import ScheduleWriteMetadata


T = TypeVar("T", bound="ScheduleWrite")


@_attrs_define
class ScheduleWrite:
    """Create body (`agent`, `prompt`, `deliver_to` and one of `cron` / `every` required) or PATCH body (every field
    optional; the merged schedule is re-validated).

        Attributes:
            agent (str | Unset): Agent the run is submitted to; must be runnable by the caller and support streaming.
            prompt (str | Unset): The message each run sends.
            metadata (ScheduleWriteMetadata | Unset): Per-run chat metadata; replaced as a whole.
            cron (str | Unset): Five-field cron expression or a descriptor such as `@daily`. No `TZ=` prefix and no
                `@every`. Setting it clears `every`.
            every (str | Unset): Fixed interval as a duration (e.g. `30m`, `1h`), at least `1m`. Setting it clears `cron`.
            timezone (str | Unset): IANA time zone name. Default `UTC`.
            deliver_to (ScheduleDelivery | Unset): Where each run's answer is appended. Exactly one of the two.
            enabled (bool | Unset): Default true. Re-enabling resets the failure count.
    """

    agent: str | Unset = UNSET
    prompt: str | Unset = UNSET
    metadata: ScheduleWriteMetadata | Unset = UNSET
    cron: str | Unset = UNSET
    every: str | Unset = UNSET
    timezone: str | Unset = UNSET
    deliver_to: ScheduleDelivery | Unset = UNSET
    enabled: bool | Unset = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        agent = self.agent

        prompt = self.prompt

        metadata: dict[str, Any] | Unset = UNSET
        if not isinstance(self.metadata, Unset):
            metadata = self.metadata.to_dict()

        cron = self.cron

        every = self.every

        timezone = self.timezone

        deliver_to: dict[str, Any] | Unset = UNSET
        if not isinstance(self.deliver_to, Unset):
            deliver_to = self.deliver_to.to_dict()

        enabled = self.enabled

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if agent is not UNSET:
            field_dict["agent"] = agent
        if prompt is not UNSET:
            field_dict["prompt"] = prompt
        if metadata is not UNSET:
            field_dict["metadata"] = metadata
        if cron is not UNSET:
            field_dict["cron"] = cron
        if every is not UNSET:
            field_dict["every"] = every
        if timezone is not UNSET:
            field_dict["timezone"] = timezone
        if deliver_to is not UNSET:
            field_dict["deliver_to"] = deliver_to
        if enabled is not UNSET:
            field_dict["enabled"] = enabled

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.schedule_delivery import ScheduleDelivery
        from ..models.schedule_write_metadata import ScheduleWriteMetadata

        d = dict(src_dict)
        agent = d.pop("agent", UNSET)

        prompt = d.pop("prompt", UNSET)

        _metadata = d.pop("metadata", UNSET)
        metadata: ScheduleWriteMetadata | Unset
        if isinstance(_metadata, Unset):
            metadata = UNSET
        else:
            metadata = ScheduleWriteMetadata.from_dict(_metadata)

        cron = d.pop("cron", UNSET)

        every = d.pop("every", UNSET)

        timezone = d.pop("timezone", UNSET)

        _deliver_to = d.pop("deliver_to", UNSET)
        deliver_to: ScheduleDelivery | Unset
        if isinstance(_deliver_to, Unset):
            deliver_to = UNSET
        else:
            deliver_to = ScheduleDelivery.from_dict(_deliver_to)

        enabled = d.pop("enabled", UNSET)

        schedule_write = cls(
            agent=agent,
            prompt=prompt,
            metadata=metadata,
            cron=cron,
            every=every,
            timezone=timezone,
            deliver_to=deliver_to,
            enabled=enabled,
        )

        schedule_write.additional_properties = d
        return schedule_write

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
