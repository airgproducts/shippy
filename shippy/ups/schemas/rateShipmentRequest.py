from pydantic import BaseModel, Field

from shippy.base.schemas import Address as BaseAddress
from shippy.base.schemas import Parcel as BaseParcel
from shippy.ups.utils import calculate_dim_weight_from_volume
from shippy.ups.config import Config

from .base import (
    Address,
    DimWeight,
    DimWeightUnitOfMeasurement,
    PackageWeight,
    PackageWeightUnitOfMeasurement,
    ShipmentCharge,
)


class Person(BaseModel):
    Name: str = Field(..., max_length=35)
    Address: Address

    @classmethod
    def from_generic_address(cls, address: BaseAddress):
        return cls(
            Name=address.name, Address=Address.from_generic_address(address=address)
        )


class PaymentDetails(BaseModel):
    ShipmentCharge: ShipmentCharge


class PackagingType(BaseModel):
    Code: str


class Package(BaseModel):
    PackagingType: PackagingType
    DimWeight: DimWeight
    PackageWeight: PackageWeight

    @classmethod
    def from_generic_parcel(cls, parcel: BaseParcel, config: Config):
        return cls(
            PackagingType=PackagingType(Code="02"),
            PackageWeight=PackageWeight(
                UnitOfMeasurement=PackageWeightUnitOfMeasurement(Code=parcel.unit_weight),
                Weight=str(parcel.weight),
            ),
            DimWeight=DimWeight(
                UnitOfMeasurement=DimWeightUnitOfMeasurement(Code=parcel.unit_weight),
                Weight=calculate_dim_weight_from_volume(parcel.volume, config),
            ),
        )


class Shipment(BaseModel):
    Shipper: Person
    ShipTo: Person
    Package: Package


class RateRequest(BaseModel):
    Shipment: Shipment


class RateShipmentRequest(BaseModel):
    RateRequest: RateRequest

    @classmethod
    def from_generic_schemas(
        cls,
        parcel: BaseParcel,
        to_address: BaseAddress,
        from_address: BaseAddress,
        config: Config,
    ):
        return cls(
            RateRequest=RateRequest(
                Shipment=Shipment(
                    Shipper=Person.from_generic_address(from_address),
                    ShipTo=Person.from_generic_address(to_address),
                    Package=Package.from_generic_parcel(parcel=parcel, config=config),
                )
            )
        )
