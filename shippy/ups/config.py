from pydantic import Field, HttpUrl

from shippy.base.config import BaseConfig


class Config(BaseConfig):
    user: str = Field(..., validation_alias="SHIPPY_UPS_CLIENT_ID")
    password: str = Field(..., validation_alias="SHIPPY_UPS_CLIENT_SECRET")
    base_url: HttpUrl = Field(..., validation_alias="SHIPPY_UPS_BASE_URL")
    account_number: str = Field(..., validation_alias="SHIPPY_UPS_ACCOUNT_NUMBER")
    volume_weight_factor: float = Field(
        0.2, validation_alias="SHIPPY_UPS_VOLUME_WEIGHT_FACTOR"
    )
