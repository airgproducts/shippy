import uuid

from shippy.base.client import BaseClient
from shippy.base.schemas import Shipment

from .config import Config
from .requests import create_shipment
from .schemas import CreateShipmentRequest, CreateShipmentResponse, ServiceCodeEnum


class Client(BaseClient):
    config: Config

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

    def ship(
        self, shipment: Shipment, service_code: ServiceCodeEnum
    ) -> CreateShipmentResponse:
        schema = CreateShipmentRequest.from_generic_schemas(
            shipment_reference=shipment.reference,
            parcel=shipment.parcel,
            to_address=shipment.to_address,
            from_address=shipment.from_address,
            account_number=self.config.account_number,
            service_code=service_code,
        )
        response = create_shipment(
            base_url=self.config.base_url,
            headers=self.headers,
            auth=self.config.auth,
            schema=schema,
        )
        return CreateShipmentResponse(data=response.json())