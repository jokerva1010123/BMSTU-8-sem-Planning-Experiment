from process import Processor


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
            # Находим минимальное ненулевое значение .next среди генераторов и процессоров
            current_time = min(map(lambda x: x.next, filter(lambda x: x.next != 0, actors)))
            if free: # Если обработчик свободен
                free_time += current_time - prev_time

            for actor in actors:
                if current_time == actor.next: # Находим сущность, которая сгенерировала событие, и по времени окончания оно ближайшее
                    if isinstance(actor, Processor): # Если это обработчик
                        wait_time = actor.process_request(current_time) # Получаем время ожидания заявки в очереди
                        wait_times_sum += wait_time
                        processed += 1
                        if len(actor.queue) == 0: # Если очередь пуста, то пока не планируем обработку
                            actor.next = 0
                            free = True # Флаг простаивания
                        else:
                            actor.next = current_time + actor.next_time() # Ставим время, когда УЖЕ БУДЕТ обработана следующая
                    else:
                        receiver = actor.generate_request(current_time) # Создаем заявку (кладем в список заявок обработчика)
                        if receiver is not None: # Если заявок нет, то нечего обрабатывать
                            if receiver.next == 0: # Если нет времени обработки следующей заявки, то создаем
                                receiver.next = current_time + receiver.next_time()
                            actor.next = current_time + actor.next_time() # Создаем время генерации следующей заявки
                            free = False

            prev_time = current_time

        return {
            'time': current_time,
            "avg_wait_time": wait_times_sum / processed,
            "free_time": free_time
        }