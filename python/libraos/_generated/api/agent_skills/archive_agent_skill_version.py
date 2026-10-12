from http import HTTPStatus
from typing import Any
from urllib.parse import quote

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.agent_skill_version import AgentSkillVersion
from ...models.error import Error
from ...models.field_error import FieldError
from ...models.flat_error import FlatError
from ...types import Response


def _get_kwargs(
    name: str,
    version: int,
) -> dict[str, Any]:

    _kwargs: dict[str, Any] = {
        "method": "post",
        "url": "/v1/skills/{name}/versions/{version}/archive".format(
            name=quote(str(name), safe=""),
            version=quote(str(version), safe=""),
        ),
    }

    return _kwargs


def _parse_response(
    *, client: AuthenticatedClient | Client, response: httpx.Response
) -> AgentSkillVersion | Error | FieldError | FlatError | None:
    if response.status_code == 200:
        response_200 = AgentSkillVersion.from_dict(response.json())

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

    if response.status_code == 404:
        response_404 = FieldError.from_dict(response.json())

        return response_404

    if response.status_code == 409:
        response_409 = FieldError.from_dict(response.json())

        return response_409

    if client.raise_on_unexpected_status:
        raise errors.UnexpectedStatus(response.status_code, response.content)
    else:
        return None


def _build_response(
    *, client: AuthenticatedClient | Client, response: httpx.Response
) -> Response[AgentSkillVersion | Error | FieldError | FlatError]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    name: str,
    version: int,
    *,
    client: AuthenticatedClient | Client,
) -> Response[AgentSkillVersion | Error | FieldError | FlatError]:
    """Archive a version

     Admin-only. Allowed from `draft` or `published`; archived is final.

    Args:
        name (str):
        version (int):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[AgentSkillVersion | Error | FieldError | FlatError]
    """

    kwargs = _get_kwargs(
        name=name,
        version=version,
    )

    response = client.get_httpx_client().request(
        **kwargs,
    )

    return _build_response(client=client, response=response)


def sync(
    name: str,
    version: int,
    *,
    client: AuthenticatedClient | Client,
) -> AgentSkillVersion | Error | FieldError | FlatError | None:
    """Archive a version

     Admin-only. Allowed from `draft` or `published`; archived is final.

    Args:
        name (str):
        version (int):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        AgentSkillVersion | Error | FieldError | FlatError
    """

    return sync_detailed(
        name=name,
        version=version,
        client=client,
    ).parsed


async def asyncio_detailed(
    name: str,
    version: int,
    *,
    client: AuthenticatedClient | Client,
) -> Response[AgentSkillVersion | Error | FieldError | FlatError]:
    """Archive a version

     Admin-only. Allowed from `draft` or `published`; archived is final.

    Args:
        name (str):
        version (int):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[AgentSkillVersion | Error | FieldError | FlatError]
    """

    kwargs = _get_kwargs(
        name=name,
        version=version,
    )

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    name: str,
    version: int,
    *,
    client: AuthenticatedClient | Client,
) -> AgentSkillVersion | Error | FieldError | FlatError | None:
    """Archive a version

     Admin-only. Allowed from `draft` or `published`; archived is final.

    Args:
        name (str):
        version (int):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        AgentSkillVersion | Error | FieldError | FlatError
    """

    return (
        await asyncio_detailed(
            name=name,
            version=version,
            client=client,
        )
    ).parsed
