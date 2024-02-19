class Processor:
    def __init__(self, generator):
        self._generator = generator
        self.queue = []
        self.next = 0

    def process_request(self, cur_time):
        push_time = self.queue.pop(0)
        wait_time = cur_time - push_time
        return wait_time

    def receive_request(self, time):
        self.queue.append(time)

    def next_time(self):
        return self._generator.generate()
