from pydantic import BaseModel

from shippy.base.models import CreateShipmentResponseBase


class ParcelData(BaseModel):
    TrackID: str
    ParcelNumber: str


class PrintData(BaseModel):
    Data: str
    LabelFormat: str


class CreatedShipment(BaseModel):
    ShipmentReference: list[str]
    ParcelData: list[ParcelData]
    PrintData: list[PrintData]
    CustomerID: str
    PickupLocation: str


class CreateShipmentResponseData(BaseModel):
    CreatedShipment: CreatedShipment


class CreateShipmentResponse(CreateShipmentResponseBase[CreateShipmentResponseData]):
    @property
    def tracking_id(self) -> str:
        return self.data.CreatedShipment.ParcelData[0].TrackID

    @property
    def _label(self) -> str:
        return self.data.CreatedShipment.PrintData[0].Data
