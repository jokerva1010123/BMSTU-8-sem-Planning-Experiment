from dataclasses import dataclass
import enum
from queue import PriorityQueue

from request import RequestBaseObject, RequestGenerator, RequestProcessor


@dataclass
class GeneratorResult:
    index: int
    total_requests: int
    total_generation_time: float
    avg_generation_time: float


@dataclass
class ProcessorResult:
    index: int
    total_requests: float
    total_processing_time: float
    total_waiting_time: float
    avg_processing_time: float
    avg_waiting_time: float


@dataclass
class ModelingResult:
    generators_results: list[GeneratorResult]
    processors_results: list[ProcessorResult]


class EventType(enum.Enum):
    simulation_finished = 0
    gen_finished = 1
    proc_finished = 2


@dataclass
class Event:
    time: float
    type: EventType
    block: RequestBaseObject


class Model:
    def __init__(self, generators: list[RequestGenerator], processors: list[RequestProcessor]):
        self.generators = generators
        self.processors = processors
        self._event_list = PriorityQueue()

    def add_event(self, new_event: Event) -> None:
        self._event_list.put((new_event.time, new_event))

    def simulate_event_based(self, max_time: float) -> ModelingResult:
        self._event_list = PriorityQueue()
        self.add_event(Event(max_time, EventType.simulation_finished, None))

        for generator in self.generators:
            next = generator.start_generation(0)
            self.add_event(Event(next, EventType.gen_finished, generator))

        while not self._event_list.empty():
            _, event = self._event_list.get()
            if event.type == EventType.simulation_finished:
                break

            if event.type == EventType.gen_finished:
                generator = event.block
                processor = generator.finish_generation()
                next = generator.start_generation(event.time)
                self.add_event(Event(next, EventType.gen_finished, generator))

                next = processor.start_processing(event.time)
                if (next):
                    self.add_event(
                        Event(next, EventType.proc_finished, processor))

            if event.type == EventType.proc_finished:
                processor = event.block
                processor.finish_processing()
                next = processor.start_processing(event.time)
                if (next):
                    self.add_event(
                        Event(next, EventType.proc_finished, processor))

        for processor in self.processors:
            processor.total_processing_time = min(
                processor.total_processing_time, max_time)

        for generator in self.generators:
            generator.total_generation_time = min(
                generator.total_generation_time, max_time)

        return ModelingResult(
            [GeneratorResult(index,
                             generator.total_requests,
                             generator.total_generation_time,
                             generator.total_generation_time/generator.total_requests)
             for index, generator in enumerate(self.generators, start=1)],
            [ProcessorResult(index,
                             processor.total_requests,
                             processor.total_processing_time,
                             processor.total_waiting_time,
                             processor.total_processing_time/processor.total_requests,
                             processor.total_waiting_time/processor.total_requests)
             for index, processor in enumerate(self.processors, start=1)])
