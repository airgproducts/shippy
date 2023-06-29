from shippy.base.utils import round_up_value
from shippy.ups.config import Config


def calculate_dim_weight_from_volume(volume: float, config: Config) -> str:
    """Volume in liters"""
    # TODO: add support for other units
    # according to https://www.ups.com/re/en/help-center/packaging-and-supplies/determine-billable-weight.page
    volume_in_liters = volume
    dimensional_weight = volume_in_liters * config.volume_weight_factor
    rounded_weight = round_up_value(dimensional_weight)
    formatted_weight = str(int(rounded_weight * 10))
    # ^ UPS implies one decimal place (e.g. 115 = 11.5)
    return formatted_weight
