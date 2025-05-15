"""
2D geometry shapes abstractions
"""

from dataclasses import dataclass
from typing import Self


@dataclass
class Rectangle:
    """
    2D rectangle abstraction.

    Attributes
    ----------
    x0 : float
        Left bound.
    x1 : float
        Right bound.
    y0 : float
        Bottom bound.
    y1 : float
        Top bound.
    related: Rectangle
        Related rectangle. (needed for tag layout algorithms)
    label: str
        Text label. (needed for plot drawing)
    """

    x0: float
    x1: float
    y0: float
    y1: float
    related: Self = None
    label: str = None

    @property
    def center_x(self) -> float:
        """
        Get x coordinate of rectangle center.
        """
        return self.x0 + self.width / 2

    @property
    def center_y(self) -> float:
        """
        Get y coordinate of rectangle center.
        """
        return self.y0 + self.height / 2

    @property
    def width(self) -> float:
        """
        Get rectangle width.
        """
        return self.x1 - self.x0

    @property
    def height(self) -> float:
        """
        Get rectangle height.
        """
        return self.y1 - self.y0

    def move(self, dx: float, dy: float) -> None:
        """
        Move by `dx` in x-axis direction and `dy` in y-axis direction.
        """
        self.x0 += dx
        self.x1 += dx
        self.y0 += dy
        self.y1 += dy

    def overlaps(self, rectangle: Self) -> bool:
        """
        Check whether `self` and `rectangle` overlap.
        """
        return not (
            self.x0 > rectangle.x1
            or self.x1 < rectangle.x0
            or self.y0 > rectangle.y1
            or self.y1 < rectangle.y0
        )

    def get_distance(self, rectangle: Self) -> float:
        """
        Get manhattan distance between `self` and `rectangle` centers.
        """
        dx = abs(self.center_x - rectangle.center_x)
        dy = abs(self.center_y - rectangle.center_y)
        return dx + dy
