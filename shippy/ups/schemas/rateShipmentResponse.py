from decimal import Decimal

from pydantic import BaseModel

from shippy.ups.schemas.base import ServiceCodeEnum


class ResponseStatus(BaseModel):
    Code: str
    Description: str


class Alert(BaseModel):
    Code: str
    Description: str


class TransactionReference(BaseModel):
    CustomerContext: str
    TransactionIdentifier: str


class Response(BaseModel):
    ResponseStatus: ResponseStatus
    Alert: list[Alert]
    TransactionReference: TransactionReference


class Service(BaseModel):
    Code: str
    Description: str


class RatedShipmentAlert(BaseModel):
    Code: str
    Description: str


class UnitOfMeasurement(BaseModel):
    Code: str
    Description: str


class BillingWeight(BaseModel):
    UnitOfMeasurement: UnitOfMeasurement
    Weight: str


class TransportationCharge(BaseModel):
    CurrencyCode: str
    MonetaryValue: str


class RatedPackage(BaseModel):
    Weight: str


class RatedShipment(BaseModel):
    Service: Service
    RatedShipmentAlert: list[RatedShipmentAlert]
    BillingWeight: BillingWeight
    TransportationCharges: TransportationCharge
    ServiceOptionsCharges: TransportationCharge
    TotalCharges: TransportationCharge
    RatedPackage: RatedPackage


class RateResponse(BaseModel):
    Response: Response
    RatedShipment: list[RatedShipment]


class RateShipmentResponseData(BaseModel):
    RateResponse: RateResponse


class ServicePrice(BaseModel):
    currency_code: str
    value: Decimal


class RateShipmentResponse(BaseModel):
    data: RateShipmentResponseData

    @property
    def service_prices(self) -> dict[ServiceCodeEnum, ServicePrice]:
        return {
            ServiceCodeEnum(entry.Service.Code): ServicePrice(
                currency_code=entry.TotalCharges.CurrencyCode,
                value=entry.TotalCharges.MonetaryValue,
            )
            for entry in self.data.RateResponse.RatedShipment
        }
