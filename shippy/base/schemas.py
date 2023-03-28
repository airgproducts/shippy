from typing import Literal

from pydantic import BaseModel, validator

_PARCEL_WEIGHT_UNIT_CHOICES = Literal["LBS", "KGS", "OZS"]
_PARCEL_VOLUME_UNIT_CHOICES = Literal["L"]


class Address(BaseModel):
    name: str
    address1: str
    address2: str | None = None
    address3: str | None = None
    contactName: str | None = None
    zipcode: str
    city: str
    provinceCode: str | None = None
    countryCode: str
    email: str | None = None
    phone: str

    @validator("*")
    def empty_str_to_none(cls, v):
        if v == "":
            return None
        return v

    # TODO: add extra validation


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
