from typing import Literal

from pydantic import BaseModel, Field

from shippy.base.schemas import Address as BaseAddress
from shippy.base.schemas import Parcel as BaseParcel

_PRODUCT_CHOICES = Literal["EXPRESS", "PARCEL", "FREIGHT", "PHARMA", "PHARMAPLUS"]
_TEMPLATE_SET_CHOICES = Literal["NONE", "ZPL_200", "ZPL_300"]
_LABEL_FORMAT_CHOICES = Literal["PDF", "PNG", "ZEBRA"]
_INCOTERM_CODE_CHOICES = Literal["10", "20", "30", "40", "50"]


class Address(BaseModel):
    Name1: str = Field(..., max_length=40)
    Name2: str | None = Field(None, max_length=40)
    Name3: str | None = Field(None, max_length=40)
    CountryCode: str = Field(..., min_length=2, max_length=2)
    Province: str | None = Field(None, max_length=40)
    ZIPCode: str = Field(..., max_length=10)
    City: str = Field(..., max_length=40)
    Street: str = Field(..., max_length=40, min_length=4)
    eMail: str | None = Field(None, max_length=80)
    MobilePhoneNumber: str | None = Field(None, min_length=4, max_length=35)
    ContactPerson: str | None = Field(None, min_length=6, max_length=40)

    @classmethod
    def from_generic_address(cls, address: BaseAddress):
        return cls(
            Name1=address.name,
            CountryCode=address.countryCode,
            Province=address.province,
            ZIPCode=address.zipcode,
            City=address.city,
            Street=address.address1,
            Name2=address.address2,
            Name3=address.address3,
            eMail=address.email,
            MobilePhoneNumber=address.phone,
            ContactPerson=address.contactName,
        )


class Shipper(BaseModel):
    ContactID: str = Field(..., max_length=20)
    AlternativeShipperAddress: Address


class Consignee(BaseModel):
    Address: Address


class ShipmentUnit(BaseModel):
    ShipmentUnitReference: list[str] | None
    Weight: float = Field(..., gt=0)
    # TODO: add validation for ShipmentUnitReference


class Shipment(BaseModel):
    ShipmentReference: list[str] | None
    IncotermCode: _INCOTERM_CODE_CHOICES = "10"
    Product: _PRODUCT_CHOICES
    Shipper: Shipper
    Consignee: Consignee
    ShipmentUnit: list[ShipmentUnit]
    # TODO: add validation for ShipmentReference


class CustomContent(BaseModel):
    CustomerLogo: str


class ReturnLabels(BaseModel):
    TemplateSet: _TEMPLATE_SET_CHOICES = "NONE"
    LabelFormat: _LABEL_FORMAT_CHOICES = "PNG"


class PrintingOptionsSchema(BaseModel):
    ReturnLabels: ReturnLabels = ReturnLabels()


class CreateShipmentRequest(BaseModel):
    Shipment: Shipment
    PrintingOptions: PrintingOptionsSchema = PrintingOptionsSchema()
    CustomContent: CustomContent | None

    @classmethod
    def from_generic_schemas(
        cls,
        shipment_reference: str,
        contact_id: str,
        parcel: BaseParcel,
        to_address: BaseAddress,
        from_address: BaseAddress,
    ):
        return cls(
            Shipment=Shipment(
                ShipmentReference=[shipment_reference],
                Product="PARCEL",
                Shipper=Shipper(
                    ContactID=contact_id,
                    AlternativeShipperAddress=Address.from_generic_address(
                        address=from_address
                    ),
                ),
                Consignee=Consignee(
                    Address=Address.from_generic_address(address=to_address)
                ),
                ShipmentUnit=[
                    ShipmentUnit(
                        Weight=parcel.weight, ShipmentUnitReference=[shipment_reference]
                    )
                ],
            )
        )
