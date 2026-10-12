from http import HTTPStatus
from typing import Any

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.agent_skill_import_preview import AgentSkillImportPreview
from ...models.agent_skill_import_request import AgentSkillImportRequest
from ...models.agent_skill_import_result import AgentSkillImportResult
from ...models.error import Error
from ...models.field_error import FieldError
from ...models.flat_error import FlatError
from ...types import Response


def _get_kwargs(
    *,
    body: AgentSkillImportRequest,
) -> dict[str, Any]:
    headers: dict[str, Any] = {}

    _kwargs: dict[str, Any] = {
        "method": "post",
        "url": "/v1/skills/import",
    }

    _kwargs["json"] = body.to_dict()

    headers["Content-Type"] = "application/json"

    _kwargs["headers"] = headers
    return _kwargs


def _parse_response(
    *, client: AuthenticatedClient | Client, response: httpx.Response
) -> AgentSkillImportPreview | AgentSkillImportResult | Error | FieldError | FlatError | None:
    if response.status_code == 200:

        def _parse_response_200(data: object) -> AgentSkillImportPreview | AgentSkillImportResult:
            try:
                if not isinstance(data, dict):
                    raise TypeError()
                response_200_type_0 = AgentSkillImportResult.from_dict(data)

                return response_200_type_0
            except (TypeError, ValueError, AttributeError, KeyError):
                pass
            if not isinstance(data, dict):
                raise TypeError()
            response_200_type_1 = AgentSkillImportPreview.from_dict(data)

            return response_200_type_1

        response_200 = _parse_response_200(response.json())

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

    if response.status_code == 422:
        response_422 = FieldError.from_dict(response.json())

        return response_422

    if response.status_code == 502:
        response_502 = FieldError.from_dict(response.json())

        return response_502

    if client.raise_on_unexpected_status:
        raise errors.UnexpectedStatus(response.status_code, response.content)
    else:
        return None


def _build_response(
    *, client: AuthenticatedClient | Client, response: httpx.Response
) -> Response[AgentSkillImportPreview | AgentSkillImportResult | Error | FieldError | FlatError]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    *,
    client: AuthenticatedClient | Client,
    body: AgentSkillImportRequest,
) -> Response[AgentSkillImportPreview | AgentSkillImportResult | Error | FieldError | FlatError]:
    """Import skills from GitHub

     Admin-only. Fetches every skill (folder with a `SKILL.md`) under a GitHub link, at most 50, and
    stores each as a new draft version recording the repository, ref and commit. A repository without a
    licence file is refused. `dry_run: true` returns a preview instead.

    Args:
        body (AgentSkillImportRequest):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[AgentSkillImportPreview | AgentSkillImportResult | Error | FieldError | FlatError]
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
    body: AgentSkillImportRequest,
) -> AgentSkillImportPreview | AgentSkillImportResult | Error | FieldError | FlatError | None:
    """Import skills from GitHub

     Admin-only. Fetches every skill (folder with a `SKILL.md`) under a GitHub link, at most 50, and
    stores each as a new draft version recording the repository, ref and commit. A repository without a
    licence file is refused. `dry_run: true` returns a preview instead.

    Args:
        body (AgentSkillImportRequest):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        AgentSkillImportPreview | AgentSkillImportResult | Error | FieldError | FlatError
    """

    return sync_detailed(
        client=client,
        body=body,
    ).parsed


async def asyncio_detailed(
    *,
    client: AuthenticatedClient | Client,
    body: AgentSkillImportRequest,
) -> Response[AgentSkillImportPreview | AgentSkillImportResult | Error | FieldError | FlatError]:
    """Import skills from GitHub

     Admin-only. Fetches every skill (folder with a `SKILL.md`) under a GitHub link, at most 50, and
    stores each as a new draft version recording the repository, ref and commit. A repository without a
    licence file is refused. `dry_run: true` returns a preview instead.

    Args:
        body (AgentSkillImportRequest):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[AgentSkillImportPreview | AgentSkillImportResult | Error | FieldError | FlatError]
    """

    kwargs = _get_kwargs(
        body=body,
    )

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    *,
    client: AuthenticatedClient | Client,
    body: AgentSkillImportRequest,
) -> AgentSkillImportPreview | AgentSkillImportResult | Error | FieldError | FlatError | None:
    """Import skills from GitHub

     Admin-only. Fetches every skill (folder with a `SKILL.md`) under a GitHub link, at most 50, and
    stores each as a new draft version recording the repository, ref and commit. A repository without a
    licence file is refused. `dry_run: true` returns a preview instead.

    Args:
        body (AgentSkillImportRequest):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        AgentSkillImportPreview | AgentSkillImportResult | Error | FieldError | FlatError
    """

    return (
        await asyncio_detailed(
            client=client,
            body=body,
        )
    ).parsed
