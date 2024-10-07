from typing import List, Optional

from pydantic import BaseModel


class ResponseStatusSchema(BaseModel):
    Code: str
    Description: str


class AlertSchema(BaseModel):
    Code: str
    Description: str


class TransactionReferenceSchema(BaseModel):
    CustomerContext: str


class ResponseSchema(BaseModel):
    ResponseStatus: ResponseStatusSchema
    Alert: Optional[List[AlertSchema]] = None
    TransactionReference: Optional[TransactionReferenceSchema] = None

    @property
    def message(self) -> str:
        message = f"{self.ResponseStatus.Code}: {self.ResponseStatus.Description}"
        for alert in self.Alert:
            message += f"; Alert {alert.Code}: {alert.Description}"
        return message


class PushToImageRepositoryResponseSchema(BaseModel):
    Response: ResponseSchema
    FormsGroupID: str


class PaperlessDocumentImageResponseSchema(BaseModel):
    PushToImageRepositoryResponse: PushToImageRepositoryResponseSchema

    @property
    def success(self):
        return self.PushToImageRepositoryResponse.Response.ResponseStatus.Code == "1"

    @property
    def response_message(self) -> str:
        return self.PushToImageRepositoryResponse.Response.message
