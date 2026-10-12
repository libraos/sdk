from http import HTTPStatus
from typing import Any, cast

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.agent_skill_files import AgentSkillFiles
from ...models.agent_skill_write_result import AgentSkillWriteResult
from ...models.create_agent_skill_files_body import CreateAgentSkillFilesBody
from ...models.error import Error
from ...models.field_error import FieldError
from ...models.flat_error import FlatError
from ...types import UNSET, Response


def _get_kwargs(
    *,
    body: AgentSkillFiles | CreateAgentSkillFilesBody | Unset = UNSET,
) -> dict[str, Any]:
    headers: dict[str, Any] = {}

    _kwargs: dict[str, Any] = {
        "method": "post",
        "url": "/v1/skills",
    }

    if isinstance(body, AgentSkillFiles):
        _kwargs["json"] = body.to_dict()

        headers["Content-Type"] = "application/json"
    if isinstance(body, CreateAgentSkillFilesBody):
        _kwargs["files"] = body.to_multipart()

        headers["Content-Type"] = "multipart/form-data"

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

    if response.status_code == 401:
        response_401 = Error.from_dict(response.json())

        return response_401

    if response.status_code == 403:
        response_403 = FlatError.from_dict(response.json())

        return response_403

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
    *,
    client: AuthenticatedClient | Client,
    body: AgentSkillFiles | CreateAgentSkillFilesBody | Unset = UNSET,
) -> Response[AgentSkillWriteResult | Any | Error | FieldError | FlatError]:
    """Upload a skill version

     Admin-only. Body is either JSON `{files}` or multipart with a `file` field holding a `SKILL.md` (a
    filename ending `.md`) or a zip (at most 8 MiB, 200 files; a single shared top-level folder is
    stripped). The skill name comes from the `SKILL.md` frontmatter. A new version always starts as
    `draft`. Content identical to the latest non-archived version returns that version with 200 and
    `created: false`. Request body limit 10 MB (413).

    Args:
        body (AgentSkillFiles):
        body (CreateAgentSkillFilesBody):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[AgentSkillWriteResult | Any | Error | FieldError | FlatError]
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
    body: AgentSkillFiles | CreateAgentSkillFilesBody | Unset = UNSET,
) -> AgentSkillWriteResult | Any | Error | FieldError | FlatError | None:
    """Upload a skill version

     Admin-only. Body is either JSON `{files}` or multipart with a `file` field holding a `SKILL.md` (a
    filename ending `.md`) or a zip (at most 8 MiB, 200 files; a single shared top-level folder is
    stripped). The skill name comes from the `SKILL.md` frontmatter. A new version always starts as
    `draft`. Content identical to the latest non-archived version returns that version with 200 and
    `created: false`. Request body limit 10 MB (413).

    Args:
        body (AgentSkillFiles):
        body (CreateAgentSkillFilesBody):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        AgentSkillWriteResult | Any | Error | FieldError | FlatError
    """

    return sync_detailed(
        client=client,
        body=body,
    ).parsed


async def asyncio_detailed(
    *,
    client: AuthenticatedClient | Client,
    body: AgentSkillFiles | CreateAgentSkillFilesBody | Unset = UNSET,
) -> Response[AgentSkillWriteResult | Any | Error | FieldError | FlatError]:
    """Upload a skill version

     Admin-only. Body is either JSON `{files}` or multipart with a `file` field holding a `SKILL.md` (a
    filename ending `.md`) or a zip (at most 8 MiB, 200 files; a single shared top-level folder is
    stripped). The skill name comes from the `SKILL.md` frontmatter. A new version always starts as
    `draft`. Content identical to the latest non-archived version returns that version with 200 and
    `created: false`. Request body limit 10 MB (413).

    Args:
        body (AgentSkillFiles):
        body (CreateAgentSkillFilesBody):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[AgentSkillWriteResult | Any | Error | FieldError | FlatError]
    """

    kwargs = _get_kwargs(
        body=body,
    )

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    *,
    client: AuthenticatedClient | Client,
    body: AgentSkillFiles | CreateAgentSkillFilesBody | Unset = UNSET,
) -> AgentSkillWriteResult | Any | Error | FieldError | FlatError | None:
    """Upload a skill version

     Admin-only. Body is either JSON `{files}` or multipart with a `file` field holding a `SKILL.md` (a
    filename ending `.md`) or a zip (at most 8 MiB, 200 files; a single shared top-level folder is
    stripped). The skill name comes from the `SKILL.md` frontmatter. A new version always starts as
    `draft`. Content identical to the latest non-archived version returns that version with 200 and
    `created: false`. Request body limit 10 MB (413).

    Args:
        body (AgentSkillFiles):
        body (CreateAgentSkillFilesBody):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        AgentSkillWriteResult | Any | Error | FieldError | FlatError
    """

    return (
        await asyncio_detailed(
            client=client,
            body=body,
        )
    ).parsed
