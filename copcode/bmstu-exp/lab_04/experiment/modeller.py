from .generator import Generator
from .processor import Processor


class Modeller:
    def __init__(self, generators, operators):
        self._generators = generators
        self._operators = operators

    def event_mode(self, num_requests):
        processed = 0
        wait_times_sum = 0

        for g in self._generators: 
            g.next = g.next_time()

        actors = self._generators + self._operators 
        free = True
        free_time = 0
        prev_time = 0

        while processed < num_requests:
            current_time = min(map(lambda x: x.next, filter(lambda x: x.next != 0, actors)))
            if free:
                free_time += current_time - prev_time

            for actor in actors:
                if current_time == actor.next:
                    if isinstance(actor, Processor):
                        wait_time = actor.process_request(current_time)
                        wait_times_sum += wait_time
                        processed += 1
                        if len(actor.queue) == 0:
                            actor.next = 0
                            free = True
                        else:
                            # actor.next = current_time + actor.next_time()
                            actor.next = current_time + actor.next_time(actor.queue[0][1])
                    else:
                        receiver = actor.generate_request(current_time)
                        if receiver is not None:
                            if receiver.next == 0:
                                # receiver.next = current_time + receiver.next_time()
                                receiver.next = current_time + receiver.next_time(actor.reqtype)
                            actor.next = current_time + actor.next_time()
                            free = False

            prev_time = current_time

        return {
            "time": current_time,
            "avg_wait_time": wait_times_sum / processed,
            "free_time": free_time
        }