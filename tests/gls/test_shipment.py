from shippy import GLSClient
from shippy.base.schemas import Parcel, Shipment


def test_create_shipment(austrian_address_1, austrian_address_2):
    gls_client = GLSClient()

    parcel = Parcel(weight=10, unit_weight="KGS", volume=1, unit_volume="L")
    shipment_reference = "shipment 0815"
    shipment = Shipment(
        from_address=austrian_address_1,
        to_address=austrian_address_2,
        parcel=parcel,
        reference=shipment_reference,
    )
    result = gls_client.ship(shipment)
    assert result.data.CreatedShipment.ShipmentReference[0] == shipment_reference
    assert result.tracking_id


def test_cancel_parcel(austrian_address_1, austrian_address_2):
    gls_client = GLSClient()

    parcel = Parcel(weight=10, unit_weight="KGS", volume=1, unit_volume="L")
    shipment_reference = "shipment 0815"
    shipment = Shipment(
        from_address=austrian_address_1,
        to_address=austrian_address_2,
        parcel=parcel,
        reference=shipment_reference,
    )
    result = gls_client.ship(shipment)

    response = gls_client.cancel_shipment(result.tracking_id)
    assert response.TrackID == result.tracking_id
