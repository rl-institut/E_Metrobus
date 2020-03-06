import math
from collections import namedtuple

ELLIPSE_RADIUS = 43
ELLIPSE_X_OFFSET = 7
ELLIPSE_Y_OFFSET = 7


class Ellipse:
    def __init__(self, share):
        """Calculates ellipse coordinates to draw from share"""
        self.share = share
        angle = share * 2 * math.pi
        self.large = 0 if share <= 0.5 else 1
        self.x = ELLIPSE_X_OFFSET + ELLIPSE_RADIUS + ELLIPSE_RADIUS * math.sin(angle)
        self.y = (
            ELLIPSE_Y_OFFSET
            + ELLIPSE_RADIUS
            + ELLIPSE_RADIUS * math.cos(angle + math.pi)
        )

    def __str__(self):
        return f"M {ELLIPSE_RADIUS + ELLIPSE_X_OFFSET} {ELLIPSE_Y_OFFSET} A {ELLIPSE_RADIUS} {ELLIPSE_RADIUS} 0 {self.large} 1 {self.x} {self.y}"


Consumption = namedtuple(
    "Consumption", ["distance", "fuel", "co2", "nitrogen", "fine_dust"]
)
