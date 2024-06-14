class Generator:
    def __init__(self, generator, count, reqtype):
        self._generator = generator
        self.receivers = []
        self.num_requests = count + 10
        self.next = 0
        self.reqtype = reqtype

    def next_time(self):
        return self._generator.generate()
    
    def generate_request(self, time):
        if self.num_requests <= 0: 
            self.next = 0
            return None
        self.num_requests -= 1

        min_queue_index = 0
        for i in range(1, len(self.receivers)):
            if len(self.receivers[i].queue) < len(self.receivers[min_queue_index].queue): 
                min_queue_index = i
        # self.receivers[min_queue_index].receive_request(time)
        self.receivers[min_queue_index].receive_request(time, self.reqtype)
        return self.receivers[min_queue_index]
