import requests
from pydantic import HttpUrl
from requests import Response
from requests.auth import HTTPBasicAuth

from .schemas import CreateShipmentRequest


def handle_gls_response(response: Response, error_message: str) -> Response:
    if response.status_code != 200:
        try:
            message = response.headers["message"]
        except KeyError:
            message = response.headers
        raise ValueError(f"{error_message} {response.status_code}: {message}")
    return response


def create_parcels_f114(
    base_url: HttpUrl,
    headers: dict[str, str],
    auth: HTTPBasicAuth,
    schema: CreateShipmentRequest,
):
    # https://shipit.gls-group.eu/webservices/3_2_9/doxygen/WS-REST-API/rest_shipment_processing.html#REST_API_REST_F_114
    sub_url = "/shipments"
    response = requests.post(
        base_url + sub_url,
        headers=headers,
        json=schema.dict(exclude_none=True),
        auth=auth,
    )
    return handle_gls_response(response, "GLS create shipment request failed with")


def cancel_parcel_by_id_f116(
    base_url: HttpUrl,
    headers: dict[str, str],
    auth: HTTPBasicAuth,
    parcel_id: str,
):
    # https://shipit.gls-group.eu/webservices/3_2_9/doxygen/WS-REST-API/rest_shipment_processing.html#REST_API_REST_F_116
    sub_url = f"/shipments/cancel/{parcel_id}"
    response = requests.post(
        base_url + sub_url,
        headers=headers,
        auth=auth,
    )
    return handle_gls_response(response, "GLS cancel shipment request failed with")
