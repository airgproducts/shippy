
from typing import Optional
from pydantic.dataclasses import dataclass
from pydantic import EmailStr
@dataclass
class Address:
    name: str
    name2: str

    address: str
    address2: str | None

    zipcode: str
    city: str
    state: Optional[str]
    country: str
    
    email: EmailStr

@dataclass
class Parcel:
    description: Optional[str]
    
    weight: float
    volume: float

@dataclass
class Shipment:
    description: str

    shipper: Address
    recipent: Address

    parcels: list[Parcel]

