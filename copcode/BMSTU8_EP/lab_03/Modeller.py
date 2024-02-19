
from EventGenerator import Generator
from Processor import Processor


class Modeller:
    def __init__(self, generators, operators):
        self._generators = generators
        self._operators = operators

    def event_mode(self, num_requests):
        refusals = 0
        processed = 0
        created = 0
        wait_times =  []

        for g in self._generators: 
            g.next = g.next_time()

        self._operators[0].next = self._operators[0].next_time(0)

        blocks = self._generators + self._operators 

        while processed <= num_requests:
            # находим наименьшее время
            current_time = self._generators[0].next
            for block in blocks:
                if 0 < block.next < current_time:
                    current_time = block.next

            # для каждого из блоков
            for block in blocks:
                # если событие наступило для этого блока
                if current_time == block.next:
                    if not isinstance(block, Processor):
                        # для генератора 
                        # проверяем, может ли оператор обработать
                        next_generator, g_type = block.generate_request(current_time)
                        if next_generator is not None and next_generator.next == 0:
                            next_generator.next = \
                                current_time + next_generator.next_time(g_type)
                            created += 1
                        else:
                            refusals += 1
                        block.next = current_time + block.next_time()
                    else:
                        task = block.process_request(current_time)
                        # print(task)
                        if task != -1:
                            wait_times.append(task['wait_time'])
                        processed += 1
                        if len(block.queue) == 0:
                            block.next = 0
                        else:
                            block.next = current_time + block.next_time(task['type'])

        wait_time_middle = 0
        for time in wait_times:
            if (time != -1):
                wait_time_middle += time
        
        wait_time_middle /= len(wait_times)

        return {
                'time': current_time,
                "wait_time_middle": wait_time_middle
                }