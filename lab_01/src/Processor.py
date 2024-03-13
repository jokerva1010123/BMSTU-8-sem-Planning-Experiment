from EventGenerator import Generator
from numpy import random as nr

class Processor(Generator):
    def __init__(self, generator, max_queue=-1):
        self._generator = generator
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
        wait_time = time - task
        # print(wait_time)
        
        self.processed_requests += 1

        return wait_time
    
    # добавляем реквест в очередь
    def receive_request(self, time):
        # print(self.max_queue_size, self.current_queue_size ) 
        if self.max_queue_size != -1 and self.max_queue_size < len(self.queue):
            return False

        self.received_requests += 1
        self.queue.append(time)
        
        if self.max_reached_queue_size < len(self.queue):
            self.max_reached_queue_size = len(self.queue)
        return True

    def next_time(self):
        return self._generator.generate()