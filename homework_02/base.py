from abc import ABC
from .exceptions import LowFuelError, NotEnoughFuel


class Vehicle(ABC):
    weight = None
    started = False
    fuel = 0
    fuel_consumption = 0

    def __init__(self, weight, fuel, fuel_consumption):
        """
        Set weight, fuel and fuel_consumption here
        """
        self.weight = weight
        self.fuel = fuel
        self.fuel_consumption = fuel_consumption

    def start(self):
        if self.started:
            return
        if self.fuel <= 0:
            raise LowFuelError
        self.started = True

    def move(self, distance: int):
        to_spend = (distance * self.fuel_consumption)
        if to_spend > self.fuel:
            raise NotEnoughFuel
        self.fuel -= to_spend
