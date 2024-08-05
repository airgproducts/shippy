import base64
from typing import Literal, Optional

from pydantic import BaseModel, Field

from shippy.base.models import CreateShipmentResponseBase

_UNIT_OF_MEASUREMENT_OPTIONS = Literal["LBS", "KGS"]
_IMAGE_FORMAT_OPTIONS = Literal["EPL", "SPL", "ZPL", "GIF"]


class ResponseStatus(BaseModel):
    Code: str = Field(..., max_length=1)
    Description: str = Field(..., max_length=35)


class TransactionReference(BaseModel):
    CustomerContext: str = Field(..., max_length=512)
    TransactionIdentifier: str


class Response(BaseModel):
    ResponseStatus: ResponseStatus
    transactionReference: Optional[TransactionReference] = Field(
        None, alias="TransactionReference"
    )
    # ^ have to use Optional and alias here instead of | None


class Charges(BaseModel):
    CurrencyCode: str = Field(..., max_length=3)
    MonetaryValue: str = Field(..., max_length=19)
    # TODO: validate monetary value


class ShipmentCharges(BaseModel):
    TransportationCharges: Charges
    ServiceOptionsCharges: Charges
    TotalCharges: Charges


class UnitOfMeasurement(BaseModel):
    Code: _UNIT_OF_MEASUREMENT_OPTIONS
    Description: str | None = Field(None, max_length=35)


class BillingWeight(BaseModel):
    UnitOfMeasurement: UnitOfMeasurement
    Weight: str = Field(..., max_length=8)


class ImageFormat(BaseModel):
    Code: _IMAGE_FORMAT_OPTIONS
    Description: str = Field(..., max_length=35)


class ShippingLabel(BaseModel):
    ImageFormat: ImageFormat
    GraphicImage: str
    HtMLImage: str | None = None


class PackageResults(BaseModel):
    TrackingNumber: str = Field(..., max_length=18)
    ServiceOptionsCharges: Charges
    ShippingLabel: ShippingLabel


class ShipmentResults(BaseModel):
    ShipmentCharges: ShipmentCharges
    BillingWeight: BillingWeight
    ShipmentIdentificationNumber: str = Field(..., max_length=18)
    PackageResults: list[PackageResults]


class ShipmentResponse(BaseModel):
    Response: Response
    ShipmentResults: ShipmentResults


class CreateShipmentResponseData(BaseModel):
    ShipmentResponse: ShipmentResponse


class CreateShipmentResponse(CreateShipmentResponseBase[CreateShipmentResponseData]):
    @property
    def tracking_id(self) -> str:
        return self.data.ShipmentResponse.ShipmentResults.PackageResults[0].TrackingNumber

    @property
    def _label(self) -> str:
        return self.data.ShipmentResponse.ShipmentResults.PackageResults[
            0
        ].ShippingLabel.GraphicImage
