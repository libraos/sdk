from http import HTTPStatus
from typing import Any
from urllib.parse import quote

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.agent_skill_diff import AgentSkillDiff
from ...models.error import Error
from ...models.field_error import FieldError
from ...types import UNSET, Response


def _get_kwargs(
    name: str,
    *,
    from_: int,
    to: int,
) -> dict[str, Any]:

    params: dict[str, Any] = {}

    params["from"] = from_

    params["to"] = to

    params = {k: v for k, v in params.items() if v is not UNSET and v is not None}

    _kwargs: dict[str, Any] = {
        "method": "get",
        "url": "/v1/skills/{name}/diff".format(
            name=quote(str(name), safe=""),
        ),
        "params": params,
    }

    return _kwargs


def _parse_response(
    *, client: AuthenticatedClient | Client, response: httpx.Response
) -> AgentSkillDiff | Error | FieldError | None:
    if response.status_code == 200:
        response_200 = AgentSkillDiff.from_dict(response.json())

        return response_200

    if response.status_code == 400:
        response_400 = FieldError.from_dict(response.json())

        return response_400

    if response.status_code == 401:
        response_401 = Error.from_dict(response.json())

        return response_401

    if response.status_code == 404:
        response_404 = FieldError.from_dict(response.json())

        return response_404

    if client.raise_on_unexpected_status:
        raise errors.UnexpectedStatus(response.status_code, response.content)
    else:
        return None


def _build_response(
    *, client: AuthenticatedClient | Client, response: httpx.Response
) -> Response[AgentSkillDiff | Error | FieldError]:
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
    from_: int,
    to: int,
) -> Response[AgentSkillDiff | Error | FieldError]:
    """Diff two versions of a skill

     Any authenticated caller; organization-scoped.

    Args:
        name (str):
        from_ (int):
        to (int):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[AgentSkillDiff | Error | FieldError]
    """

    kwargs = _get_kwargs(
        name=name,
        from_=from_,
        to=to,
    )

    response = client.get_httpx_client().request(
        **kwargs,
    )

    return _build_response(client=client, response=response)


def sync(
    name: str,
    *,
    client: AuthenticatedClient | Client,
    from_: int,
    to: int,
) -> AgentSkillDiff | Error | FieldError | None:
    """Diff two versions of a skill

     Any authenticated caller; organization-scoped.

    Args:
        name (str):
        from_ (int):
        to (int):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        AgentSkillDiff | Error | FieldError
    """

    return sync_detailed(
        name=name,
        client=client,
        from_=from_,
        to=to,
    ).parsed


async def asyncio_detailed(
    name: str,
    *,
    client: AuthenticatedClient | Client,
    from_: int,
    to: int,
) -> Response[AgentSkillDiff | Error | FieldError]:
    """Diff two versions of a skill

     Any authenticated caller; organization-scoped.

    Args:
        name (str):
        from_ (int):
        to (int):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[AgentSkillDiff | Error | FieldError]
    """

    kwargs = _get_kwargs(
        name=name,
        from_=from_,
        to=to,
    )

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    name: str,
    *,
    client: AuthenticatedClient | Client,
    from_: int,
    to: int,
) -> AgentSkillDiff | Error | FieldError | None:
    """Diff two versions of a skill

     Any authenticated caller; organization-scoped.

    Args:
        name (str):
        from_ (int):
        to (int):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        AgentSkillDiff | Error | FieldError
    """

    return (
        await asyncio_detailed(
            name=name,
            client=client,
            from_=from_,
            to=to,
        )
    ).parsed
