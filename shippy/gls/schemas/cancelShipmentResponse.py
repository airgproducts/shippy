from pydantic import BaseModel


class CancelShipmentResponse(BaseModel):
    TrackID: str
    result: str
