
import numpy.random as nr
from abc import ABC, abstractmethod


class BaseDistr(ABC):
    @abstractmethod
    def random_value(self) -> float:
        pass


class ExponentialDistr(BaseDistr):
    def __init__(self, intensity: float):
        self._i = 1 / intensity

    def random_value(self) -> float:
        return nr.exponential(self._i)


class NormalDistr(BaseDistr):
    def __init__(self, intensity: float, range: float):
        self._i = 1 / intensity
        self._range = range

    def random_value(self) -> float:
        return nr.normal(self._i, self._range)
