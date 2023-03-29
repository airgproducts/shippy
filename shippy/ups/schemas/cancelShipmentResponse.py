from typing import Optional

from pydantic import BaseModel, Field

from shippy.base.models import CancelShipmentResponseBase


class Status(BaseModel):
    Code: str = Field(..., min_length=1, max_length=1)
    Description: str


class Response(BaseModel):
    ResponseStatus: Status


class SummaryResult(BaseModel):
    Status: Status


class PackageLevelResult(BaseModel):
    Status: Status
    TrackingNumber: str = Field(..., max_length=18)


class VoidShipmentResponse(BaseModel):
    Response: Response
    SummaryResult: SummaryResult
    packageLevelResult: Optional[PackageLevelResult] = Field(
        None, alias="PackageLevelResult"
    )
    # ^ have to use Optional and alias here instead of | None


class CancelShipmentResponseData(BaseModel):
    VoidShipmentResponse: VoidShipmentResponse


class CancelShipmentResponse(CancelShipmentResponseBase[CancelShipmentResponseData]):
    @property
    def cancellation_successful(self) -> bool:
        return (
            self.data.VoidShipmentResponse.Response.ResponseStatus.Code == "1"
            and self.data.VoidShipmentResponse.SummaryResult.Status.Code == "1"
        )
