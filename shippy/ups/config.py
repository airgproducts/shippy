from pydantic import BaseSettings, Field, HttpUrl

from shippy.base.config import BaseConfig


class Config(BaseSettings, BaseConfig):
    user: str = Field(..., env="SHIPPY_UPS_USERNAME")
    password: str = Field(..., env="SHIPPY_UPS_PASSWORD")
    base_url: HttpUrl = Field(..., env="SHIPPY_UPS_BASE_URL")
    key: str = Field(..., env="SHIPPY_UPS_KEY")
    account_number: str = Field(..., env="SHIPPY_UPS_ACCOUNT_NUMBER")
