class Generator:
    def __init__(self, generator, count):
        self._generator = generator # Генератор значений по закону распределения
        self.receivers = [] # Массив обработчиков
        self.num_requests = count + 10 # Кол-во заявок
        self.next = 0 # Время, когда будет УЖЕ сгенерирована следующая заявка

    def next_time(self):
        return self._generator.generate()

# Здесь выбираем обработчика с минимальной очередью и кладем в его очередь время прихода заявки
    def generate_request(self, time):
        if self.num_requests <= 0:
            self.next = 0
            return None
        self.num_requests -= 1

        min_queue_index = 0
        for i in range(1, len(self.receivers)):
            if len(self.receivers[i].queue) < len(self.receivers[min_queue_index].queue):
                min_queue_index = i
        self.receivers[min_queue_index].receive_request(time)
        return self.receivers[min_queue_index]