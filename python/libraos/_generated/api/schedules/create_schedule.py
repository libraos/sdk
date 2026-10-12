from http import HTTPStatus
from typing import Any

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.error import Error
from ...models.flat_error import FlatError
from ...models.schedule import Schedule
from ...models.schedule_limit_error import ScheduleLimitError
from ...models.schedule_write import ScheduleWrite
from ...types import Response


def _get_kwargs(
    *,
    body: ScheduleWrite,
) -> dict[str, Any]:
    headers: dict[str, Any] = {}

    _kwargs: dict[str, Any] = {
        "method": "post",
        "url": "/v1/managed/schedules",
    }

    _kwargs["json"] = body.to_dict()

    headers["Content-Type"] = "application/json"

    _kwargs["headers"] = headers
    return _kwargs


def _parse_response(
    *, client: AuthenticatedClient | Client, response: httpx.Response
) -> Error | FlatError | Schedule | ScheduleLimitError | None:
    if response.status_code == 201:
        response_201 = Schedule.from_dict(response.json())

        return response_201

    if response.status_code == 400:
        response_400 = FlatError.from_dict(response.json())

        return response_400

    if response.status_code == 401:
        response_401 = Error.from_dict(response.json())

        return response_401

    if response.status_code == 403:
        response_403 = FlatError.from_dict(response.json())

        return response_403

    if response.status_code == 404:
        response_404 = FlatError.from_dict(response.json())

        return response_404

    if response.status_code == 409:
        response_409 = ScheduleLimitError.from_dict(response.json())

        return response_409

    if client.raise_on_unexpected_status:
        raise errors.UnexpectedStatus(response.status_code, response.content)
    else:
        return None


def _build_response(
    *, client: AuthenticatedClient | Client, response: httpx.Response
) -> Response[Error | FlatError | Schedule | ScheduleLimitError]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    *,
    client: AuthenticatedClient | Client,
    body: ScheduleWrite,
) -> Response[Error | FlatError | Schedule | ScheduleLimitError]:
    """Create a scheduled run

     Runs `prompt` against `agent` on a cron expression or fixed interval, as the caller, through the
    async job path, and appends each finished answer to the `deliver_to` conversation. The interval must
    not be below the deployment minimum (`LIBRA_OS_SCHEDULES_MIN_INTERVAL`, default 15m). A schedule is
    auto-paused (`last_status: paused_failures`) after `LIBRA_OS_SCHEDULES_MAX_FAILURES` (default 3)
    consecutive failed runs. Requires a user session (API keys get 403).

    Args:
        body (ScheduleWrite): Create body (`agent`, `prompt`, `deliver_to` and one of `cron` /
            `every` required) or PATCH body (every field optional; the merged schedule is re-
            validated).

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Error | FlatError | Schedule | ScheduleLimitError]
    """

    kwargs = _get_kwargs(
        body=body,
    )

    response = client.get_httpx_client().request(
        **kwargs,
    )

    return _build_response(client=client, response=response)


def sync(
    *,
    client: AuthenticatedClient | Client,
    body: ScheduleWrite,
) -> Error | FlatError | Schedule | ScheduleLimitError | None:
    """Create a scheduled run

     Runs `prompt` against `agent` on a cron expression or fixed interval, as the caller, through the
    async job path, and appends each finished answer to the `deliver_to` conversation. The interval must
    not be below the deployment minimum (`LIBRA_OS_SCHEDULES_MIN_INTERVAL`, default 15m). A schedule is
    auto-paused (`last_status: paused_failures`) after `LIBRA_OS_SCHEDULES_MAX_FAILURES` (default 3)
    consecutive failed runs. Requires a user session (API keys get 403).

    Args:
        body (ScheduleWrite): Create body (`agent`, `prompt`, `deliver_to` and one of `cron` /
            `every` required) or PATCH body (every field optional; the merged schedule is re-
            validated).

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Error | FlatError | Schedule | ScheduleLimitError
    """

    return sync_detailed(
        client=client,
        body=body,
    ).parsed


async def asyncio_detailed(
    *,
    client: AuthenticatedClient | Client,
    body: ScheduleWrite,
) -> Response[Error | FlatError | Schedule | ScheduleLimitError]:
    """Create a scheduled run

     Runs `prompt` against `agent` on a cron expression or fixed interval, as the caller, through the
    async job path, and appends each finished answer to the `deliver_to` conversation. The interval must
    not be below the deployment minimum (`LIBRA_OS_SCHEDULES_MIN_INTERVAL`, default 15m). A schedule is
    auto-paused (`last_status: paused_failures`) after `LIBRA_OS_SCHEDULES_MAX_FAILURES` (default 3)
    consecutive failed runs. Requires a user session (API keys get 403).

    Args:
        body (ScheduleWrite): Create body (`agent`, `prompt`, `deliver_to` and one of `cron` /
            `every` required) or PATCH body (every field optional; the merged schedule is re-
            validated).

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Error | FlatError | Schedule | ScheduleLimitError]
    """

    kwargs = _get_kwargs(
        body=body,
    )

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    *,
    client: AuthenticatedClient | Client,
    body: ScheduleWrite,
) -> Error | FlatError | Schedule | ScheduleLimitError | None:
    """Create a scheduled run

     Runs `prompt` against `agent` on a cron expression or fixed interval, as the caller, through the
    async job path, and appends each finished answer to the `deliver_to` conversation. The interval must
    not be below the deployment minimum (`LIBRA_OS_SCHEDULES_MIN_INTERVAL`, default 15m). A schedule is
    auto-paused (`last_status: paused_failures`) after `LIBRA_OS_SCHEDULES_MAX_FAILURES` (default 3)
    consecutive failed runs. Requires a user session (API keys get 403).

    Args:
        body (ScheduleWrite): Create body (`agent`, `prompt`, `deliver_to` and one of `cron` /
            `every` required) or PATCH body (every field optional; the merged schedule is re-
            validated).

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Error | FlatError | Schedule | ScheduleLimitError
    """

    return (
        await asyncio_detailed(
            client=client,
            body=body,
        )
    ).parsed
