from typing import Literal

from pydantic import BaseModel

_PARCEL_WEIGHT_UNIT_CHOICES = Literal["LBS", "KGS", "OZS"]
_PARCEL_VOLUME_UNIT_CHOICES = Literal["L"]


class Address(BaseModel):
    name: str
    address1: str
    address2: str | None = None
    address3: str | None = None
    contactName: str
    zipcode: str
    city: str
    province: str | None = None
    countryCode: str
    email: str | None = None
    phone: str

    # TODO: add validation


class Parcel(BaseModel):
    weight: float
    volume: float
    unit_weight: _PARCEL_WEIGHT_UNIT_CHOICES
    unit_volume: _PARCEL_VOLUME_UNIT_CHOICES
    description: str | None = None


class Shipment(BaseModel):
    from_address: Address
    to_address: Address
    parcel: Parcel
    reference: str
