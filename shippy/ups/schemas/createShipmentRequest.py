from typing import Literal

from pydantic import BaseModel, Field

from shippy.base.schemas import Address as BaseAddress
from shippy.base.schemas import Parcel as BaseParcel
from shippy.ups.utils import calculate_dim_weight_from_volume

from .base import (
    Address,
    BillShipper,
    DimWeight,
    DimWeightUnitOfMeasurement,
    PackageWeight,
    PackageWeightUnitOfMeasurement,
    ServiceEnum,
    ShipmentCharge,
)

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


class PaymentInformation(BaseModel):
    ShipmentCharge: ShipmentCharge


class ReferenceNumber(BaseModel):
    Value: str = Field(..., max_length=35)


class Service(BaseModel):
    Code: ServiceEnum
    Description: str | None = Field(None, max_length=35)


class Packaging(BaseModel):
    Code: _PACKAGING_CODE_CHOICES
    Description: str | None = Field(None, max_length=35)


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
        service_code: ServiceEnum,
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
