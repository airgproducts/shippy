from pydantic import BaseModel, Field

from shippy.base.schemas import Address as BaseAddress


class Address(BaseModel):
    CountryCode: str = Field(..., min_length=2, max_length=2)
    ZIPCode: str = Field(..., max_length=10)
    City: str = Field(..., max_length=40)
    Street: str = Field(..., max_length=40, min_length=4)

    @classmethod
    def from_generic_address(cls, address: BaseAddress):
        return cls(
            CountryCode=address.countryCode,
            ZIPCode=address.zipcode,
            City=address.city,
            Street=address.address1,
        )


class AddressContainer(BaseModel):
    Address: Address


class RateShipmentRequest(BaseModel):
    Source: AddressContainer
    Destination: AddressContainer

    @classmethod
    def from_generic_schema(cls, from_address: BaseAddress, to_address: BaseAddress):
        return cls(
            Source=AddressContainer(Address=Address.from_generic_address(from_address)),
            Destination=AddressContainer(
                Address=Address.from_generic_address(to_address)
            ),
        )
