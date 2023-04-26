from shippy import UPSClient
from shippy.base.schemas import Parcel, Shipment
from shippy.ups.schemas import ServiceEnum, CreateShipmentResponse
from shippy.ups.schemas.createShipmentRequest import ShipmentServiceOptions

def create_shipment(austrian_address_1, german_address_1) -> Shipment:
    parcel = Parcel(weight=10, unit_weight="KGS", volume=1, unit_volume="L")
    shipment_reference = "shipment 0815"
    return Shipment(
        from_address=austrian_address_1,
        to_address=german_address_1,
        parcel=parcel,
        reference=shipment_reference,
    )

def check_shipment_response(result: CreateShipmentResponse):
    assert result
    assert result.tracking_id.startswith("1Z")
    assert result.label_as_bytes.startswith(b"GIF")

def test_create_shipment(austrian_address_1, german_address_1):
    ups_client = UPSClient()
    shipment = create_shipment(austrian_address_1, german_address_1)

    result = ups_client.ship(shipment, ServiceEnum.UPS_STANDARD)
    check_shipment_response(result)

def test_create_shipment_with_signature(austrian_address_1, german_address_1):
    ups_client = UPSClient()
    shipment = create_shipment(austrian_address_1, german_address_1)
    request = ups_client.create_shipment_request(shipment, ServiceEnum.UPS_STANDARD)

    assert request.ShipmentRequest.Shipment.ShipmentServiceOptions.DeliveryConfirmation is None
    request.ShipmentRequest.Shipment.ShipmentServiceOptions.require_signature()
    assert request.ShipmentRequest.Shipment.ShipmentServiceOptions.DeliveryConfirmation is not None

    result = ups_client.ship(request, ServiceEnum.UPS_STANDARD)
    check_shipment_response(result)


def test_cancel_shipment(austrian_address_1, german_address_1):
    shipment_id = "1Z2220060290602143"  # provided by UPS for test system
    ups_client = UPSClient()
    result = ups_client.cancel_shipment(shipment_id)
    assert result.cancellation_successful
