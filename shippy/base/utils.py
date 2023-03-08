import math


def round_up_value(val: float, decimals: int = 1):
    return math.ceil(val * 10 * decimals) / 10 * decimals
