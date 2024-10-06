import datetime
import uuid

from shippy.base.client import BaseClient
from shippy.base.schemas import Shipment

from .config import Config
from .requests import (
    cancel_shipment,
    create_shipment,
    create_token,
    paperless_document_image,
    paperless_document_upload,
    rate_shipment,
)
from .schemas import (
    CancelShipmentResponse,
    CreateShipmentRequest,
    CreateShipmentResponse,
    CreateTokenRequest,
    CreateTokenResponse,
    ImageFileSchema,
    PaperlessDocumentImageRequestSchema,
    PaperlessDocumentImageResponseSchema,
    PaperlessDocumentUploadRequestSchema,
    PaperlessDocumentUploadResponseSchema,
    RateShipmentRequest,
    RateShipmentResponse,
    ServiceEnum,
    UploadFileSchema,
)


class UPSClient(BaseClient):
    config: Config
    name = "UPS"
    bearer_token: CreateTokenResponse | None = None

    def __init__(self, config: Config | None = None):
        super().__init__(config, Config)

    def get_bearer_token(self) -> CreateTokenResponse:
        if (
            self.bearer_token
            and self.bearer_token.expires_in_datetime
            > datetime.datetime.now(tz=datetime.UTC)
        ):
            return self.bearer_token
        token = self.create_token()
        self.bearer_token = token
        return token

    @property
    def headers(self, with_token=False) -> dict[str, str]:
        return {
            "Authorization": f"Bearer {self.get_bearer_token().access_token}",
            "transID": str(uuid.uuid4()),
            "transactionSrc": "shippy",
        }

    def create_shipment_request(
        self, shipment: Shipment, service: ServiceEnum
    ) -> CreateShipmentRequest:
        return CreateShipmentRequest.from_generic_schemas(
            shipment_reference=shipment.reference,
            parcel=shipment.parcel,
            to_address=shipment.to_address,
            from_address=shipment.from_address,
            service_code=service,
            config=self.config,
        )

    def ship(
        self, shipment: Shipment | CreateShipmentRequest, service: ServiceEnum
    ) -> CreateShipmentResponse:
        if isinstance(shipment, CreateShipmentRequest):
            ups_schema = shipment
        else:
            ups_schema = self.create_shipment_request(shipment, service)

        response = create_shipment(
            base_url=self.config.base_url,
            headers=self.headers,
            schema=ups_schema,
        )
        return CreateShipmentResponse(data=response.json())

    def rate(self, shipment: Shipment) -> RateShipmentResponse:
        # TODO: implement tracking with new UPS api
        raise NotImplementedError
        schema = RateShipmentRequest.from_generic_schemas(
            parcel=shipment.parcel,
            to_address=shipment.to_address,
            from_address=shipment.from_address,
            config=self.config,
        )
        response = rate_shipment(
            base_url=self.config.base_url,
            headers=self.headers,
            schema=schema,
            request_option="Shop",
        )
        return RateShipmentResponse(data=response.json())

    def cancel_shipment(self, tracking_id: str) -> CancelShipmentResponse:
        response = cancel_shipment(
            base_url=self.config.base_url,
            headers=self.headers,
            shipment_id=tracking_id,
        )
        return CancelShipmentResponse(data=response.json())

    def create_token(self) -> CreateTokenResponse:
        schema = CreateTokenRequest(grant_type="client_credentials")
        response = create_token(
            schema=schema,
            base_url=self.config.base_url,
            auth=self.config.auth,
            account_number=self.config.account_number,
        )
        return CreateTokenResponse(**response.json())

    def paperless_document_upload(
        self, files: list[UploadFileSchema]
    ) -> PaperlessDocumentUploadResponseSchema:
        schema = PaperlessDocumentUploadRequestSchema.create(
            shipper_number=self.config.account_number, files=files
        )
        response = paperless_document_upload(
            schema=schema,
            base_url=self.config.base_url,
            headers=self.headers,
        )
        return PaperlessDocumentUploadResponseSchema(**response.json())

    def paperless_document_image(
        self, data: ImageFileSchema
    ) -> PaperlessDocumentImageResponseSchema:
        schema = PaperlessDocumentImageRequestSchema.create(
            data=data, shipper_number=self.config.account_number
        )
        response = paperless_document_image(
            schema=schema,
            base_url=self.config.base_url,
            headers=self.headers,
        )

        return PaperlessDocumentImageResponseSchema(**response.json())

    @staticmethod
    def get_tracking_link(tracking_id: str):
        return (
            f"http://wwwapps.ups.com/WebTracking/track?track=yes&trackNums={tracking_id}"
        )
