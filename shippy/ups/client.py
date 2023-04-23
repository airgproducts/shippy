import uuid

from shippy.base.client import BaseClient
from shippy.base.schemas import Shipment

from .config import Config
from .requests import cancel_shipment, create_shipment, rate_shipment
from .schemas import (
    CancelShipmentResponse,
    CreateShipmentRequest,
    CreateShipmentResponse,
    RateShipmentRequest,
    RateShipmentResponse,
    ServiceEnum,
)


class UPSClient(BaseClient):
    config: Config
    name = "UPS"

    def __init__(self, config: Config | None = None):
        super().__init__(config, Config)

    @property
    def headers(self) -> dict[str, str]:
        return {
            "AccessLicenseNumber": self.config.key,
            "transID": str(uuid.uuid4()),
            "transactionSrc": "shippy",
            "Username": self.config.user,
            "Password": self.config.password,
        }
    
    def create_shipment_request(self, shipment: Shipment, service: ServiceEnum) -> CreateShipmentRequest:
        return CreateShipmentRequest.from_generic_schemas(
                shipment_reference=shipment.reference,
                parcel=shipment.parcel,
                to_address=shipment.to_address,
                from_address=shipment.from_address,
                account_number=self.config.account_number,
                service_code=service,
            )


    def ship(self, shipment: Shipment | CreateShipmentRequest, service: ServiceEnum) -> CreateShipmentResponse:
        if isinstance(shipment, CreateShipmentRequest):
            ups_schema = shipment
        else:
            ups_schema = self.create_shipment_request(shipment, service)

        response = create_shipment(
            base_url=self.config.base_url,
            headers=self.headers,
            auth=self.config.auth,
            schema=ups_schema,
        )
        return CreateShipmentResponse(data=response.json())

    def rate(self, shipment: Shipment) -> RateShipmentResponse:
        schema = RateShipmentRequest.from_generic_schemas(
            parcel=shipment.parcel,
            to_address=shipment.to_address,
            from_address=shipment.from_address,
        )
        response = rate_shipment(
            base_url=self.config.base_url,
            headers=self.headers,
            auth=self.config.auth,
            schema=schema,
            request_option="Shop",
        )
        return RateShipmentResponse(data=response.json())

    def cancel_shipment(self, tracking_id: str) -> CancelShipmentResponse:
        response = cancel_shipment(
            base_url=self.config.base_url,
            headers=self.headers,
            auth=self.config.auth,
            shipment_id=tracking_id,
        )
        return CancelShipmentResponse(data=response.json())

    @staticmethod
    def get_tracking_link(tracking_id: str):
        return (
            f"http://wwwapps.ups.com/WebTracking/track?track=yes&trackNums={tracking_id}"
        )
