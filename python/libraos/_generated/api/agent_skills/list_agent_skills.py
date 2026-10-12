from http import HTTPStatus
from typing import Any

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.agent_skill_list import AgentSkillList
from ...models.error import Error
from ...types import Response


def _get_kwargs() -> dict[str, Any]:

    _kwargs: dict[str, Any] = {
        "method": "get",
        "url": "/v1/skills",
    }

    return _kwargs


def _parse_response(*, client: AuthenticatedClient | Client, response: httpx.Response) -> AgentSkillList | Error | None:
    if response.status_code == 200:
        response_200 = AgentSkillList.from_dict(response.json())

        return response_200

    if response.status_code == 401:
        response_401 = Error.from_dict(response.json())

        return response_401

    if client.raise_on_unexpected_status:
        raise errors.UnexpectedStatus(response.status_code, response.content)
    else:
        return None


def _build_response(
    *, client: AuthenticatedClient | Client, response: httpx.Response
) -> Response[AgentSkillList | Error]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    *,
    client: AuthenticatedClient | Client,
) -> Response[AgentSkillList | Error]:
    """List Agent Skills in the catalog

     Any authenticated caller; scoped to the caller's organization. Agents attach skills by name through
    `agent_skills`. The catalog is registered only on deployments with PostgreSQL; otherwise every
    `/v1/skills` route answers 404.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[AgentSkillList | Error]
    """

    kwargs = _get_kwargs()

    response = client.get_httpx_client().request(
        **kwargs,
    )

    return _build_response(client=client, response=response)


def sync(
    *,
    client: AuthenticatedClient | Client,
) -> AgentSkillList | Error | None:
    """List Agent Skills in the catalog

     Any authenticated caller; scoped to the caller's organization. Agents attach skills by name through
    `agent_skills`. The catalog is registered only on deployments with PostgreSQL; otherwise every
    `/v1/skills` route answers 404.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        AgentSkillList | Error
    """

    return sync_detailed(
        client=client,
    ).parsed


async def asyncio_detailed(
    *,
    client: AuthenticatedClient | Client,
) -> Response[AgentSkillList | Error]:
    """List Agent Skills in the catalog

     Any authenticated caller; scoped to the caller's organization. Agents attach skills by name through
    `agent_skills`. The catalog is registered only on deployments with PostgreSQL; otherwise every
    `/v1/skills` route answers 404.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[AgentSkillList | Error]
    """

    kwargs = _get_kwargs()

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    *,
    client: AuthenticatedClient | Client,
) -> AgentSkillList | Error | None:
    """List Agent Skills in the catalog

     Any authenticated caller; scoped to the caller's organization. Agents attach skills by name through
    `agent_skills`. The catalog is registered only on deployments with PostgreSQL; otherwise every
    `/v1/skills` route answers 404.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        AgentSkillList | Error
    """

    return (
        await asyncio_detailed(
            client=client,
        )
    ).parsed
