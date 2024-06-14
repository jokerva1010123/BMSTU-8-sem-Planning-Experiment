class Processor:
    def __init__(self, generators):
        self._generators = generators
        self.queue = []
        self.next = 0

    def next_time(self, reqtype):
        return self._generators[reqtype].generate()

    def receive_request(self, time, reqtype):
        # self.queue.append(time)
        self.queue.append([time, reqtype])
        
    def process_request(self, cur_time):
        # push_time = self.queue.pop(0)
        push_time, reqtype = self.queue.pop(0)
        wait_time = cur_time - push_time
        return wait_time
