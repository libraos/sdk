from http import HTTPStatus
from typing import Any, cast
from urllib.parse import quote

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.decision_predict_request import DecisionPredictRequest
from ...models.decision_predict_result import DecisionPredictResult
from ...models.error import Error
from ...models.flat_error import FlatError
from ...types import Response


def _get_kwargs(
    name: str,
    *,
    body: DecisionPredictRequest,
) -> dict[str, Any]:
    headers: dict[str, Any] = {}

    _kwargs: dict[str, Any] = {
        "method": "post",
        "url": "/v1/decision/{name}/predict".format(
            name=quote(str(name), safe=""),
        ),
    }

    _kwargs["json"] = body.to_dict()

    headers["Content-Type"] = "application/json"

    _kwargs["headers"] = headers
    return _kwargs


def _parse_response(
    *, client: AuthenticatedClient | Client, response: httpx.Response
) -> Any | DecisionPredictResult | Error | FlatError | None:
    if response.status_code == 200:
        response_200 = DecisionPredictResult.from_dict(response.json())

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

    if response.status_code == 413:
        response_413 = cast(Any, None)
        return response_413

    if client.raise_on_unexpected_status:
        raise errors.UnexpectedStatus(response.status_code, response.content)
    else:
        return None


def _build_response(
    *, client: AuthenticatedClient | Client, response: httpx.Response
) -> Response[Any | DecisionPredictResult | Error | FlatError]:
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
    body: DecisionPredictRequest,
) -> Response[Any | DecisionPredictResult | Error | FlatError]:
    r"""Classify texts

     Classifies up to 1000 texts with `version`, or the active version when omitted. A 404 means \"no
    usable model — use your fallback\". Admin, or a connector-role service client.

    Args:
        name (str):
        body (DecisionPredictRequest):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Any | DecisionPredictResult | Error | FlatError]
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
    body: DecisionPredictRequest,
) -> Any | DecisionPredictResult | Error | FlatError | None:
    r"""Classify texts

     Classifies up to 1000 texts with `version`, or the active version when omitted. A 404 means \"no
    usable model — use your fallback\". Admin, or a connector-role service client.

    Args:
        name (str):
        body (DecisionPredictRequest):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Any | DecisionPredictResult | Error | FlatError
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
    body: DecisionPredictRequest,
) -> Response[Any | DecisionPredictResult | Error | FlatError]:
    r"""Classify texts

     Classifies up to 1000 texts with `version`, or the active version when omitted. A 404 means \"no
    usable model — use your fallback\". Admin, or a connector-role service client.

    Args:
        name (str):
        body (DecisionPredictRequest):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Any | DecisionPredictResult | Error | FlatError]
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
    body: DecisionPredictRequest,
) -> Any | DecisionPredictResult | Error | FlatError | None:
    r"""Classify texts

     Classifies up to 1000 texts with `version`, or the active version when omitted. A 404 means \"no
    usable model — use your fallback\". Admin, or a connector-role service client.

    Args:
        name (str):
        body (DecisionPredictRequest):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Any | DecisionPredictResult | Error | FlatError
    """

    return (
        await asyncio_detailed(
            name=name,
            client=client,
            body=body,
        )
    ).parsed
