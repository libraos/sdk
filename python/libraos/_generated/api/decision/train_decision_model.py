from http import HTTPStatus
from typing import Any, cast
from urllib.parse import quote

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.decision_not_better_error import DecisionNotBetterError
from ...models.decision_train_request import DecisionTrainRequest
from ...models.decision_version import DecisionVersion
from ...models.error import Error
from ...models.flat_error import FlatError
from ...types import UNSET, Response, Unset


def _get_kwargs(
    name: str,
    *,
    body: DecisionTrainRequest,
    gate: float | Unset = UNSET,
) -> dict[str, Any]:
    headers: dict[str, Any] = {}

    params: dict[str, Any] = {}

    params["gate"] = gate

    params = {k: v for k, v in params.items() if v is not UNSET and v is not None}

    _kwargs: dict[str, Any] = {
        "method": "post",
        "url": "/v1/decision/{name}/train".format(
            name=quote(str(name), safe=""),
        ),
        "params": params,
    }

    _kwargs["json"] = body.to_dict()

    headers["Content-Type"] = "application/json"

    _kwargs["headers"] = headers
    return _kwargs


def _parse_response(
    *, client: AuthenticatedClient | Client, response: httpx.Response
) -> Any | DecisionNotBetterError | DecisionVersion | Error | FlatError | None:
    if response.status_code == 201:
        response_201 = DecisionVersion.from_dict(response.json())

        return response_201

    if response.status_code == 400:
        response_400 = FlatError.from_dict(response.json())

        return response_400

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
        response_422 = DecisionNotBetterError.from_dict(response.json())

        return response_422

    if response.status_code == 429:
        response_429 = FlatError.from_dict(response.json())

        return response_429

    if client.raise_on_unexpected_status:
        raise errors.UnexpectedStatus(response.status_code, response.content)
    else:
        return None


def _build_response(
    *, client: AuthenticatedClient | Client, response: httpx.Response
) -> Response[Any | DecisionNotBetterError | DecisionVersion | Error | FlatError]:
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
    body: DecisionTrainRequest,
    gate: float | Unset = UNSET,
) -> Response[Any | DecisionNotBetterError | DecisionVersion | Error | FlatError]:
    r"""Train a candidate version

     Fits a calibrated classifier (70/15/15 train/calibrate/test split) and stores it as a **candidate**;
    training never activates a version. A `Content-Type` starting with `application/json` reads `{rows,
    gate}`; any other content type reads JSONL, one `{\"text\",\"label\"}` object per line. Limits: 16
    MB body, 100,000 rows, 2-32 labels, enough rows for 20 calibration and 20 test examples. Training
    rows are not stored. One training run per server instance at a time. Admin, or a connector-role
    service client.

    Args:
        name (str):
        gate (float | Unset):
        body (DecisionTrainRequest):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Any | DecisionNotBetterError | DecisionVersion | Error | FlatError]
    """

    kwargs = _get_kwargs(
        name=name,
        body=body,
        gate=gate,
    )

    response = client.get_httpx_client().request(
        **kwargs,
    )

    return _build_response(client=client, response=response)


def sync(
    name: str,
    *,
    client: AuthenticatedClient | Client,
    body: DecisionTrainRequest,
    gate: float | Unset = UNSET,
) -> Any | DecisionNotBetterError | DecisionVersion | Error | FlatError | None:
    r"""Train a candidate version

     Fits a calibrated classifier (70/15/15 train/calibrate/test split) and stores it as a **candidate**;
    training never activates a version. A `Content-Type` starting with `application/json` reads `{rows,
    gate}`; any other content type reads JSONL, one `{\"text\",\"label\"}` object per line. Limits: 16
    MB body, 100,000 rows, 2-32 labels, enough rows for 20 calibration and 20 test examples. Training
    rows are not stored. One training run per server instance at a time. Admin, or a connector-role
    service client.

    Args:
        name (str):
        gate (float | Unset):
        body (DecisionTrainRequest):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Any | DecisionNotBetterError | DecisionVersion | Error | FlatError
    """

    return sync_detailed(
        name=name,
        client=client,
        body=body,
        gate=gate,
    ).parsed


async def asyncio_detailed(
    name: str,
    *,
    client: AuthenticatedClient | Client,
    body: DecisionTrainRequest,
    gate: float | Unset = UNSET,
) -> Response[Any | DecisionNotBetterError | DecisionVersion | Error | FlatError]:
    r"""Train a candidate version

     Fits a calibrated classifier (70/15/15 train/calibrate/test split) and stores it as a **candidate**;
    training never activates a version. A `Content-Type` starting with `application/json` reads `{rows,
    gate}`; any other content type reads JSONL, one `{\"text\",\"label\"}` object per line. Limits: 16
    MB body, 100,000 rows, 2-32 labels, enough rows for 20 calibration and 20 test examples. Training
    rows are not stored. One training run per server instance at a time. Admin, or a connector-role
    service client.

    Args:
        name (str):
        gate (float | Unset):
        body (DecisionTrainRequest):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Any | DecisionNotBetterError | DecisionVersion | Error | FlatError]
    """

    kwargs = _get_kwargs(
        name=name,
        body=body,
        gate=gate,
    )

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    name: str,
    *,
    client: AuthenticatedClient | Client,
    body: DecisionTrainRequest,
    gate: float | Unset = UNSET,
) -> Any | DecisionNotBetterError | DecisionVersion | Error | FlatError | None:
    r"""Train a candidate version

     Fits a calibrated classifier (70/15/15 train/calibrate/test split) and stores it as a **candidate**;
    training never activates a version. A `Content-Type` starting with `application/json` reads `{rows,
    gate}`; any other content type reads JSONL, one `{\"text\",\"label\"}` object per line. Limits: 16
    MB body, 100,000 rows, 2-32 labels, enough rows for 20 calibration and 20 test examples. Training
    rows are not stored. One training run per server instance at a time. Admin, or a connector-role
    service client.

    Args:
        name (str):
        gate (float | Unset):
        body (DecisionTrainRequest):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Any | DecisionNotBetterError | DecisionVersion | Error | FlatError
    """

    return (
        await asyncio_detailed(
            name=name,
            client=client,
            body=body,
            gate=gate,
        )
    ).parsed
