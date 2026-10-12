from http import HTTPStatus
from typing import Any

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.flat_error import FlatError
from ...types import UNSET, Response, Unset


def _get_kwargs(
    *,
    task: str | Unset = UNSET,
    hardware: str | Unset = UNSET,
    compatibility: str | Unset = UNSET,
) -> dict[str, Any]:

    params: dict[str, Any] = {}

    params["task"] = task

    params["hardware"] = hardware

    params["compatibility"] = compatibility

    params = {k: v for k, v in params.items() if v is not UNSET and v is not None}

    _kwargs: dict[str, Any] = {
        "method": "get",
        "url": "/v1/managed/models/recommendations.md",
        "params": params,
    }

    return _kwargs


def _parse_response(*, client: AuthenticatedClient | Client, response: httpx.Response) -> FlatError | str | None:
    if response.status_code == 200:
        response_200 = response.text
        return response_200

    if response.status_code == 400:
        response_400 = FlatError.from_dict(response.json())

        return response_400

    if response.status_code == 401:
        response_401 = FlatError.from_dict(response.json())

        return response_401

    if response.status_code == 403:
        response_403 = FlatError.from_dict(response.json())

        return response_403

    if response.status_code == 503:
        response_503 = FlatError.from_dict(response.json())

        return response_503

    if client.raise_on_unexpected_status:
        raise errors.UnexpectedStatus(response.status_code, response.content)
    else:
        return None


def _build_response(*, client: AuthenticatedClient | Client, response: httpx.Response) -> Response[FlatError | str]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    *,
    client: AuthenticatedClient | Client,
    task: str | Unset = UNSET,
    hardware: str | Unset = UNSET,
    compatibility: str | Unset = UNSET,
) -> Response[FlatError | str]:
    """Model recommendations as Markdown

     The same report as `GET /v1/managed/models/recommendations`, rendered as Markdown. Same access rules
    and query parameters.

    Args:
        task (str | Unset):
        hardware (str | Unset):
        compatibility (str | Unset):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[FlatError | str]
    """

    kwargs = _get_kwargs(
        task=task,
        hardware=hardware,
        compatibility=compatibility,
    )

    response = client.get_httpx_client().request(
        **kwargs,
    )

    return _build_response(client=client, response=response)


def sync(
    *,
    client: AuthenticatedClient | Client,
    task: str | Unset = UNSET,
    hardware: str | Unset = UNSET,
    compatibility: str | Unset = UNSET,
) -> FlatError | str | None:
    """Model recommendations as Markdown

     The same report as `GET /v1/managed/models/recommendations`, rendered as Markdown. Same access rules
    and query parameters.

    Args:
        task (str | Unset):
        hardware (str | Unset):
        compatibility (str | Unset):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        FlatError | str
    """

    return sync_detailed(
        client=client,
        task=task,
        hardware=hardware,
        compatibility=compatibility,
    ).parsed


async def asyncio_detailed(
    *,
    client: AuthenticatedClient | Client,
    task: str | Unset = UNSET,
    hardware: str | Unset = UNSET,
    compatibility: str | Unset = UNSET,
) -> Response[FlatError | str]:
    """Model recommendations as Markdown

     The same report as `GET /v1/managed/models/recommendations`, rendered as Markdown. Same access rules
    and query parameters.

    Args:
        task (str | Unset):
        hardware (str | Unset):
        compatibility (str | Unset):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[FlatError | str]
    """

    kwargs = _get_kwargs(
        task=task,
        hardware=hardware,
        compatibility=compatibility,
    )

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    *,
    client: AuthenticatedClient | Client,
    task: str | Unset = UNSET,
    hardware: str | Unset = UNSET,
    compatibility: str | Unset = UNSET,
) -> FlatError | str | None:
    """Model recommendations as Markdown

     The same report as `GET /v1/managed/models/recommendations`, rendered as Markdown. Same access rules
    and query parameters.

    Args:
        task (str | Unset):
        hardware (str | Unset):
        compatibility (str | Unset):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        FlatError | str
    """

    return (
        await asyncio_detailed(
            client=client,
            task=task,
            hardware=hardware,
            compatibility=compatibility,
        )
    ).parsed
