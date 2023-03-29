from enum import Enum
from typing import Literal

from pydantic import BaseModel, Field, validator

from shippy.base.schemas import Address as BaseAddress

_PACKAGE_WEIGHT_UNIT_OF_MEASUREMENT_CHOICES = Literal["LBS", "KGS", "OZS"]
_DIM_WEIGHT_UNIT_OF_MEASUREMENT_CHOICES = Literal["LBS", "KGS"]
_PAYMENT_INFORMATION_TYPE_CHOICES = Literal["01", "02", "03"]


class Address(BaseModel):
    AddressLine: list[str]
    City: str = Field(..., max_length=30)
    PostalCode: str = Field(..., max_length=9)
    CountryCode: str = Field(..., min_length=2, max_length=2)
    StateProvinceCode: str | None = Field(None, min_length=2, max_length=5)

    @classmethod
    def from_generic_address(cls, address: BaseAddress):
        address_line = [
            entry
            for entry in [address.address1, address.address2, address.address3]
            if entry
        ]
        return cls(
            AddressLine=address_line,
            City=address.city,
            PostalCode=address.zipcode,
            CountryCode=address.countryCode,
            StateProvinceCode=address.provinceCode,
        )

    @validator("AddressLine")
    def validate_address_line_entry(cls, address_line):
        for entry in address_line:
            if len(entry) > 35:
                raise ValueError(
                    f'AddressLine entry "{entry}" is longer than 35 characters'
                )
        return address_line


class BillShipper(BaseModel):
    AccountNumber: str = Field(..., max_length=6)


class ShipmentCharge(BaseModel):
    Type: _PAYMENT_INFORMATION_TYPE_CHOICES
    BillShipper: BillShipper


class PackageWeightUnitOfMeasurement(BaseModel):
    Code: _PACKAGE_WEIGHT_UNIT_OF_MEASUREMENT_CHOICES
    Description: str | None = Field(None, max_length=35)


class DimWeightUnitOfMeasurement(BaseModel):
    Code: _DIM_WEIGHT_UNIT_OF_MEASUREMENT_CHOICES
    Description: str | None = Field(None, max_length=35)


class PackageWeight(BaseModel):
    UnitOfMeasurement: PackageWeightUnitOfMeasurement
    Weight: str = Field(..., max_length=5)
    # TODO: validate weight string


class DimWeight(BaseModel):
    UnitOfMeasurement: DimWeightUnitOfMeasurement
    Weight: str = Field(..., max_length=6)
    # TODO: validate weight string


class ServiceCodeEnum(str, Enum):
    UPS_NEXT_DAY_AIR = "01"
    UPS_SECOND_DAY_AIR = "02"
    UPS_GROUND = "03"
    UPS_EXPRESS = "07"
    UPS_EXPEDITED = "08"
    UPS_STANDARD = "11"
    UPS_THREE_DAY_SELECT = "12"
    UPS_NEXT_DAY_AIR_SAVER = "13"
    UPS_NEXT_DAY_AIR_EARLY = "14"
    UPS_WORLDWIDE_ECONOMY_DDU = "17"
    UPS_EXPRESS_PLUS = "54"
    UPS_SECOND_DAY_AIR_AM = "59"
    UPS_SAVER = "65"
    UPS_FIRST_CLASS_MAIL = "M2"
    UPS_PRIORITY_MAIL = "M3"
    UPS_EXPEDITED_MAIL_INNOVATIONS = "M4"
    UPS_PRIORITY_MAIL_INNOVATIONS = "M5"
    UPS_ECONOMY_MAIL_INNOVATIONS = "M6"
    UPS_MAIL_INNOVATIONS_MI_RETURNS = "M7"
    UPS_ACCESS_POINT_ECONOMY = "70"
    UPS_WORLDWIDE_EXPRESS_FREIGHT_MIDDAY = "71"
    UPS_WORLDWIDE_ECONOMY = "72"
    UPS_EXPRESS1200 = "74"
    UPS_TODAY_STANDARD = "82"
    UPS_TODAY_DEDICATED_COURIER = "83"
    UPS_TODAY_INTERCITY = "84"
    UPS_TODAY_EXPRESS = "85"
    UPS_TODAY_EXPRESS_SAVER = "86"
    UPS_WORLDWIDE_EXPRESS_FREIGHT = "96"
