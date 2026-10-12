from __future__ import annotations

import datetime
from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, TypeVar, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field
from dateutil.parser import isoparse

from ..models.schedule_last_status import ScheduleLastStatus
from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.schedule_delivery import ScheduleDelivery
    from ..models.schedule_metadata import ScheduleMetadata


T = TypeVar("T", bound="Schedule")


@_attrs_define
class Schedule:
    """
    Attributes:
        id (str): `sched_` followed by 24 hex characters.
        tenant_id (str):
        owner_user_id (str):
        agent (str):
        prompt (str):
        timezone (str):
        deliver_to (ScheduleDelivery): Where each run's answer is appended. Exactly one of the two.
        enabled (bool):
        last_job_id (str): Async job id of the last run; empty until the first run.
        last_status (ScheduleLastStatus):
        missed_runs (int):
        consecutive_failures (int):
        created_at (datetime.datetime):
        updated_at (datetime.datetime):
        org_id (None | str | Unset): Null on schedules created before organizations were recorded.
        app_id (str | Unset):
        metadata (ScheduleMetadata | Unset):
        cron (str | Unset):
        every (str | Unset):
        next_run_at (datetime.datetime | None | Unset): Null when disabled.
        last_run_at (datetime.datetime | None | Unset):
        last_error (str | Unset):
    """

    id: str
    tenant_id: str
    owner_user_id: str
    agent: str
    prompt: str
    timezone: str
    deliver_to: ScheduleDelivery
    enabled: bool
    last_job_id: str
    last_status: ScheduleLastStatus
    missed_runs: int
    consecutive_failures: int
    created_at: datetime.datetime
    updated_at: datetime.datetime
    org_id: None | str | Unset = UNSET
    app_id: str | Unset = UNSET
    metadata: ScheduleMetadata | Unset = UNSET
    cron: str | Unset = UNSET
    every: str | Unset = UNSET
    next_run_at: datetime.datetime | None | Unset = UNSET
    last_run_at: datetime.datetime | None | Unset = UNSET
    last_error: str | Unset = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        id = self.id

        tenant_id = self.tenant_id

        owner_user_id = self.owner_user_id

        agent = self.agent

        prompt = self.prompt

        timezone = self.timezone

        deliver_to = self.deliver_to.to_dict()

        enabled = self.enabled

        last_job_id = self.last_job_id

        last_status = self.last_status.value

        missed_runs = self.missed_runs

        consecutive_failures = self.consecutive_failures

        created_at = self.created_at.isoformat()

        updated_at = self.updated_at.isoformat()

        org_id: None | str | Unset
        if isinstance(self.org_id, Unset):
            org_id = UNSET
        else:
            org_id = self.org_id

        app_id = self.app_id

        metadata: dict[str, Any] | Unset = UNSET
        if not isinstance(self.metadata, Unset):
            metadata = self.metadata.to_dict()

        cron = self.cron

        every = self.every

        next_run_at: None | str | Unset
        if isinstance(self.next_run_at, Unset):
            next_run_at = UNSET
        elif isinstance(self.next_run_at, datetime.datetime):
            next_run_at = self.next_run_at.isoformat()
        else:
            next_run_at = self.next_run_at

        last_run_at: None | str | Unset
        if isinstance(self.last_run_at, Unset):
            last_run_at = UNSET
        elif isinstance(self.last_run_at, datetime.datetime):
            last_run_at = self.last_run_at.isoformat()
        else:
            last_run_at = self.last_run_at

        last_error = self.last_error

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "id": id,
                "tenant_id": tenant_id,
                "owner_user_id": owner_user_id,
                "agent": agent,
                "prompt": prompt,
                "timezone": timezone,
                "deliver_to": deliver_to,
                "enabled": enabled,
                "last_job_id": last_job_id,
                "last_status": last_status,
                "missed_runs": missed_runs,
                "consecutive_failures": consecutive_failures,
                "created_at": created_at,
                "updated_at": updated_at,
            }
        )
        if org_id is not UNSET:
            field_dict["org_id"] = org_id
        if app_id is not UNSET:
            field_dict["app_id"] = app_id
        if metadata is not UNSET:
            field_dict["metadata"] = metadata
        if cron is not UNSET:
            field_dict["cron"] = cron
        if every is not UNSET:
            field_dict["every"] = every
        if next_run_at is not UNSET:
            field_dict["next_run_at"] = next_run_at
        if last_run_at is not UNSET:
            field_dict["last_run_at"] = last_run_at
        if last_error is not UNSET:
            field_dict["last_error"] = last_error

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.schedule_delivery import ScheduleDelivery
        from ..models.schedule_metadata import ScheduleMetadata

        d = dict(src_dict)
        id = d.pop("id")

        tenant_id = d.pop("tenant_id")

        owner_user_id = d.pop("owner_user_id")

        agent = d.pop("agent")

        prompt = d.pop("prompt")

        timezone = d.pop("timezone")

        deliver_to = ScheduleDelivery.from_dict(d.pop("deliver_to"))

        enabled = d.pop("enabled")

        last_job_id = d.pop("last_job_id")

        last_status = ScheduleLastStatus(d.pop("last_status"))

        missed_runs = d.pop("missed_runs")

        consecutive_failures = d.pop("consecutive_failures")

        created_at = isoparse(d.pop("created_at"))

        updated_at = isoparse(d.pop("updated_at"))

        def _parse_org_id(data: object) -> None | str | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(None | str | Unset, data)

        org_id = _parse_org_id(d.pop("org_id", UNSET))

        app_id = d.pop("app_id", UNSET)

        _metadata = d.pop("metadata", UNSET)
        metadata: ScheduleMetadata | Unset
        if isinstance(_metadata, Unset):
            metadata = UNSET
        else:
            metadata = ScheduleMetadata.from_dict(_metadata)

        cron = d.pop("cron", UNSET)

        every = d.pop("every", UNSET)

        def _parse_next_run_at(data: object) -> datetime.datetime | None | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            try:
                if not isinstance(data, str):
                    raise TypeError()
                next_run_at_type_0 = isoparse(data)

                return next_run_at_type_0
            except (TypeError, ValueError, AttributeError, KeyError):
                pass
            return cast(datetime.datetime | None | Unset, data)

        next_run_at = _parse_next_run_at(d.pop("next_run_at", UNSET))

        def _parse_last_run_at(data: object) -> datetime.datetime | None | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            try:
                if not isinstance(data, str):
                    raise TypeError()
                last_run_at_type_0 = isoparse(data)

                return last_run_at_type_0
            except (TypeError, ValueError, AttributeError, KeyError):
                pass
            return cast(datetime.datetime | None | Unset, data)

        last_run_at = _parse_last_run_at(d.pop("last_run_at", UNSET))

        last_error = d.pop("last_error", UNSET)

        schedule = cls(
            id=id,
            tenant_id=tenant_id,
            owner_user_id=owner_user_id,
            agent=agent,
            prompt=prompt,
            timezone=timezone,
            deliver_to=deliver_to,
            enabled=enabled,
            last_job_id=last_job_id,
            last_status=last_status,
            missed_runs=missed_runs,
            consecutive_failures=consecutive_failures,
            created_at=created_at,
            updated_at=updated_at,
            org_id=org_id,
            app_id=app_id,
            metadata=metadata,
            cron=cron,
            every=every,
            next_run_at=next_run_at,
            last_run_at=last_run_at,
            last_error=last_error,
        )

        schedule.additional_properties = d
        return schedule

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
