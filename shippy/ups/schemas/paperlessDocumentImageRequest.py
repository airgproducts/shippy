from datetime import datetime
from typing import Literal, Optional

from pydantic import BaseModel, Field

DATETIME_REGEX = r"\d{4}-(0[1-9]|1[0-2])-(0[1-9]|[12][0-9]|3[01])-(0[0-9]|1[0-9]|2[0-3])\.(0[0-9]|[1-5][0-9])\.(0[0-9]|[1-5][0-9])"


class ImageFileSchema(BaseModel):
    # for user-friendly schema creation
    document_id: str
    shipment_datetime: datetime
    shipment_identifier: str
    tracking_number: str


class TransactionReferenceSchema(BaseModel):
    CustomerContext: str


class RequestSchema(BaseModel):
    TransactionReference: TransactionReferenceSchema | None = None


class FormsHistoryDocumentIDSchema(BaseModel):
    DocumentID: str


class PushToImageRepositoryRequestSchema(BaseModel):
    Request: RequestSchema
    FormsHistoryDocumentID: FormsHistoryDocumentIDSchema
    ShipmentIdentifier: str
    ShipmentDateAndTime: str = Field(regex=DATETIME_REGEX)
    ShipmentType: Literal["1", "2"]
    TrackingNumber: str
    ShipperNumber: str = Field(..., min_length=6, max_length=6)

    @staticmethod
    def datetime_to_string(datetime_object: datetime) -> str:
        return datetime_object.strftime("%Y-%m-%d-%H.%M.%S")


class PaperlessDocumentImageRequestSchema(BaseModel):
    PushToImageRepositoryRequest: PushToImageRepositoryRequestSchema

    @classmethod
    def create(cls, data: ImageFileSchema, shipper_number: str):
        return cls(
            PushToImageRepositoryRequest=PushToImageRepositoryRequestSchema(
                Request=RequestSchema(),
                FormsHistoryDocumentID=FormsHistoryDocumentIDSchema(
                    DocumentID=data.document_id,
                ),
                ShipmentIdentifier=data.shipment_identifier,
                ShipmentDateAndTime=PushToImageRepositoryRequestSchema.datetime_to_string(
                    data.shipment_datetime
                ),
                ShipmentType="1",  # for small packages
                TrackingNumber=data.tracking_number,
                ShipperNumber=shipper_number,
            )
        )
