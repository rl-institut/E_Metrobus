
import os
from dataclasses import dataclass, fields
from typing import Dict

import pandas
from django.conf import settings

STATIONS_FILE = os.path.join(settings.APPS_DIR, "navigation", "stations.csv")


@dataclass
class DataPerKilometer:
    fuel: float
    co2: float
    nitrogen: float
    fine_dust: float

    def __mul__(self, value):
        return DataPerKilometer(
            *(getattr(self, dim.name) * value for dim in fields(self))
        )


@dataclass
class Vehicle:
    name: str
    passengers: int
    data: DataPerKilometer


VEHICLES = [
    Vehicle(name="car", passengers=30, data=DataPerKilometer(14 / 100, 322, 34, 54)),
    Vehicle(name="bus", passengers=30, data=DataPerKilometer(10 / 100, 200, 22, 40)),
    Vehicle(name="e-bus", passengers=30, data=DataPerKilometer(5 / 100, 120, 10, 30)),
    Vehicle(name="bicycle", passengers=30, data=DataPerKilometer(0, 0, 0, 0)),
    Vehicle(name="pedestrian", passengers=30, data=DataPerKilometer(0, 0, 0, 0)),
]


class Stations:
    def __init__(self, filename):
        self.stations = pandas.read_csv(filename, index_col=0)
        self.__init_stations()

    def __init_stations(self):
        # Mirror diagonal:
        for i, station in enumerate(self.stations):
            self.stations[station] = self.stations.iloc[i]

    def get_stations(self):
        return (station for station in self.stations)

    def get_distance(self, from_station: str, to_station: str) -> float:
        return self.stations[from_station][to_station]

    def get_route_data(
        self, from_station: str, to_station: str
    ) -> Dict[str, DataPerKilometer]:
        passenger_kilometer = self.get_distance(from_station, to_station)
        return {
            vehicle.name: vehicle.data * vehicle.passengers * passenger_kilometer
            for vehicle in VEHICLES
        }

    def __getitem__(self, item):
        return self.stations.index[item]


STATIONS = Stations(STATIONS_FILE)


if __name__ == "__main__":
    print(STATIONS.get_route_data("Station C", "Station A"))
