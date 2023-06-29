from json import JSONDecodeError
from typing import Literal

import requests
from pydantic import HttpUrl
from requests import Response
from requests.auth import HTTPBasicAuth

from shippy.base.errors import ShippyAPIError

from .schemas import CreateShipmentRequest, RateShipmentRequest

_REQUEST_OPTION_CHOICES = Literal["Rate", "Shop"]


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
    auth: HTTPBasicAuth,
    schema: CreateShipmentRequest,
):
    sub_url = "/shipments"
    response = requests.post(
        base_url + sub_url,
        headers=headers,
        json=schema.dict(exclude_none=True),
        auth=auth,
    )
    return handle_ups_response(response)


def rate_shipment(
    base_url: HttpUrl,
    headers: dict[str, str],
    auth: HTTPBasicAuth,
    schema: RateShipmentRequest,
    request_option: _REQUEST_OPTION_CHOICES,
):
    sub_url = f"/rating/{request_option}"
    response = requests.post(
        base_url + sub_url,
        headers=headers,
        json=schema.dict(exclude_none=True),
        auth=auth,
    )
    return handle_ups_response(response)


def cancel_shipment(
    base_url: HttpUrl,
    headers: dict[str, str],
    auth: HTTPBasicAuth,
    shipment_id: str,
):
    sub_url = f"/shipments/cancel/{shipment_id}"
    response = requests.delete(
        base_url + sub_url,
        headers=headers,
        auth=auth,
    )
    return handle_ups_response(response)
