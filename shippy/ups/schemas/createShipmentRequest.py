from enum import Enum
from typing import Literal

from pydantic import BaseModel, Field

from shippy.base.schemas import Address as BaseAddress
from shippy.base.schemas import Parcel as BaseParcel
from shippy.ups.utils import calculate_dim_weight_from_volume

_PAYMENT_INFORMATION_TYPE_CHOICES = Literal["01", "02", "03"]


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


_PACKAGING_CODE_CHOICES = Literal[
    "01",
    "02",
    "03",
    "21",
    "24",
    "25",
    "30",
    "2a",
    "2b",
    "56",
    "57",
    "58",
    "59",
    "60",
    "61",
    "62",
    "63",
    "64",
    "65",
    "66",
    "67",
]
_PACKAGE_WEIGHT_UNIT_OF_MEASUREMENT_CHOICES = Literal["LBS", "KGS", "OZS"]
_DIM_WEIGHT_UNIT_OF_MEASUREMENT_CHOICES = Literal["LBS", "KGS"]


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
            StateProvinceCode=address.province,
        )


class Phone(BaseModel):
    Number: str = Field(..., max_length=15)
    Extension: str | None = Field(None, max_length=4)


class Shipper(BaseModel):
    Name: str = Field(..., max_length=35)
    AttentionName: str = Field(..., max_length=35)
    Phone: Phone
    ShipperNumber: str = Field(..., max_length=6)
    EmailAddress: str | None = Field(None, max_length=50)
    Address: Address

    @classmethod
    def from_generic_address(cls, address: BaseAddress, shipper_number: str):
        return cls(
            Name=address.name,
            AttentionName=address.contactName,
            Phone=Phone(Number=address.phone.replace(" ", "")),
            ShipperNumber=shipper_number,
            EmailAddress=address.email,
            Address=Address.from_generic_address(address=address),
        )


class ShipTo(BaseModel):
    Name: str = Field(..., max_length=35)
    AttentionName: str = Field(..., max_length=35)
    Phone: Phone
    EmailAddress: str | None = Field(None, max_length=50)
    Address: Address

    @classmethod
    def from_generic_address(cls, address: BaseAddress):
        return cls(
            Name=address.name,
            AttentionName=address.contactName,
            Phone=Phone(Number=address.phone),
            EmailAddress=address.email,
            Address=Address.from_generic_address(address=address),
        )


class BillShipper(BaseModel):
    AccountNumber: str = Field(..., max_length=6)


class ShipmentCharge(BaseModel):
    Type: _PAYMENT_INFORMATION_TYPE_CHOICES
    BillShipper: BillShipper


class PaymentInformation(BaseModel):
    ShipmentCharge: ShipmentCharge


class ReferenceNumber(BaseModel):
    Value: str = Field(..., max_length=35)


class Service(BaseModel):
    Code: ServiceCodeEnum
    Description: str | None = Field(None, max_length=35)


class Packaging(BaseModel):
    Code: _PACKAGING_CODE_CHOICES
    Description: str | None = Field(None, max_length=35)


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

    @classmethod
    def from_weight_and_volume(cls, weight: PackageWeight, volume: float):
        # todo: from parcel model
        return cls(UnitOfMeasurement=weight.UnitOfMeasurement, Weight=1)


class Package(BaseModel):
    Description: str | None = Field(None, max_length=35)
    Packaging: Packaging
    DimWeight: DimWeight
    PackageWeight: PackageWeight

    @classmethod
    def from_generic_parcel(cls, parcel: BaseParcel):
        return cls(
            Description=parcel.description,
            Packaging=Packaging(Code="02"),
            PackageWeight=PackageWeight(
                UnitOfMeasurement=PackageWeightUnitOfMeasurement(Code=parcel.unit_weight),
                Weight=str(parcel.weight),
            ),
            DimWeight=DimWeight(
                UnitOfMeasurement=DimWeightUnitOfMeasurement(Code=parcel.unit_weight),
                Weight=calculate_dim_weight_from_volume(parcel.volume),
            ),
        )


class Shipment(BaseModel):
    Description: str = Field(..., max_length=50)
    Shipper: Shipper
    ShipTo: ShipTo
    PaymentInformation: PaymentInformation
    ReferenceNumber: ReferenceNumber
    Service: Service
    Package: Package


class ShipmentRequest(BaseModel):
    Shipment: Shipment


class CreateShipmentRequest(BaseModel):
    ShipmentRequest: ShipmentRequest

    @classmethod
    def from_generic_schemas(
        cls,
        account_number: str,
        shipment_reference: str,
        parcel: BaseParcel,
        to_address: BaseAddress,
        from_address: BaseAddress,
        service_code: ServiceCodeEnum,
    ):
        return cls(
            ShipmentRequest=ShipmentRequest(
                Shipment=Shipment(
                    Description="description",
                    Shipper=Shipper.from_generic_address(
                        address=from_address, shipper_number=account_number
                    ),
                    ShipTo=ShipTo.from_generic_address(address=to_address),
                    PaymentInformation=PaymentInformation(
                        ShipmentCharge=ShipmentCharge(
                            Type="01",
                            BillShipper=BillShipper(
                                AccountNumber=account_number,
                            ),
                        ),
                    ),
                    ReferenceNumber=ReferenceNumber(Value=shipment_reference),
                    Service=Service(Code=service_code, Description="UPS Standard"),
                    Package=Package.from_generic_parcel(parcel),
                )
            )
        )
