from shippy import UPSClient
from shippy.base.schemas import Parcel, Shipment
from shippy.ups.schemas import ServiceCodeEnum
from shippy.ups.schemas.rateShipmentResponse import ServicePrice


def test_rate_shipment(austrian_address_1, german_address_1):
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
    assert isinstance(result.service_prices[ServiceCodeEnum.UPS_STANDARD], ServicePrice)
    assert isinstance(result.service_prices[ServiceCodeEnum.UPS_SAVER], ServicePrice)
    assert isinstance(result.service_prices[ServiceCodeEnum.UPS_EXPRESS], ServicePrice)
