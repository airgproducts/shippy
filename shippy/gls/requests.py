import requests
from pydantic import HttpUrl
from requests import Response
from requests.auth import HTTPBasicAuth

from shippy.base.errors import ShippyAPIError

from .schemas import CreateShipmentRequest, RateShipmentRequest


def handle_gls_response(response: Response, error_message: str) -> Response:
    if response.status_code != 200:
        try:
            message = str(response.headers["message"])
        except KeyError:
            message = str(response.headers)
        if response.text:
            message += " " + response.text
        raise ShippyAPIError(f"{error_message} {response.status_code}: {message}")
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
        str(base_url) + sub_url,
        headers=headers,
        json=schema.model_dump(exclude_none=True, by_alias=True),
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
        str(base_url) + sub_url,
        headers=headers,
        auth=auth,
    )
    return handle_gls_response(response, "GLS cancel shipment request failed with")


def get_estimated_delivery_days_f234(
    base_url: HttpUrl,
    headers: dict[str, str],
    auth: HTTPBasicAuth,
    schema: RateShipmentRequest,
):
    # https://shipit.gls-group.eu/webservices/3_2_9/doxygen/WS-REST-API/rest_timeframe.html#REST_API_REST_TF_1
    sub_url = f"/timeframe/deliverydays"
    response = requests.post(
        str(base_url) + sub_url,
        headers=headers,
        json=schema.model_dump(exclude_none=True, by_alias=True),
        auth=auth,
    )
    return handle_gls_response(response, "GLS get estimated delivery days failed with")
