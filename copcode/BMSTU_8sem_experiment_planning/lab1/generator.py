from typing import List, Union
import distributions
from processor import Processor


class Generator:
    def __init__(self, time_distribution: distributions.AbstractDistribution):
        self._time_distribution = time_distribution
        self._receivers: List[Processor] = []
        self.time_periods: List[Union[int, float]] = []

    def set_receivers(self, receivers: List[Processor]):
        self._receivers = receivers

    def generate_time_period(self):
        time = self._time_distribution.generate_time()
        self.time_periods.append(time)
        return time

    def generate_request(self):
        for receiver in self._receivers:
            receiver.receive_request()
