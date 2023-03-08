from pydantic import BaseSettings, Field, HttpUrl

from shippy.base.config import BaseConfig


class Config(BaseSettings, BaseConfig):
    user: str = Field(..., env="SHIPPY_GLS_USER")
    password: str = Field(..., env="SHIPPY_GLS_PASSWORD")
    base_url: HttpUrl = Field(..., env="SHIPPY_GLS_BASE_URL")
    contact_id: str = Field(..., env="SHIPPY_GLS_CONTACT_ID")
