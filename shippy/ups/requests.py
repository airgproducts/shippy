from json import JSONDecodeError
from typing import Literal

import requests
from pydantic import HttpUrl
from requests import Response
from requests.auth import HTTPBasicAuth

from shippy.base.errors import ShippyAPIError

from .schemas import CreateShipmentRequest, CreateTokenRequest, RateShipmentRequest

_REQUEST_OPTION_CHOICES = Literal["Rate", "Shop"]
_TIMEOUT = 5
_REQUEST_KWARGS = {"timeout": _TIMEOUT}


def handle_ups_response(response: Response) -> Response:
    if response.status_code != 200:
        try:
            message = response.json()
        except JSONDecodeError:
            message = response.content
        raise ShippyAPIError(
            f"UPS create shipment request failed with {response.status_code}: {message}"
        )
    return response


def create_shipment(
    base_url: HttpUrl,
    headers: dict[str, str],
    schema: CreateShipmentRequest,
):
    sub_url = "api/shipments/v2403/ship"
    response = requests.post(
        base_url + sub_url,
        headers=headers,
        json=schema.dict(exclude_none=True),
        **_REQUEST_KWARGS,
    )
    print(response.json())
    return handle_ups_response(response)


def rate_shipment(
    base_url: HttpUrl,
    headers: dict[str, str],
    schema: RateShipmentRequest,
    request_option: _REQUEST_OPTION_CHOICES,
):
    sub_url = f"rating/{request_option}"
    response = requests.post(
        base_url + sub_url,
        headers=headers,
        json=schema.dict(exclude_none=True),
        **_REQUEST_KWARGS,
    )
    return handle_ups_response(response)


def cancel_shipment(
    base_url: HttpUrl,
    headers: dict[str, str],
    shipment_id: str,
):
    sub_url = f"api/shipments/v2403/void/cancel/{shipment_id}"
    response = requests.delete(
        base_url + sub_url,
        headers=headers,
        **_REQUEST_KWARGS,
    )
    return handle_ups_response(response)


def create_token(
    base_url: HttpUrl,
    account_number: str,
    auth: HTTPBasicAuth,
    schema: CreateTokenRequest,
):
    sub_url = f"security/v1/oauth/token"
    headers = {
        "Content-Type": "application/x-www-form-urlencoded",
        "x-merchant-id": account_number,
    }
    response = requests.post(
        str(base_url) + sub_url,
        headers=headers,
        auth=auth,
        data=schema.dict(exclude_none=True),
        **_REQUEST_KWARGS,
    )
    return handle_ups_response(response)
