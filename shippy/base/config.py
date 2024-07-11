from pydantic import HttpUrl
from pydantic_settings import BaseSettings, SettingsConfigDict
from requests.auth import HTTPBasicAuth


class BaseConfig(BaseSettings):
    model_config = SettingsConfigDict(populate_by_name=True)
    user: str
    password: str
    base_url: HttpUrl

    @property
    def auth(self) -> HTTPBasicAuth:
        return HTTPBasicAuth(self.user, self.password)
