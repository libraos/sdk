from http import HTTPStatus
from typing import Any

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.error import Error
from ...models.field_error import FieldError
from ...models.user_skill_list import UserSkillList
from ...types import Response


def _get_kwargs() -> dict[str, Any]:

    _kwargs: dict[str, Any] = {
        "method": "get",
        "url": "/v1/user-skills",
    }

    return _kwargs


def _parse_response(
    *, client: AuthenticatedClient | Client, response: httpx.Response
) -> Error | FieldError | UserSkillList | None:
    if response.status_code == 200:
        response_200 = UserSkillList.from_dict(response.json())

        return response_200

    if response.status_code == 401:
        response_401 = Error.from_dict(response.json())

        return response_401

    if response.status_code == 403:
        response_403 = FieldError.from_dict(response.json())

        return response_403

    if client.raise_on_unexpected_status:
        raise errors.UnexpectedStatus(response.status_code, response.content)
    else:
        return None


def _build_response(
    *, client: AuthenticatedClient | Client, response: httpx.Response
) -> Response[Error | FieldError | UserSkillList]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    *,
    client: AuthenticatedClient | Client,
) -> Response[Error | FieldError | UserSkillList]:
    """List your user skills

     The skills approved for the caller in the caller's org. Each is pinned to a catalog version and its
    SHA-256. When that version is archived or its content no longer matches, the skill is listed as
    `unavailable` and stops applying from the caller's next turn. Requires a signed-in person.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Error | FieldError | UserSkillList]
    """

    kwargs = _get_kwargs()

    response = client.get_httpx_client().request(
        **kwargs,
    )

    return _build_response(client=client, response=response)


def sync(
    *,
    client: AuthenticatedClient | Client,
) -> Error | FieldError | UserSkillList | None:
    """List your user skills

     The skills approved for the caller in the caller's org. Each is pinned to a catalog version and its
    SHA-256. When that version is archived or its content no longer matches, the skill is listed as
    `unavailable` and stops applying from the caller's next turn. Requires a signed-in person.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Error | FieldError | UserSkillList
    """

    return sync_detailed(
        client=client,
    ).parsed


async def asyncio_detailed(
    *,
    client: AuthenticatedClient | Client,
) -> Response[Error | FieldError | UserSkillList]:
    """List your user skills

     The skills approved for the caller in the caller's org. Each is pinned to a catalog version and its
    SHA-256. When that version is archived or its content no longer matches, the skill is listed as
    `unavailable` and stops applying from the caller's next turn. Requires a signed-in person.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Error | FieldError | UserSkillList]
    """

    kwargs = _get_kwargs()

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    *,
    client: AuthenticatedClient | Client,
) -> Error | FieldError | UserSkillList | None:
    """List your user skills

     The skills approved for the caller in the caller's org. Each is pinned to a catalog version and its
    SHA-256. When that version is archived or its content no longer matches, the skill is listed as
    `unavailable` and stops applying from the caller's next turn. Requires a signed-in person.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Error | FieldError | UserSkillList
    """

    return (
        await asyncio_detailed(
            client=client,
        )
    ).parsed
