
class Generator:
    def __init__(self, generator, count, g_type):
        self._generator = generator
        self.receivers = []
        self.num_requests = count
        self.next = 0 
        self.type = g_type

    def next_time(self):
        return self._generator.generate()
    
    def generate_request(self, time):
        if self.num_requests <= 0: 
            return None
        self.num_requests -= 1

        # Поиск обработчика с наименьшей очередью 
        receiver_min = self.receivers[0]
        min = len(self.receivers[0].queue)
        for receiver in self.receivers:
            if len(receiver.queue) < min: 
                min = len(receiver.queue)
                receiver_min = receiver
        receiver_min.receive_request(time, self.type)
        return receiver_min, self.type