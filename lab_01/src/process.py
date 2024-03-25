class Processor:
    def __init__(self, generator):
        self._generator = generator
        self.queue = []
        self.next = 0 # Время окончания следующей обработки

    def process_request(self, cur_time): # Обработать заявку (вернуть время обработки)
        push_time = self.queue.pop(0) # время прихода заявки, которая в очереди первая
        wait_time = cur_time - push_time # время ожидания в очереди
        return wait_time

    def receive_request(self, time): # Положить в очередь время прихода заявки
        self.queue.append(time)

    def next_time(self): # Получить время обработки по закону распределения
        return self._generator.generate()