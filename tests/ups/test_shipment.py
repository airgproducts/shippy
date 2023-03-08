from shippy import UPSClient
from shippy.base.schemas import Parcel, Shipment
from shippy.ups.schemas import ServiceCodeEnum


def test_create_shipment(austrian_address_1, german_address_1):
    gls_client = UPSClient()

    parcel = Parcel(weight=10, unit_weight="KGS", volume=1, unit_volume="L")
    shipment_reference = "shipment 0815"
    shipment = Shipment(
        from_address=austrian_address_1,
        to_address=german_address_1,
        parcel=parcel,
        reference=shipment_reference,
    )

    result = gls_client.ship(shipment, ServiceCodeEnum.UPS_STANDARD)
    assert result
    assert result.tracking_id.startswith("1Z")
    assert result.label_as_bytes.startswith(b"GIF")
