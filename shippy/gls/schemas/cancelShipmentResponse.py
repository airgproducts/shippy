from pydantic import BaseModel


class CancelShipmentResponseData(BaseModel):
    TrackID: str
    result: str


class CancelShipmentResponse(BaseModel):
    data: CancelShipmentResponseData
