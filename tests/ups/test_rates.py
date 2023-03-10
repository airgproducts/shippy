from shippy import UPSClient
from shippy.base.schemas import Parcel, Shipment


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

    result = ups_client.rate(shipment)
    assert result
