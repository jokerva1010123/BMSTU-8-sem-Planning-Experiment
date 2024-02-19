from numpy.random import Generator as RandGen, default_rng
from numpy import float64
from math import sqrt, pi

class Service():
    def __init__(self, intense, sigma):
        self.m = 1 / intense
        self.sigma = sigma
    
    def set_mean(self, intense):
        self.m = 1 / intense

    def set_sigma(self, sigma):
        self.sigma = sigma

    def generate(self):
        gen = default_rng()
        res = -1
        while res <= 0:
            res = gen.normal(self.m, self.sigma)
        return res
    
class Generator():
    def __init__(self, intense):
        self.sigma = 1 / intense
    
    def set_intense(self, intense):
        self.sigma = 1 / intense

    def generate(self):
        gen = default_rng()
        return gen.exponential(self.sigma)
    
class Queue():
    def __init__(self, gen_intense, serv_intense, serv_deviation):
        self.service = Service(serv_intense, serv_deviation)
        self.generator = Generator(gen_intense)
    
    def set_gen_intense(self, gen_intense):
        self.generator.set_intense(gen_intense)
    
    def set_serv_intense(self, intense):
        self.service.set_mean(intense)
        
    def set_serv_deviation(self, sigma):
        self.service.set_sigma(sigma)

    def add_event(self, events, event: list):
        i = 0
        while i < len(events) and events[i][0] < event[0]:
            i += 1
        events.insert(i, event)

    def start(self, time):
        processed_tasks = 0
        cur_queue_len = 0
        max_queue_len = 0
        task_present = []
        gen_times = []
        serv_times = []

        events = [[0, 'g'],  [time, 't']]
        
        free, process_flag = True, False

        while min([ev[0] for ev in events]) < time:
            event = events.pop(0)
            # print(event)
            # Генератор
            if event[1] == 'g':
                task_present.append(-1 * event[0])
                cur_queue_len += 1
                if cur_queue_len > max_queue_len:
                    max_queue_len = cur_queue_len
                gen_times.append(self.generator.generate())
                self.add_event(events, [event[0] + gen_times[-1], 'g'])
                if free:
                    process_flag = True

            # Обработчик
            elif event[1] == 'p':
                processed_tasks += 1
                task_present[processed_tasks - 1] += event[0]
                process_flag = True

            if process_flag:
                if cur_queue_len > 0:
                    cur_queue_len -= 1
                    serv_times.append(self.service.generate())
                    self.add_event(events, [event[0] + serv_times[-1], 'p'])
                    free = False
                else:
                    free = True
                process_flag = False

        while (task_present[-1] < 0):
            task_present.pop()
        
        avg_gen = sum(gen_times) / len(gen_times)
        avg_service = sum(serv_times) / len(serv_times)
        # print(serv_times)
        # print(gen_times)
        # print(sum(serv_times))
        # print(sum(gen_times))
        return sum(task_present) / len(task_present) - avg_service #, processed_tasks, avg_service / avg_gen


        