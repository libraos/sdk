from http import HTTPStatus
from typing import Any

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.error import Error
from ...models.list_registry_agents_response_200 import ListRegistryAgentsResponse200
from ...models.list_registry_agents_response_400 import ListRegistryAgentsResponse400
from ...models.list_registry_agents_source import ListRegistryAgentsSource
from ...types import UNSET, Response, Unset


def _get_kwargs(
    *,
    source: ListRegistryAgentsSource | Unset = UNSET,
) -> dict[str, Any]:

    params: dict[str, Any] = {}

    json_source: str | Unset = UNSET
    if not isinstance(source, Unset):
        json_source = source.value

    params["source"] = json_source

    params = {k: v for k, v in params.items() if v is not UNSET and v is not None}

    _kwargs: dict[str, Any] = {
        "method": "get",
        "url": "/api/agents",
        "params": params,
    }

    return _kwargs


def _parse_response(
    *, client: AuthenticatedClient | Client, response: httpx.Response
) -> Error | ListRegistryAgentsResponse200 | ListRegistryAgentsResponse400 | None:
    if response.status_code == 200:
        response_200 = ListRegistryAgentsResponse200.from_dict(response.json())

        return response_200

    if response.status_code == 400:
        response_400 = ListRegistryAgentsResponse400.from_dict(response.json())

        return response_400

    if response.status_code == 403:
        response_403 = Error.from_dict(response.json())

        return response_403

    if client.raise_on_unexpected_status:
        raise errors.UnexpectedStatus(response.status_code, response.content)
    else:
        return None


def _build_response(
    *, client: AuthenticatedClient | Client, response: httpx.Response
) -> Response[Error | ListRegistryAgentsResponse200 | ListRegistryAgentsResponse400]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    *,
    client: AuthenticatedClient | Client,
    source: ListRegistryAgentsSource | Unset = UNSET,
) -> Response[Error | ListRegistryAgentsResponse200 | ListRegistryAgentsResponse400]:
    """List registry agents (admin)

     Every agent the registry has loaded, with the definition metadata an admin surface needs. Admin
    only.

    Distinct from `GET /v1/agents`, which is the managed-agents endpoint and returns a different,
    smaller shape. That one was documented and this one was not, so consumers reached for it first and
    got a misleading answer (libraos#1351).

    A stock image ships more presets than a tenant has agents of its own, so a caller rendering this
    list unfiltered shows bundled presets as if they belonged to the tenant. Use `source=custom` to
    avoid that.

    Args:
        source (ListRegistryAgentsSource | Unset):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Error | ListRegistryAgentsResponse200 | ListRegistryAgentsResponse400]
    """

    kwargs = _get_kwargs(
        source=source,
    )

    response = client.get_httpx_client().request(
        **kwargs,
    )

    return _build_response(client=client, response=response)


def sync(
    *,
    client: AuthenticatedClient | Client,
    source: ListRegistryAgentsSource | Unset = UNSET,
) -> Error | ListRegistryAgentsResponse200 | ListRegistryAgentsResponse400 | None:
    """List registry agents (admin)

     Every agent the registry has loaded, with the definition metadata an admin surface needs. Admin
    only.

    Distinct from `GET /v1/agents`, which is the managed-agents endpoint and returns a different,
    smaller shape. That one was documented and this one was not, so consumers reached for it first and
    got a misleading answer (libraos#1351).

    A stock image ships more presets than a tenant has agents of its own, so a caller rendering this
    list unfiltered shows bundled presets as if they belonged to the tenant. Use `source=custom` to
    avoid that.

    Args:
        source (ListRegistryAgentsSource | Unset):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Error | ListRegistryAgentsResponse200 | ListRegistryAgentsResponse400
    """

    return sync_detailed(
        client=client,
        source=source,
    ).parsed


async def asyncio_detailed(
    *,
    client: AuthenticatedClient | Client,
    source: ListRegistryAgentsSource | Unset = UNSET,
) -> Response[Error | ListRegistryAgentsResponse200 | ListRegistryAgentsResponse400]:
    """List registry agents (admin)

     Every agent the registry has loaded, with the definition metadata an admin surface needs. Admin
    only.

    Distinct from `GET /v1/agents`, which is the managed-agents endpoint and returns a different,
    smaller shape. That one was documented and this one was not, so consumers reached for it first and
    got a misleading answer (libraos#1351).

    A stock image ships more presets than a tenant has agents of its own, so a caller rendering this
    list unfiltered shows bundled presets as if they belonged to the tenant. Use `source=custom` to
    avoid that.

    Args:
        source (ListRegistryAgentsSource | Unset):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Error | ListRegistryAgentsResponse200 | ListRegistryAgentsResponse400]
    """

    kwargs = _get_kwargs(
        source=source,
    )

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    *,
    client: AuthenticatedClient | Client,
    source: ListRegistryAgentsSource | Unset = UNSET,
) -> Error | ListRegistryAgentsResponse200 | ListRegistryAgentsResponse400 | None:
    """List registry agents (admin)

     Every agent the registry has loaded, with the definition metadata an admin surface needs. Admin
    only.

    Distinct from `GET /v1/agents`, which is the managed-agents endpoint and returns a different,
    smaller shape. That one was documented and this one was not, so consumers reached for it first and
    got a misleading answer (libraos#1351).

    A stock image ships more presets than a tenant has agents of its own, so a caller rendering this
    list unfiltered shows bundled presets as if they belonged to the tenant. Use `source=custom` to
    avoid that.

    Args:
        source (ListRegistryAgentsSource | Unset):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Error | ListRegistryAgentsResponse200 | ListRegistryAgentsResponse400
    """

    return (
        await asyncio_detailed(
            client=client,
            source=source,
        )
    ).parsed
