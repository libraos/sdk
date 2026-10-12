from http import HTTPStatus
from typing import Any
from urllib.parse import quote

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.decision_model import DecisionModel
from ...models.error import Error
from ...models.flat_error import FlatError
from ...types import Response


def _get_kwargs(
    name: str,
) -> dict[str, Any]:

    _kwargs: dict[str, Any] = {
        "method": "get",
        "url": "/v1/decision/{name}".format(
            name=quote(str(name), safe=""),
        ),
    }

    return _kwargs


def _parse_response(
    *, client: AuthenticatedClient | Client, response: httpx.Response
) -> DecisionModel | Error | FlatError | None:
    if response.status_code == 200:
        response_200 = DecisionModel.from_dict(response.json())

        return response_200

    if response.status_code == 400:
        response_400 = FlatError.from_dict(response.json())

        return response_400

    if response.status_code == 401:
        response_401 = Error.from_dict(response.json())

        return response_401

    if response.status_code == 403:
        response_403 = FlatError.from_dict(response.json())

        return response_403

    if response.status_code == 404:
        response_404 = FlatError.from_dict(response.json())

        return response_404

    if client.raise_on_unexpected_status:
        raise errors.UnexpectedStatus(response.status_code, response.content)
    else:
        return None


def _build_response(
    *, client: AuthenticatedClient | Client, response: httpx.Response
) -> Response[DecisionModel | Error | FlatError]:
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
) -> Response[DecisionModel | Error | FlatError]:
    """List a decision probe's versions

     Named, calibrated text classifiers a client can consult before falling back to its own model: trust
    a prediction whose confidence clears the version's gate, send the rest to the fallback. Admin, or a
    connector-role service client. Registered only when `LIBRA_OS_DECISION_API_ENABLED` is on and
    PostgreSQL is configured; otherwise the routes answer 404.

    Args:
        name (str):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[DecisionModel | Error | FlatError]
    """

    kwargs = _get_kwargs(
        name=name,
    )

    response = client.get_httpx_client().request(
        **kwargs,
    )

    return _build_response(client=client, response=response)


def sync(
    name: str,
    *,
    client: AuthenticatedClient | Client,
) -> DecisionModel | Error | FlatError | None:
    """List a decision probe's versions

     Named, calibrated text classifiers a client can consult before falling back to its own model: trust
    a prediction whose confidence clears the version's gate, send the rest to the fallback. Admin, or a
    connector-role service client. Registered only when `LIBRA_OS_DECISION_API_ENABLED` is on and
    PostgreSQL is configured; otherwise the routes answer 404.

    Args:
        name (str):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        DecisionModel | Error | FlatError
    """

    return sync_detailed(
        name=name,
        client=client,
    ).parsed


async def asyncio_detailed(
    name: str,
    *,
    client: AuthenticatedClient | Client,
) -> Response[DecisionModel | Error | FlatError]:
    """List a decision probe's versions

     Named, calibrated text classifiers a client can consult before falling back to its own model: trust
    a prediction whose confidence clears the version's gate, send the rest to the fallback. Admin, or a
    connector-role service client. Registered only when `LIBRA_OS_DECISION_API_ENABLED` is on and
    PostgreSQL is configured; otherwise the routes answer 404.

    Args:
        name (str):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[DecisionModel | Error | FlatError]
    """

    kwargs = _get_kwargs(
        name=name,
    )

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    name: str,
    *,
    client: AuthenticatedClient | Client,
) -> DecisionModel | Error | FlatError | None:
    """List a decision probe's versions

     Named, calibrated text classifiers a client can consult before falling back to its own model: trust
    a prediction whose confidence clears the version's gate, send the rest to the fallback. Admin, or a
    connector-role service client. Registered only when `LIBRA_OS_DECISION_API_ENABLED` is on and
    PostgreSQL is configured; otherwise the routes answer 404.

    Args:
        name (str):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        DecisionModel | Error | FlatError
    """

    return (
        await asyncio_detailed(
            name=name,
            client=client,
        )
    ).parsed
