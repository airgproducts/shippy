from shippy import UPSClient
from shippy.base.schemas import Parcel, Shipment
from shippy.ups.schemas import ServiceEnum


def test_create_shipment(austrian_address_1, german_address_1):
    ups_client = UPSClient()

    parcel = Parcel(weight=10, unit_weight="KGS", volume=1, unit_volume="L")
    shipment_reference = "shipment 0815"
    shipment = Shipment(
        from_address=austrian_address_1,
        to_address=german_address_1,
        parcel=parcel,
        reference=shipment_reference,
    )

    result = ups_client.ship(shipment, ServiceEnum.UPS_STANDARD)
    assert result
    assert result.tracking_id.startswith("1Z")
    assert result.label_as_bytes.startswith(b"GIF")


def test_cancel_shipment(austrian_address_1, german_address_1):
    shipment_id = "1Z2220060290602143"  # provided by UPS for test system
    ups_client = UPSClient()
    result = ups_client.cancel_shipment(shipment_id)
    assert result.cancellation_successful
