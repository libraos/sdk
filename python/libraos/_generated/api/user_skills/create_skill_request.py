from http import HTTPStatus
from typing import Any

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.error import Error
from ...models.field_error import FieldError
from ...models.skill_request_create import SkillRequestCreate
from ...models.skill_request_write_result import SkillRequestWriteResult
from ...types import Response


def _get_kwargs(
    *,
    body: SkillRequestCreate,
) -> dict[str, Any]:
    headers: dict[str, Any] = {}

    _kwargs: dict[str, Any] = {
        "method": "post",
        "url": "/v1/skill-requests",
    }

    _kwargs["json"] = body.to_dict()

    headers["Content-Type"] = "application/json"

    _kwargs["headers"] = headers
    return _kwargs


def _parse_response(
    *, client: AuthenticatedClient | Client, response: httpx.Response
) -> Error | FieldError | SkillRequestWriteResult | None:
    if response.status_code == 200:
        response_200 = SkillRequestWriteResult.from_dict(response.json())

        return response_200

    if response.status_code == 201:
        response_201 = SkillRequestWriteResult.from_dict(response.json())

        return response_201

    if response.status_code == 400:
        response_400 = FieldError.from_dict(response.json())

        return response_400

    if response.status_code == 401:
        response_401 = Error.from_dict(response.json())

        return response_401

    if response.status_code == 403:
        response_403 = FieldError.from_dict(response.json())

        return response_403

    if response.status_code == 409:
        response_409 = FieldError.from_dict(response.json())

        return response_409

    if client.raise_on_unexpected_status:
        raise errors.UnexpectedStatus(response.status_code, response.content)
    else:
        return None


def _build_response(
    *, client: AuthenticatedClient | Client, response: httpx.Response
) -> Response[Error | FieldError | SkillRequestWriteResult]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    *,
    client: AuthenticatedClient | Client,
    body: SkillRequestCreate,
) -> Response[Error | FieldError | SkillRequestWriteResult]:
    """Request a skill for your own copilot

     Asks an admin of the caller's org for an Agent Skill from a GitHub link, for the caller's own
    copilot. Nothing is fetched here: only an admin's preview or approval reads the link. If the caller
    already has a pending request for the same link, in any accepted form, it is returned with 200 and
    `created: false`. At most 10 pending requests per person. Once approved, the skill applies only to
    the caller's own interactive chat turns in this org, on `/v1/messages` and
    `/agents/v1/{api_key}/chat` (with its `/v1/apps/{app}/agents/{id}/chat` alias). It never applies on
    `/v1/chat/completions`, to service clients or API keys, or in async jobs and schedules, and an
    agent's own skill of the same name wins. Requires a signed-in person: service clients and API keys
    get 403. Registered only on deployments with PostgreSQL; otherwise every user-skills route answers
    404.

    Args:
        body (SkillRequestCreate):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Error | FieldError | SkillRequestWriteResult]
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
    body: SkillRequestCreate,
) -> Error | FieldError | SkillRequestWriteResult | None:
    """Request a skill for your own copilot

     Asks an admin of the caller's org for an Agent Skill from a GitHub link, for the caller's own
    copilot. Nothing is fetched here: only an admin's preview or approval reads the link. If the caller
    already has a pending request for the same link, in any accepted form, it is returned with 200 and
    `created: false`. At most 10 pending requests per person. Once approved, the skill applies only to
    the caller's own interactive chat turns in this org, on `/v1/messages` and
    `/agents/v1/{api_key}/chat` (with its `/v1/apps/{app}/agents/{id}/chat` alias). It never applies on
    `/v1/chat/completions`, to service clients or API keys, or in async jobs and schedules, and an
    agent's own skill of the same name wins. Requires a signed-in person: service clients and API keys
    get 403. Registered only on deployments with PostgreSQL; otherwise every user-skills route answers
    404.

    Args:
        body (SkillRequestCreate):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Error | FieldError | SkillRequestWriteResult
    """

    return sync_detailed(
        client=client,
        body=body,
    ).parsed


async def asyncio_detailed(
    *,
    client: AuthenticatedClient | Client,
    body: SkillRequestCreate,
) -> Response[Error | FieldError | SkillRequestWriteResult]:
    """Request a skill for your own copilot

     Asks an admin of the caller's org for an Agent Skill from a GitHub link, for the caller's own
    copilot. Nothing is fetched here: only an admin's preview or approval reads the link. If the caller
    already has a pending request for the same link, in any accepted form, it is returned with 200 and
    `created: false`. At most 10 pending requests per person. Once approved, the skill applies only to
    the caller's own interactive chat turns in this org, on `/v1/messages` and
    `/agents/v1/{api_key}/chat` (with its `/v1/apps/{app}/agents/{id}/chat` alias). It never applies on
    `/v1/chat/completions`, to service clients or API keys, or in async jobs and schedules, and an
    agent's own skill of the same name wins. Requires a signed-in person: service clients and API keys
    get 403. Registered only on deployments with PostgreSQL; otherwise every user-skills route answers
    404.

    Args:
        body (SkillRequestCreate):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Error | FieldError | SkillRequestWriteResult]
    """

    kwargs = _get_kwargs(
        body=body,
    )

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    *,
    client: AuthenticatedClient | Client,
    body: SkillRequestCreate,
) -> Error | FieldError | SkillRequestWriteResult | None:
    """Request a skill for your own copilot

     Asks an admin of the caller's org for an Agent Skill from a GitHub link, for the caller's own
    copilot. Nothing is fetched here: only an admin's preview or approval reads the link. If the caller
    already has a pending request for the same link, in any accepted form, it is returned with 200 and
    `created: false`. At most 10 pending requests per person. Once approved, the skill applies only to
    the caller's own interactive chat turns in this org, on `/v1/messages` and
    `/agents/v1/{api_key}/chat` (with its `/v1/apps/{app}/agents/{id}/chat` alias). It never applies on
    `/v1/chat/completions`, to service clients or API keys, or in async jobs and schedules, and an
    agent's own skill of the same name wins. Requires a signed-in person: service clients and API keys
    get 403. Registered only on deployments with PostgreSQL; otherwise every user-skills route answers
    404.

    Args:
        body (SkillRequestCreate):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Error | FieldError | SkillRequestWriteResult
    """

    return (
        await asyncio_detailed(
            client=client,
            body=body,
        )
    ).parsed
