import requests
from pydantic import HttpUrl
from requests import Response
from requests.auth import HTTPBasicAuth

from .schemas import CreateShipmentRequest


def handle_ups_response(response: Response) -> Response:
    if response.status_code != 200:
        raise ValueError(
            f"UPS create shipment request failed with {response.status_code}: {response.json()}"
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
