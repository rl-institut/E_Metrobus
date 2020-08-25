import math
import datetime as dt
from collections import namedtuple
from dataclasses import dataclass, fields

from django.utils.translation import gettext_lazy as _

ELLIPSE_RADIUS = 43
ELLIPSE_X_OFFSET = 7
ELLIPSE_Y_OFFSET = 7

Consumption = namedtuple("Consumption", ["distance", "co2", "nitrogen", "fine_dust"])

FLEET_START_DATE = dt.date(2020, 8, 27)
FLEET_DISTANCE_PER_DAY = 2800


def get_fleet_distance():
    days = (dt.date.today() - FLEET_START_DATE).days + 1
    distance = FLEET_DISTANCE_PER_DAY * days
    return max(distance, FLEET_DISTANCE_PER_DAY)


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
        if self.share == 1:
            return f"M {ELLIPSE_RADIUS + ELLIPSE_X_OFFSET} {ELLIPSE_Y_OFFSET} A {ELLIPSE_RADIUS} {ELLIPSE_RADIUS} 0 {self.large} 1 {ELLIPSE_X_OFFSET + ELLIPSE_RADIUS } {ELLIPSE_Y_OFFSET + 2 * ELLIPSE_RADIUS} A {ELLIPSE_RADIUS} {ELLIPSE_RADIUS} 0 {self.large} 1 {ELLIPSE_X_OFFSET + ELLIPSE_RADIUS } {ELLIPSE_Y_OFFSET}"  # noqa
        return f"M {ELLIPSE_RADIUS + ELLIPSE_X_OFFSET} {ELLIPSE_Y_OFFSET} A {ELLIPSE_RADIUS} {ELLIPSE_RADIUS} 0 {self.large} 1 {self.x} {self.y}"  # noqa


@dataclass
class DataPerKilometer:
    co2: float
    nitrogen: float
    fine_dust: float

    def __mul__(self, value):
        return DataPerKilometer(
            *(getattr(self, dim.name) * value for dim in fields(self))
        )

    def __truediv__(self, value):
        return DataPerKilometer(
            *(getattr(self, dim.name) / value for dim in fields(self))
        )


@dataclass
class Vehicle:
    name: str
    label: str
    data: DataPerKilometer


VEHICLES = [
    Vehicle(
        name="car",
        label=_("PKW (Diesel)"),
        data=DataPerKilometer(co2=147, nitrogen=0.43, fine_dust=0.007),
    ),
    Vehicle(
        name="bus",
        label=_("Dieselbus"),
        data=DataPerKilometer(co2=80, nitrogen=0.32, fine_dust=0.005),
    ),
    Vehicle(name="e-pkw", label=_("Elektro-PKW"), data=DataPerKilometer(53, 0, 0),),
    Vehicle(name="e-bus", label=_("Elektrobus"), data=DataPerKilometer(42, 0, 0),),
    Vehicle(name="bicycle", label=_("Fahrrad"), data=DataPerKilometer(0, 0, 0),),
    Vehicle(name="pedestrian", label=_("zu Fuß"), data=DataPerKilometer(0, 0, 0),),
]

DATA_SOURCES = [
    'Umweltbundesamt, "Vergleich der durchschnittlichen Emissionen einzelner '
    'Verkehrsmittel im Personenverkehr in Deutschland - '
    'Bezugsjahr 2018", 01/2020, TREMOD 6.03',
    'Umweltbundesamt, '
    '"Entwicklung der spezifischen Kohlendioxid-Emissionen des deutschen Strommix in '
    'den Jahren 1990 - 2019", 13/2020',
    _("Annahmen zum Energieverbrauch der E-PKWs und E-Busse: Reiner Lemoine Institut"),
    _("Annahmen zur Personenzahl eines Linienbusses: BVG"),
]

POSTHOG_EVENTS = ("shared", "sources", "english")

FINISHED_SLOGANS = (
    _(
        "Oha, da ist noch Luft nach oben! Macht aber nichts. "
        "In unserem Info-Bereich findest du Antworten auf "
        "all deine Fragen zu E-Bussen, die du nie zu stellen gewagt hast."
    ),
    _(
        "Nicht schlecht, aber das geht noch besser! "
        "Alle Fakten zum Nachlesen und Aufschlauen findest du in unserem Info-Bereich."
    ),
    _(
        "Wow! Wir können dir kaum noch etwas beibringen. "
        "Alle Fakten zum Nachlesen findest du nochmal in unserem Info-Bereich."
    ),
)
