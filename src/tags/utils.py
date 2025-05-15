import random
from typing import Sequence

from .geometry import Rectangle


def random_float(a: float, b: float):
    """
    Get random float number in range [a, b).
    """
    return random.random() * (b - a) + a


def get_bounding_rectangle(rectangles: Sequence[Rectangle]) -> Rectangle:
    """
    Get minimal rectangle, which completely contains specified rectangles.
    """
    x0 = min(map(lambda x: x.x0, rectangles))
    x1 = max(map(lambda x: x.x1, rectangles))
    y0 = min(map(lambda x: x.y0, rectangles))
    y1 = max(map(lambda x: x.y1, rectangles))
    return Rectangle(x0, x1, y0, y1)
