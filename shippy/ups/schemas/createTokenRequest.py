from pydantic import BaseModel


class CreateTokenRequest(BaseModel):
    grant_type: str
