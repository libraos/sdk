from http import HTTPStatus
from typing import Any
from urllib.parse import quote

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.error import Error
from ...models.field_error import FieldError
from ...models.flat_error import FlatError
from ...models.skill_request_approval import SkillRequestApproval
from ...models.skill_request_envelope import SkillRequestEnvelope
from ...types import Response


def _get_kwargs(
    id: str,
    *,
    body: SkillRequestApproval,
) -> dict[str, Any]:
    headers: dict[str, Any] = {}

    _kwargs: dict[str, Any] = {
        "method": "post",
        "url": "/v1/managed/skill-requests/{id}/approve".format(
            id=quote(str(id), safe=""),
        ),
    }

    _kwargs["json"] = body.to_dict()

    headers["Content-Type"] = "application/json"

    _kwargs["headers"] = headers
    return _kwargs


def _parse_response(
    *, client: AuthenticatedClient | Client, response: httpx.Response
) -> Error | FieldError | FlatError | SkillRequestEnvelope | None:
    if response.status_code == 200:
        response_200 = SkillRequestEnvelope.from_dict(response.json())

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
) -> Response[Error | FieldError | FlatError | SkillRequestEnvelope]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    id: str,
    *,
    client: AuthenticatedClient | Client,
    body: SkillRequestApproval,
) -> Response[Error | FieldError | FlatError | SkillRequestEnvelope]:
    """Approve a pending skill request

     Admin-only. Reads exactly `commit`, the commit the preview returned, and imports the chosen skills'
    instructions into the org catalog through the `/v1/skills` import path: the source is pinned to that
    commit and the licence is recorded. Scripts and binary files are left out. It then publishes the
    versions and activates them for the requester only. A link that yields several importable skills
    needs `skills`. Approval never changes what an existing skill name means for the org's agents: a
    name the org already uses (a catalog version in any status, or a `LIBRA_OS_SKILLS_DIR` folder) is
    refused, unless identical content is already published, in which case that version is reused and
    nothing is written. To give someone an update to a skill the org already has, publish it through
    `/v1/skills` first, then approve. At most 10 active user skills per person.

    Args:
        id (str):
        body (SkillRequestApproval):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Error | FieldError | FlatError | SkillRequestEnvelope]
    """

    kwargs = _get_kwargs(
        id=id,
        body=body,
    )

    response = client.get_httpx_client().request(
        **kwargs,
    )

    return _build_response(client=client, response=response)


def sync(
    id: str,
    *,
    client: AuthenticatedClient | Client,
    body: SkillRequestApproval,
) -> Error | FieldError | FlatError | SkillRequestEnvelope | None:
    """Approve a pending skill request

     Admin-only. Reads exactly `commit`, the commit the preview returned, and imports the chosen skills'
    instructions into the org catalog through the `/v1/skills` import path: the source is pinned to that
    commit and the licence is recorded. Scripts and binary files are left out. It then publishes the
    versions and activates them for the requester only. A link that yields several importable skills
    needs `skills`. Approval never changes what an existing skill name means for the org's agents: a
    name the org already uses (a catalog version in any status, or a `LIBRA_OS_SKILLS_DIR` folder) is
    refused, unless identical content is already published, in which case that version is reused and
    nothing is written. To give someone an update to a skill the org already has, publish it through
    `/v1/skills` first, then approve. At most 10 active user skills per person.

    Args:
        id (str):
        body (SkillRequestApproval):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Error | FieldError | FlatError | SkillRequestEnvelope
    """

    return sync_detailed(
        id=id,
        client=client,
        body=body,
    ).parsed


async def asyncio_detailed(
    id: str,
    *,
    client: AuthenticatedClient | Client,
    body: SkillRequestApproval,
) -> Response[Error | FieldError | FlatError | SkillRequestEnvelope]:
    """Approve a pending skill request

     Admin-only. Reads exactly `commit`, the commit the preview returned, and imports the chosen skills'
    instructions into the org catalog through the `/v1/skills` import path: the source is pinned to that
    commit and the licence is recorded. Scripts and binary files are left out. It then publishes the
    versions and activates them for the requester only. A link that yields several importable skills
    needs `skills`. Approval never changes what an existing skill name means for the org's agents: a
    name the org already uses (a catalog version in any status, or a `LIBRA_OS_SKILLS_DIR` folder) is
    refused, unless identical content is already published, in which case that version is reused and
    nothing is written. To give someone an update to a skill the org already has, publish it through
    `/v1/skills` first, then approve. At most 10 active user skills per person.

    Args:
        id (str):
        body (SkillRequestApproval):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Error | FieldError | FlatError | SkillRequestEnvelope]
    """

    kwargs = _get_kwargs(
        id=id,
        body=body,
    )

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    id: str,
    *,
    client: AuthenticatedClient | Client,
    body: SkillRequestApproval,
) -> Error | FieldError | FlatError | SkillRequestEnvelope | None:
    """Approve a pending skill request

     Admin-only. Reads exactly `commit`, the commit the preview returned, and imports the chosen skills'
    instructions into the org catalog through the `/v1/skills` import path: the source is pinned to that
    commit and the licence is recorded. Scripts and binary files are left out. It then publishes the
    versions and activates them for the requester only. A link that yields several importable skills
    needs `skills`. Approval never changes what an existing skill name means for the org's agents: a
    name the org already uses (a catalog version in any status, or a `LIBRA_OS_SKILLS_DIR` folder) is
    refused, unless identical content is already published, in which case that version is reused and
    nothing is written. To give someone an update to a skill the org already has, publish it through
    `/v1/skills` first, then approve. At most 10 active user skills per person.

    Args:
        id (str):
        body (SkillRequestApproval):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Error | FieldError | FlatError | SkillRequestEnvelope
    """

    return (
        await asyncio_detailed(
            id=id,
            client=client,
            body=body,
        )
    ).parsed
