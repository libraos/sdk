from http import HTTPStatus
from typing import Any, cast
from urllib.parse import quote

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.error import Error
from ...models.field_error import FieldError
from ...models.flat_error import FlatError
from ...types import UNSET, Response


def _get_kwargs(
    name: str,
    *,
    user_id: str,
) -> dict[str, Any]:

    params: dict[str, Any] = {}

    params["user_id"] = user_id

    params = {k: v for k, v in params.items() if v is not UNSET and v is not None}

    _kwargs: dict[str, Any] = {
        "method": "delete",
        "url": "/v1/managed/user-skills/{name}".format(
            name=quote(str(name), safe=""),
        ),
        "params": params,
    }

    return _kwargs


def _parse_response(
    *, client: AuthenticatedClient | Client, response: httpx.Response
) -> Any | Error | FieldError | FlatError | None:
    if response.status_code == 204:
        response_204 = cast(Any, None)
        return response_204

    if response.status_code == 400:
        response_400 = FieldError.from_dict(response.json())

        return response_400

    if response.status_code == 401:
        response_401 = Error.from_dict(response.json())

        return response_401

    if response.status_code == 403:
        response_403 = FlatError.from_dict(response.json())

        return response_403

    if response.status_code == 404:
        response_404 = FieldError.from_dict(response.json())

        return response_404

    if client.raise_on_unexpected_status:
        raise errors.UnexpectedStatus(response.status_code, response.content)
    else:
        return None


def _build_response(
    *, client: AuthenticatedClient | Client, response: httpx.Response
) -> Response[Any | Error | FieldError | FlatError]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    name: str,
    *,
    client: AuthenticatedClient | Client,
    user_id: str,
) -> Response[Any | Error | FieldError | FlatError]:
    """Remove a person's user skill

     Admin-only. Removes the skill from the person named by `user_id`, in the admin's org, whether it is
    `active` or `unavailable`. It stops applying from their next turn. The catalog version, the request
    and other people's skills are unchanged. Each removal is recorded as an audit event (namespace
    `user_skills`, event `user_skill.removed`).

    Args:
        name (str):
        user_id (str):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Any | Error | FieldError | FlatError]
    """

    kwargs = _get_kwargs(
        name=name,
        user_id=user_id,
    )

    response = client.get_httpx_client().request(
        **kwargs,
    )

    return _build_response(client=client, response=response)


def sync(
    name: str,
    *,
    client: AuthenticatedClient | Client,
    user_id: str,
) -> Any | Error | FieldError | FlatError | None:
    """Remove a person's user skill

     Admin-only. Removes the skill from the person named by `user_id`, in the admin's org, whether it is
    `active` or `unavailable`. It stops applying from their next turn. The catalog version, the request
    and other people's skills are unchanged. Each removal is recorded as an audit event (namespace
    `user_skills`, event `user_skill.removed`).

    Args:
        name (str):
        user_id (str):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Any | Error | FieldError | FlatError
    """

    return sync_detailed(
        name=name,
        client=client,
        user_id=user_id,
    ).parsed


async def asyncio_detailed(
    name: str,
    *,
    client: AuthenticatedClient | Client,
    user_id: str,
) -> Response[Any | Error | FieldError | FlatError]:
    """Remove a person's user skill

     Admin-only. Removes the skill from the person named by `user_id`, in the admin's org, whether it is
    `active` or `unavailable`. It stops applying from their next turn. The catalog version, the request
    and other people's skills are unchanged. Each removal is recorded as an audit event (namespace
    `user_skills`, event `user_skill.removed`).

    Args:
        name (str):
        user_id (str):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Any | Error | FieldError | FlatError]
    """

    kwargs = _get_kwargs(
        name=name,
        user_id=user_id,
    )

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    name: str,
    *,
    client: AuthenticatedClient | Client,
    user_id: str,
) -> Any | Error | FieldError | FlatError | None:
    """Remove a person's user skill

     Admin-only. Removes the skill from the person named by `user_id`, in the admin's org, whether it is
    `active` or `unavailable`. It stops applying from their next turn. The catalog version, the request
    and other people's skills are unchanged. Each removal is recorded as an audit event (namespace
    `user_skills`, event `user_skill.removed`).

    Args:
        name (str):
        user_id (str):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Any | Error | FieldError | FlatError
    """

    return (
        await asyncio_detailed(
            name=name,
            client=client,
            user_id=user_id,
        )
    ).parsed
