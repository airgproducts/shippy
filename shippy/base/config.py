from pathlib import Path

from pydantic import HttpUrl
from pydantic_settings import BaseSettings, SettingsConfigDict
from requests.auth import HTTPBasicAuth

env_file_path = Path(__file__).parent.parent.parent.joinpath(".env")


class BaseConfig(BaseSettings):
    model_config = SettingsConfigDict(
        populate_by_name=True, env_file=env_file_path, extra="allow"
    )
    user: str
    password: str
    base_url: HttpUrl

    @property
    def auth(self) -> HTTPBasicAuth:
        return HTTPBasicAuth(self.user, self.password)
