from datetime import datetime

from shippy.base.client import BaseClient
from shippy.base.schemas import Shipment

from .config import Config
from .requests import (
    cancel_parcel_by_id_f116,
    create_parcels_f114,
    get_estimated_delivery_days_f234,
)
from .schemas import (
    CancelShipmentResponse,
    CreateShipmentRequest,
    CreateShipmentResponse,
    RateShipmentRequest,
    RateShipmentResponse,
    ServiceEnum,
)


class GLSClient(BaseClient):
    config: Config
    name = "GLS"

    def __init__(self, config: Config | None = None):
        super().__init__(config, Config)

    @property
    def headers(self) -> dict[str, str]:
        return {
            "Content-Type": "application/glsVersion1+json",
            "Accept": "application/glsVersion1+json, application/json",
        }

    def ship(
        self,
        shipment: Shipment,
        service: ServiceEnum = ServiceEnum.GLS_STANDARD,
    ) -> CreateShipmentResponse:
        schema = CreateShipmentRequest.from_generic_schemas(
            shipment_reference=shipment.reference,
            contact_id=self.config.contact_id,
            parcel=shipment.parcel,
            to_address=shipment.to_address,
            from_address=shipment.from_address,
        )
        response = create_parcels_f114(
            base_url=self.config.base_url,
            headers=self.headers,
            auth=self.config.auth,
            schema=schema,
        )
        return CreateShipmentResponse(data=response.json())

    def rate(self, shipment: Shipment) -> RateShipmentResponse:
        # TODO: GLS rating does not work anymore with 404
        raise NotImplementedError
        schema = RateShipmentRequest.from_generic_schema(
            from_address=shipment.from_address, to_address=shipment.to_address
        )
        request_date = datetime.now()
        response = get_estimated_delivery_days_f234(
            base_url=self.config.base_url,
            headers=self.headers,
            auth=self.config.auth,
            schema=schema,
        )
        return RateShipmentResponse(data=response.json(), requested_at=request_date)

    def cancel_shipment(self, tracking_id: str) -> CancelShipmentResponse:
        response = cancel_parcel_by_id_f116(
            base_url=self.config.base_url,
            headers=self.headers,
            auth=self.config.auth,
            parcel_id=tracking_id,
        )
        return CancelShipmentResponse(data=response.json())

    @staticmethod
    def get_tracking_link(tracking_id: str) -> str:
        return f"https://gls-group.eu/track/{tracking_id}"
