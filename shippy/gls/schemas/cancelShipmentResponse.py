from pydantic import BaseModel

from shippy.base.models import CancelShipmentResponseBase


class CancelShipmentResponseData(BaseModel):
    TrackID: str
    result: str


class CancelShipmentResponse(CancelShipmentResponseBase[CancelShipmentResponseData]):
    @property
    def cancellation_successful(self) -> bool:
        return (
            self.data.result == "CANCELLED" or self.data.result == "CANCELLATION_PENDING"
        )
