from typing import Literal

from pydantic import BaseModel, Field

ALLOWED_FILE_FORMATS = Literal[
    "bmp", "doc", "gif", "jpg", "pdf", "png", "rtf", "tif", "txt", "xls", "docx", "xlsx"
]
ALLOWED_DOCUMENT_TYPES = Literal[
    "001",
    "002",
    "003",
    "004",
    "005",
    "006",
    "007",
    "008",
    "009",
    "010",
    "011",
    "012",
    "013",
]


class UploadFileSchema(BaseModel):
    # for user-friendly schema creation
    name: str = Field(..., max_length=300)
    format: ALLOWED_FILE_FORMATS
    document_type: ALLOWED_DOCUMENT_TYPES
    file_as_base_64: str


class TransactionReferenceSchema(BaseModel):
    CustomerContext: str


class RequestSchema(BaseModel):
    TransactionReference: TransactionReferenceSchema | None = None


class UserCreatedFormSchema(BaseModel):
    UserCreatedFormFileName: str = Field(..., max_length=300)
    UserCreatedFormFileFormat: ALLOWED_FILE_FORMATS
    UserCreatedFormDocumentType: ALLOWED_DOCUMENT_TYPES
    UserCreatedFormFile: str

    @classmethod
    def from_upload_file_schema(cls, schema: UploadFileSchema):
        return cls(
            UserCreatedFormFileName=schema.name,
            UserCreatedFormFileFormat=schema.format,
            UserCreatedFormDocumentType=schema.document_type,
            UserCreatedFormFile=schema.file_as_base_64,
        )


class UploadRequestSchema(BaseModel):
    Request: RequestSchema
    ShipperNumber: str = Field(..., min_length=6, max_length=6)
    UserCreatedForm: list[UserCreatedFormSchema]


class PaperlessDocumentUploadRequestSchema(BaseModel):
    UploadRequest: UploadRequestSchema

    @classmethod
    def create(cls, shipper_number: str, files: list[UploadFileSchema]):
        return cls(
            UploadRequest=UploadRequestSchema(
                Request=RequestSchema(),
                ShipperNumber=shipper_number,
                UserCreatedForm=[
                    UserCreatedFormSchema.from_upload_file_schema(schema)
                    for schema in files
                ],
            )
        )
