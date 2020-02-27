import pandas
from typing import Dict
from dataclasses import dataclass, fields

FILENAME = "stations.csv"


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
    Vehicle(name="car", passengers=30, data=DataPerKilometer(14/100, 322, 34, 54)),
    Vehicle(name="bus", passengers=30, data=DataPerKilometer(10/100, 322, 34, 54)),
    Vehicle(name="e-bus", passengers=30, data=DataPerKilometer(5/100, 322, 34, 54)),
    Vehicle(
        name="bicycle", passengers=30, data=DataPerKilometer(0, 0, 0, 0)
    ),
    Vehicle(
        name="pedestrian", passengers=30, data=DataPerKilometer(0, 0, 0, 0)
    ),
]


STATIONS = pandas.read_csv(FILENAME, index_col=0)

# Mirror diagonal:
for i, station in enumerate(STATIONS):
    STATIONS[station] = STATIONS.iloc[i]


def get_route_data(from_station: str, to_station: str) -> Dict[str, DataPerKilometer]:
    passenger_kilometer = STATIONS[from_station][to_station]
    return {
        vehicle.name: vehicle.data * vehicle.passengers * passenger_kilometer
        for vehicle in VEHICLES
    }


if __name__ == "__main__":
    print(get_route_data("Station C", "Station A"))
