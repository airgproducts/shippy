from shippy.base.client import BaseClient
from shippy.base.schemas import Shipment

from .config import Config
from .requests import cancel_parcel_by_id_f116, create_parcels_f114
from .schemas import CancelShipmentResponse, CreateShipmentRequest, CreateShipmentResponse


class Client(BaseClient):
    config: Config

    def __init__(self, config: Config | None = None):
        super().__init__(config, Config)

    @property
    def headers(self) -> dict[str, str]:
        return {
            "Content-Type": "application/glsVersion1+json",
            "Accept": "application/glsVersion1+json, application/json",
        }

    def ship(self, shipment: Shipment) -> CreateShipmentResponse:
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

    def cancel_shipment(self, tracking_id: str):
        response = cancel_parcel_by_id_f116(
            base_url=self.config.base_url,
            headers=self.headers,
            auth=self.config.auth,
            parcel_id=tracking_id,
        )
        return CancelShipmentResponse(**response.json())
