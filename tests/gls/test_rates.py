from datetime import datetime

from shippy import GLSClient
from shippy.base.schemas import Parcel, Shipment


def test_rate_shipment(austrian_address_1, austrian_address_2):
    gls_client = GLSClient()

    parcel = Parcel(weight=10, unit_weight="KGS", volume=1, unit_volume="L")
    shipment_reference = "shipment 0815"
    shipment = Shipment(
        from_address=austrian_address_1,
        to_address=austrian_address_2,
        parcel=parcel,
        reference=shipment_reference,
    )
    result = gls_client.rate(shipment)
    assert isinstance(result.delivery_date, datetime)
    assert result.delivery_date > datetime.now()
