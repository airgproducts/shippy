from datetime import datetime
from importlib.metadata import files

from shippy import UPSClient
from shippy.ups.schemas import (
    ImageFileSchema,
    PaperlessDocumentUploadResponseSchema,
    ServiceEnum,
    UploadFileSchema,
)

from .test_shipment import create_shipment

file_example = UploadFileSchema(
    name="Sample Document",
    format="pdf",
    document_type="002",
    file_as_base_64="SGVsbG8sIFdvcmxkIQ==",  # "Hello, World!" in base64
)


def test_upload_file():
    ups_client = UPSClient()
    files = [file_example]
    upload_response = ups_client.paperless_document_upload(files)
    assert isinstance(upload_response, PaperlessDocumentUploadResponseSchema)
    assert isinstance(upload_response.document_ids, list)
    assert len(upload_response.document_ids) > 0
    assert isinstance(upload_response.document_ids[0], str)


def test_image_file(austrian_address_1, german_address_1):
    ups_client = UPSClient()

    # create shipment first
    shipment_response = ups_client.ship(
        create_shipment(austrian_address_1, german_address_1), ServiceEnum.UPS_STANDARD
    )

    # then create document
    upload_response = ups_client.paperless_document_upload(files=[file_example])

    data = ImageFileSchema(
        document_id=upload_response.document_ids[0],
        shipment_datetime=datetime.now(),
        shipment_identifier=shipment_response.shipping_id,
        tracking_number=shipment_response.tracking_id,
    )
    image_response = ups_client.paperless_document_image(data)
    assert image_response.success
