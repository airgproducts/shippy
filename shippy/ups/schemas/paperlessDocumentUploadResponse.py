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
    TransactionReference: TransactionReferenceSchema


class FormsHistoryDocumentIDSchema(BaseModel):
    DocumentID: List[str]


class UploadResponseSchema(BaseModel):
    Response: ResponseSchema
    FormsHistoryDocumentID: FormsHistoryDocumentIDSchema


class PaperlessDocumentUploadResponseSchema(BaseModel):
    UploadResponse: UploadResponseSchema

    @property
    def document_ids(self) -> list[str]:
        return self.UploadResponse.FormsHistoryDocumentID.DocumentID
