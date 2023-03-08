from shippy.base.utils import round_up_value


def get_tracking_link(tracking_id: str):
    return f"http://wwwapps.ups.com/WebTracking/track?track=yes&trackNums={tracking_id}"


def calculate_dim_weight_from_volume(volume: float) -> str:
    """Volume in liters"""
    # TODO: add support for other units
    # according to https://www.ups.com/re/en/help-center/packaging-and-supplies/determine-billable-weight.page
    volume_in_liters = volume
    volume_in_cm3 = volume_in_liters * 1000
    dimensional_weight = volume_in_cm3 / 5000
    rounded_weight = round_up_value(dimensional_weight)
    formatted_weight = str(int(rounded_weight * 10))
    # ^ UPS implies one decimal place (e.g. 115 = 11.5)
    return formatted_weight
