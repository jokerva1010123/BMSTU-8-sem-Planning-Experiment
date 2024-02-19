from EventGenerator import Generator
from numpy import random as nr

class Processor(Generator):
    def __init__(self, generators, max_queue=-1):
        self._generators = generators
        self.processed_requests = 0
        self.received_requests  = 0
        self.queue = []

        self.max_queue_size = max_queue
        self.max_reached_queue_size = 0

        self.next = 0

# обрабатываем запрос, если они есть
    def process_request(self, time):
        if len(self.queue) == 0:
            return -1

        task = self.queue.pop(0)
        task['wait_time']  = time - task['time']
        # print(wait_time)
        
        self.processed_requests += 1
        # print(task)
        return task
    
# добавляем реквест в очередь
    def receive_request(self, time, g_type):
        self.received_requests += 1
        self.queue.append({
            'time': time, 
            'type': g_type,
            'wait_time': 0
        })
        
        if self.max_reached_queue_size < len(self.queue):
            self.max_reached_queue_size = len(self.queue)
        return True

    def next_time(self, g_type):
        return self._generators[g_type].generate()