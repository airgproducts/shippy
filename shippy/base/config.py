from pydantic import HttpUrl
from requests.auth import HTTPBasicAuth


class BaseConfig:
    user: str
    password: str
    base_url: HttpUrl

    @property
    def auth(self) -> HTTPBasicAuth:
        return HTTPBasicAuth(self.user, self.password)
