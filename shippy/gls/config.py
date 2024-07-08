from pydantic import Field, HttpUrl
from pydantic_settings import BaseSettings

from shippy.base.config import BaseConfig


class Config(BaseSettings, BaseConfig):
    user: str = Field(..., validation_alias="SHIPPY_GLS_USER")
    password: str = Field(..., validation_alias="SHIPPY_GLS_PASSWORD")
    base_url: HttpUrl = Field(..., validation_alias="SHIPPY_GLS_BASE_URL")
    contact_id: str = Field(..., validation_alias="SHIPPY_GLS_CONTACT_ID")
