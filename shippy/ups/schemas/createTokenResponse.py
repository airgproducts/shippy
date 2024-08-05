import datetime

from pydantic import BaseModel


class CreateTokenResponse(BaseModel):
    token_type: str
    client_id: str
    status: str
    access_token: str
    expires_in: str
    issued_at: str

    @property
    def issued_at_datetime(self):
        issued_at_timestamp = int(self.issued_at) / 1000
        return datetime.datetime.fromtimestamp(issued_at_timestamp, datetime.UTC)

    @property
    def expires_in_datetime(self):
        return self.issued_at_datetime + datetime.timedelta(seconds=int(self.expires_in))
