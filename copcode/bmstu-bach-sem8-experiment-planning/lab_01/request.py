from dataclasses import dataclass
from distributions import BaseDistr


@dataclass
class Request:
    time_in = None
    time_out = None


class RequestBaseObject:
    pass


class RequestProcessor(RequestBaseObject):
    def __init__(self, time_generator: BaseDistr):
        self._time_generator = time_generator
        self._queue = []
        self._waitingTime = 0
        self._busy = False

        self.total_requests = 0
        self.total_processing_time = 0
        self.total_waiting_time = 0

    @property
    def queue_size(self) -> int:
        return len(self._queue)

    def push_request(self, request: Request) -> None:
        self._queue.append(request)

    def start_processing(self, curr_time: float) -> float:
        if self._busy or len(self._queue) == 0:
            return None
        self._busy = True
        request = self._queue.pop(0)
        duration = self.generate_duration()
        next = curr_time + duration

        request.time_out = next
        self.total_waiting_time += curr_time - request.time_in

        self.total_processing_time += duration
        return next

    def finish_processing(self) -> None:
        if not self._busy:
            return None
        self._busy = False
        self.total_requests += 1

    def generate_duration(self) -> float:
        return self._time_generator.random_value()


class RequestGenerator(RequestBaseObject):
    def __init__(self, time_generator: BaseDistr, receivers: list[RequestProcessor] = []):
        self._time_generator = time_generator
        self._receivers = receivers
        self._request = None
        self._busy = False

        self.total_requests = 0
        self.total_generation_time = 0

    def start_generation(self, curr_time: float) -> float:
        if self._busy:
            return None
        self._busy = True
        duration = self.generate_duration()
        next = curr_time + duration
        self.total_generation_time += duration

        self._request = Request()
        self._request.time_in = next
        return next

    def finish_generation(self) -> RequestProcessor:
        if not self._busy:
            return None
        self._busy = False
        self.total_requests += 1

        min_queue_size = self._receivers[0].queue_size
        min_receiver_id = 0
        for index, receiver in enumerate(self._receivers):
            if receiver.queue_size < min_queue_size:
                min_queue_size = receiver.queue_size
                min_receiver_id = index

        self._receivers[min_receiver_id].push_request(self._request)
        return self._receivers[min_receiver_id]

    def generate_duration(self) -> float:
        return self._time_generator.random_value()
