import math


def round_up(value: int):
    """Round up value to nearest hundred."""
    return int(math.ceil(value / 100.0)) * 100
