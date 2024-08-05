from pydantic import BaseSettings, Field, HttpUrl

from shippy.base.config import BaseConfig


class Config(BaseSettings, BaseConfig):
    user: str = Field(..., env="SHIPPY_UPS_CLIENT_ID")
    password: str = Field(..., env="SHIPPY_UPS_CLIENT_SECRET")
    base_url: HttpUrl = Field(..., env="SHIPPY_UPS_BASE_URL")
    account_number: str = Field(..., env="SHIPPY_UPS_ACCOUNT_NUMBER")
    volume_weight_factor: float = Field(0.2, env="SHIPPY_UPS_VOLUME_WEIGHT_FACTOR")
