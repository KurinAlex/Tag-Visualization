from dataclasses import dataclass
from typing import Self


@dataclass
class Rectangle:
    x0: float
    x1: float
    y0: float
    y1: float
    related: Self = None

    @property
    def center_x(self):
        return self.x0 + self.width / 2

    @property
    def center_y(self):
        return self.y0 + self.height / 2

    @property
    def width(self):
        return self.x1 - self.x0

    @property
    def height(self):
        return self.y1 - self.y0

    def move(self, dx: float, dy: float):
        self.x0 += dx
        self.x1 += dx
        self.y0 += dy
        self.y1 += dy

    def overlaps(self, rectangle: Self):
        return not (
            self.x0 > rectangle.x1
            or self.x1 < rectangle.x0
            or self.y0 > rectangle.y1
            or self.y1 < rectangle.y0
        )

    def get_distance(self, rectangle: Self):
        dx = abs(self.center_x - rectangle.center_x)
        dy = abs(self.center_y - rectangle.center_y)
        return dx + dy
