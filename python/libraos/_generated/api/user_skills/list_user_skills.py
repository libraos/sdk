from http import HTTPStatus
from typing import Any

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.error import Error
from ...models.field_error import FieldError
from ...models.flat_error import FlatError
from ...models.managed_user_skill_list import ManagedUserSkillList
from ...types import UNSET, Response, Unset


def _get_kwargs(
    *,
    user_id: str | Unset = UNSET,
    name: str | Unset = UNSET,
    limit: int | Unset = UNSET,
) -> dict[str, Any]:

    params: dict[str, Any] = {}

    params["user_id"] = user_id

    params["name"] = name

    params["limit"] = limit

    params = {k: v for k, v in params.items() if v is not UNSET and v is not None}

    _kwargs: dict[str, Any] = {
        "method": "get",
        "url": "/v1/managed/user-skills",
        "params": params,
    }

    return _kwargs


def _parse_response(
    *, client: AuthenticatedClient | Client, response: httpx.Response
) -> Error | FieldError | FlatError | ManagedUserSkillList | None:
    if response.status_code == 200:
        response_200 = ManagedUserSkillList.from_dict(response.json())

        return response_200

    if response.status_code == 400:
        response_400 = FieldError.from_dict(response.json())

        return response_400

    if response.status_code == 401:
        response_401 = Error.from_dict(response.json())

        return response_401

    if response.status_code == 403:
        response_403 = FlatError.from_dict(response.json())

        return response_403

    if client.raise_on_unexpected_status:
        raise errors.UnexpectedStatus(response.status_code, response.content)
    else:
        return None


def _build_response(
    *, client: AuthenticatedClient | Client, response: httpx.Response
) -> Response[Error | FieldError | FlatError | ManagedUserSkillList]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    *,
    client: AuthenticatedClient | Client,
    user_id: str | Unset = UNSET,
    name: str | Unset = UNSET,
    limit: int | Unset = UNSET,
) -> Response[Error | FieldError | FlatError | ManagedUserSkillList]:
    """List the org's user skills

     Admin-only. The user skills of everyone in the admin's org, by `user_id` and then `name`. Each item
    is what that person's `GET /v1/user-skills` shows, plus `user_id`, so a skill whose version was
    archived is listed as `unavailable` with a `reason`.

    Args:
        user_id (str | Unset):
        name (str | Unset):
        limit (int | Unset):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Error | FieldError | FlatError | ManagedUserSkillList]
    """

    kwargs = _get_kwargs(
        user_id=user_id,
        name=name,
        limit=limit,
    )

    response = client.get_httpx_client().request(
        **kwargs,
    )

    return _build_response(client=client, response=response)


def sync(
    *,
    client: AuthenticatedClient | Client,
    user_id: str | Unset = UNSET,
    name: str | Unset = UNSET,
    limit: int | Unset = UNSET,
) -> Error | FieldError | FlatError | ManagedUserSkillList | None:
    """List the org's user skills

     Admin-only. The user skills of everyone in the admin's org, by `user_id` and then `name`. Each item
    is what that person's `GET /v1/user-skills` shows, plus `user_id`, so a skill whose version was
    archived is listed as `unavailable` with a `reason`.

    Args:
        user_id (str | Unset):
        name (str | Unset):
        limit (int | Unset):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Error | FieldError | FlatError | ManagedUserSkillList
    """

    return sync_detailed(
        client=client,
        user_id=user_id,
        name=name,
        limit=limit,
    ).parsed


async def asyncio_detailed(
    *,
    client: AuthenticatedClient | Client,
    user_id: str | Unset = UNSET,
    name: str | Unset = UNSET,
    limit: int | Unset = UNSET,
) -> Response[Error | FieldError | FlatError | ManagedUserSkillList]:
    """List the org's user skills

     Admin-only. The user skills of everyone in the admin's org, by `user_id` and then `name`. Each item
    is what that person's `GET /v1/user-skills` shows, plus `user_id`, so a skill whose version was
    archived is listed as `unavailable` with a `reason`.

    Args:
        user_id (str | Unset):
        name (str | Unset):
        limit (int | Unset):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Error | FieldError | FlatError | ManagedUserSkillList]
    """

    kwargs = _get_kwargs(
        user_id=user_id,
        name=name,
        limit=limit,
    )

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    *,
    client: AuthenticatedClient | Client,
    user_id: str | Unset = UNSET,
    name: str | Unset = UNSET,
    limit: int | Unset = UNSET,
) -> Error | FieldError | FlatError | ManagedUserSkillList | None:
    """List the org's user skills

     Admin-only. The user skills of everyone in the admin's org, by `user_id` and then `name`. Each item
    is what that person's `GET /v1/user-skills` shows, plus `user_id`, so a skill whose version was
    archived is listed as `unavailable` with a `reason`.

    Args:
        user_id (str | Unset):
        name (str | Unset):
        limit (int | Unset):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Error | FieldError | FlatError | ManagedUserSkillList
    """

    return (
        await asyncio_detailed(
            client=client,
            user_id=user_id,
            name=name,
            limit=limit,
        )
    ).parsed
