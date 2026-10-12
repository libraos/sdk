from http import HTTPStatus
from typing import Any, cast
from urllib.parse import quote

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.agent_skill_edit import AgentSkillEdit
from ...models.agent_skill_write_result import AgentSkillWriteResult
from ...models.error import Error
from ...models.field_error import FieldError
from ...models.flat_error import FlatError
from ...types import Response


def _get_kwargs(
    name: str,
    *,
    body: AgentSkillEdit,
) -> dict[str, Any]:
    headers: dict[str, Any] = {}

    _kwargs: dict[str, Any] = {
        "method": "put",
        "url": "/v1/skills/{name}".format(
            name=quote(str(name), safe=""),
        ),
    }

    _kwargs["json"] = body.to_dict()

    headers["Content-Type"] = "application/json"

    _kwargs["headers"] = headers
    return _kwargs


def _parse_response(
    *, client: AuthenticatedClient | Client, response: httpx.Response
) -> AgentSkillWriteResult | Any | Error | FieldError | FlatError | None:
    if response.status_code == 200:
        response_200 = AgentSkillWriteResult.from_dict(response.json())

        return response_200

    if response.status_code == 201:
        response_201 = AgentSkillWriteResult.from_dict(response.json())

        return response_201

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

    if response.status_code == 413:
        response_413 = cast(Any, None)
        return response_413

    if response.status_code == 422:
        response_422 = FieldError.from_dict(response.json())

        return response_422

    if client.raise_on_unexpected_status:
        raise errors.UnexpectedStatus(response.status_code, response.content)
    else:
        return None


def _build_response(
    *, client: AuthenticatedClient | Client, response: httpx.Response
) -> Response[AgentSkillWriteResult | Any | Error | FieldError | FlatError]:
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
    body: AgentSkillEdit,
) -> Response[AgentSkillWriteResult | Any | Error | FieldError | FlatError]:
    """Save an edited skill as a new draft version

     Admin-only. Never overwrites a version: the files become a new draft (`source.kind: edit`). The
    `SKILL.md` frontmatter name must stay the path name. Identical content returns the latest version
    with 200.

    Args:
        name (str):
        body (AgentSkillEdit):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[AgentSkillWriteResult | Any | Error | FieldError | FlatError]
    """

    kwargs = _get_kwargs(
        name=name,
        body=body,
    )

    response = client.get_httpx_client().request(
        **kwargs,
    )

    return _build_response(client=client, response=response)


def sync(
    name: str,
    *,
    client: AuthenticatedClient | Client,
    body: AgentSkillEdit,
) -> AgentSkillWriteResult | Any | Error | FieldError | FlatError | None:
    """Save an edited skill as a new draft version

     Admin-only. Never overwrites a version: the files become a new draft (`source.kind: edit`). The
    `SKILL.md` frontmatter name must stay the path name. Identical content returns the latest version
    with 200.

    Args:
        name (str):
        body (AgentSkillEdit):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        AgentSkillWriteResult | Any | Error | FieldError | FlatError
    """

    return sync_detailed(
        name=name,
        client=client,
        body=body,
    ).parsed


async def asyncio_detailed(
    name: str,
    *,
    client: AuthenticatedClient | Client,
    body: AgentSkillEdit,
) -> Response[AgentSkillWriteResult | Any | Error | FieldError | FlatError]:
    """Save an edited skill as a new draft version

     Admin-only. Never overwrites a version: the files become a new draft (`source.kind: edit`). The
    `SKILL.md` frontmatter name must stay the path name. Identical content returns the latest version
    with 200.

    Args:
        name (str):
        body (AgentSkillEdit):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[AgentSkillWriteResult | Any | Error | FieldError | FlatError]
    """

    kwargs = _get_kwargs(
        name=name,
        body=body,
    )

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    name: str,
    *,
    client: AuthenticatedClient | Client,
    body: AgentSkillEdit,
) -> AgentSkillWriteResult | Any | Error | FieldError | FlatError | None:
    """Save an edited skill as a new draft version

     Admin-only. Never overwrites a version: the files become a new draft (`source.kind: edit`). The
    `SKILL.md` frontmatter name must stay the path name. Identical content returns the latest version
    with 200.

    Args:
        name (str):
        body (AgentSkillEdit):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        AgentSkillWriteResult | Any | Error | FieldError | FlatError
    """

    return (
        await asyncio_detailed(
            name=name,
            client=client,
            body=body,
        )
    ).parsed
