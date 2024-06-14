import numpy as np
from numpy.random import rayleigh, uniform
from matplotlib import pyplot as plt


def rayleigh_intensity(params):
    t = rayleigh(params[0], 1)[0]
    while t < 0:
        t = rayleigh(params[0], 1)[0]
    return t


def uniform_intensity(params):
    # res = -1
    # while res < 0:
    res = abs(uniform(params[0] - params[1], params[0] + params[1]))
    return res


class Generator:
    def __init__(self, func, params):
        self.law = func
        self.params = params

    def generation_time(self):
        return self.law(self.params)


class EventModel:
    def __init__(self, generators, processor, total_apps=0):
        self.generators = generators
        self.processor = processor
        self.total_apps = total_apps

    def proceed(self):
        processed = 0
        self.queue = []
        self.events = []
        self.totally_waited = 0
        i = 0
        for generator in self.generators:
            self.events.append([generator.generation_time(), 'g', i])
            i += 1
        self.free = True
        while processed < self.total_apps:
            event = self.events.pop(0)
            if event[1] == 'g':
                self._generate(event)
            elif event[1] == 'p':
                processed += 1
                self._process(event[0])

        return self.totally_waited

    def _add_event(self, event):
        i = 0
        while i < len(self.events) and self.events[i][0] < event[0]:
            i += 1
        self.events.insert(i, event)

    def _generate(self, event):
        self.queue.append(event[0])
        self._add_event([event[0] + self.generators[event[2]].generation_time(), 'g', event[2]])
        if self.free:
            self._process(event[0])

    def _process(self, time):
        if len(self.queue) > 0:
            processing_time = self.processor.generation_time()
            self.totally_waited += processing_time + time - self.queue.pop(0)
            self._add_event([time + processing_time, 'p'])
            self.free = False
        else:
            self.free = True


# def view(total_apps, proc_dev):
#     max_int = 100
#     proc = Generator(uniform_intensity, (1, 0.5))
#     Xdata = list()
#     Ydata = list()

#     # for intensity in np.arange(0.1, max_int + 1, 0.1):
#     i = 0.001
#     while i < 1.01:
#         gen = Generator(rayleigh_intensity, (1 / i,))
#         model = EventModel([gen], proc, total_apps)
#         Xdata.append(i)#(intensity / max_int)
#         # temp = (model.proceed() / total_apps) - 2
#         Ydata.append(model.proceed() / total_apps)

#         i = round(i + 0.01, 2)

#     Xdata.reverse()
#     pyplot.title('Average awaiting time')
#     pyplot.grid(True)
#     pyplot.plot(Xdata, Ydata)
#     pyplot.xlabel("Strain (p)")
#     pyplot.ylabel("Average time")
#     pyplot.show()
def view(total_apps, proc_dev):
    max_int = 100
    proc = Generator(uniform_intensity, (35, proc_dev))
    Xdata = []
    Ydata = []

    for intensity in range(1, max_int + 2):
        print(intensity)
        gen = Generator(rayleigh_intensity, (intensity,))
        sum = 0
        for i in range(1, 1000):
            model = EventModel([gen], proc, total_apps)
            sum += model.proceed()
        Xdata.append((intensity - 1) / max_int)
        y = sum / (100 * total_apps) - 1
        if y < 0:
            y = 0
        Ydata.append(y)

    Ydata.reverse()
    delta_zero = Ydata[0]
    for i in range(0, len(Ydata)):
        Ydata[i] -= delta_zero

    plt.plot(Xdata, Ydata, '#2eb821')
    plt.grid(True)
    plt.title("Генератор: Рэлея; ОА: равномерный")
    plt.ylabel('Время пребывания заявки в СМО')
    plt.xlabel('Загрузка системы')
    plt.show()
    # pyplot.title('Average awaiting time')
    # pyplot.grid(True)
    # pyplot.plot(Xdata, Ydata)
    # pyplot.xlabel("Strain (p)")
    # pyplot.ylabel("Average time")
    # pyplot.show()


if __name__ == "__main__":
    total_apps = 1
    total_apps = int(input("Enter total apps amount: "))
    if total_apps < 1:
        print("Input error.\n")
        exit(1)

    proc_int = float(input("Enter processor intensity: "))
    proc_dev = float(input("Enter processor range: "))

    gen_amount = 1
    # gen_amount = int(input("Enter generators amount: "))
    gens = []
    gen_int_sum = 0
    for i in range(gen_amount):
        gen_int = float(input("Enter generator intensity: "))
        gens.append(Generator(rayleigh_intensity, (gen_int,)))
        gen_int_sum += gen_int

    proc = Generator(uniform_intensity, (proc_int, proc_dev))
    model = EventModel(gens, proc, total_apps)

    time = model.proceed()
    print("Strain: p =", gen_int_sum / proc_int, "\nTotal awaiting time:", time, "\nAverage time: ", time / total_apps)

    view(total_apps, proc_dev)


















# import sys
# # import math

# # import numpy.random as nr
# # import matplotlib.pyplot as plt
# # import matplotlib as mpl
# from prettytable import PrettyTable

# from PyQt5.QtWidgets import QApplication, QMainWindow, QTableWidgetItem, QMessageBox

# from mainwindow import Ui_MainWindow
# # from graph import Generator, EventModel, rayleigh_intensity, uniform_intensity, view


# # class UniformGenerator:
# #     def __init__(self, intensivity, range=1):
# #         self.mean = intensivity
# #         self.hdiff = max(math.sqrt(12 * range) / 2, intensivity)

# #     def generation_time(self):
# #         return nr.uniform(self.mean - self.hdiff, self.mean + self.hdiff)


# # class RayleighGenerator:
# #     def __init__(self, sigma):
# #         self.sigma = sigma

# #     def generation_time(self):
# #         t = nr.rayleigh(self.sigma, 1)[0]
# #         while t < 0:
# #             t = nr.rayleigh(self.sigma, 1)[0]
# #         return t


# # class RequestGenerator:
# #     def __init__(self, generator):
# #         self._generator = generator
# #         self._receivers = set()
# #         self.time_periods = []

# #     def add_receiver(self, receiver):
# #         self._receivers.add(receiver)

# #     def remove_receiver(self, receiver):
# #         try:
# #             self._receivers.remove(receiver)
# #         except KeyError:
# #             pass

# #     def next_time_period(self):
# #         time = self._generator.generation_time()
# #         self.time_periods.append(time)
# #         return time

# #     def emit_request(self):
# #         for receiver in self._receivers:
# #             receiver.receive_request()


# # class RequestProcessor:
# #     def __init__(self, generator, len_queue=0, reenter_probability=0):
# #         self._generator = generator
# #         self._current_queue_size = 0
# #         self._max_queue_size = 0
# #         self._processed_requests = 0
# #         self._reenter_probability = reenter_probability
# #         self._reentered_requests = 0
# #         self._len_queue = len_queue
# #         self._num_lost_requests = 0
# #         self.time_periods = []

# #     @property
# #     def processed_requests(self):
# #         return self._processed_requests

# #     @property
# #     def lost_requests(self):
# #         return self._num_lost_requests

# #     @property
# #     def max_queue_size(self):
# #         return self._max_queue_size

# #     @property
# #     def current_queue_size(self):
# #         return self._current_queue_size

# #     @property
# #     def reentered_requests(self):
# #         return self._reentered_requests

# #     def process(self):
# #         if self._current_queue_size > 0:
# #             time_processed_request.append(current_time)
# #             self._processed_requests += 1
# #             self._current_queue_size -= 1

# #     def receive_request(self):
# #         self._current_queue_size += 1
# #         if self._current_queue_size > self._max_queue_size:
# #             self._max_queue_size += 1

# #     def next_time_period(self):
# #         time = self._generator.generation_time()
# #         self.time_periods.append(time)
# #         return time


# # current_time = 0
# # time_processed_request = []

# # class Modeller:
# #     def __init__(self, generator, processor):
# #         self._generator = generator
# #         self._processor = processor
# #         self._generator.add_receiver(self._processor)

# #     def time_based_modelling(self, dt, time_modelling):
# #         global current_time
# #         global time_processed_request
# #         global p_teor
# #         time_processed_request.clear()
# #         current_time = 0
# #         generator = self._generator
# #         processor = self._processor
# #         queue_size = [0]
# #         time_generated_request = []
# #         num_requests = [0]


# #         gen_period = generator.next_time_period()
# #         proc_period = gen_period + processor.next_time_period()

# #         while current_time < time_modelling :
# #             num = num_requests[-1]
# #             if gen_period <= current_time:
# #                 time_generated_request.append(current_time)
# #                 generator.emit_request()
# #                 num += 1
# #                 gen_period += generator.next_time_period()
# #             if proc_period <= current_time:
# #                 if processor.current_queue_size > 0:
# #                     num -= 1
# #                 processor.process()

# #                 if processor.current_queue_size > 0:
# #                     proc_period += processor.next_time_period()
# #                 else:
# #                     proc_period = gen_period + processor.next_time_period()
# #             queue_size.append(processor.current_queue_size)


# #             current_time += dt
# #             num_requests.append(num)

# #         lambda_fact = 1 / (sum(generator.time_periods) / len(generator.time_periods))
# #         mu_fact = 1 / (sum(processor.time_periods) / len(processor.time_periods))
# #         p = lambda_fact / mu_fact
# #         num_reports_teor = p / (1 - p)
# #         num_reports_fact = sum(queue_size) / len(queue_size)
# #         k = num_reports_fact / num_reports_teor

# #         if p_teor >= 1 or p_teor <= 0 or k == 0:
# #             k = 1

# #         if (len(time_processed_request)):
# #             mas_time_request_in_smo = []
# #             for i in range(len(time_processed_request)):
# #                 mas_time_request_in_smo.append(time_processed_request[i] - time_generated_request[i])
# #             avg_time_in_smo = sum(mas_time_request_in_smo) / len(mas_time_request_in_smo) / k
# #         else:
# #             avg_time_in_smo = 0

# #         result = [
# #             processor.processed_requests,
# #             processor.reentered_requests,
# #             processor.max_queue_size,
# #             current_time,
# #             sum(queue_size) / len(queue_size),
# #             lambda_fact,
# #             mu_fact,
# #             avg_time_in_smo
# #         ]
# #         return result

# # def create_graph():
# #     i = 0.001
# #     mas = []
# #     res = []
# #     while i < 1.01:
# #         print(i)
# #         mas_i = []
# #         for j in range(100):
# #             step = 0.1
# #             time_modelling = 1000
# #             intensivity_gen = i
# #             intensivity_proc = 1
# #             range_proc = 1
# #             generator = RequestGenerator(RayleighGenerator(1 / intensivity_gen))
# #             OA = UniformGenerator(1 / intensivity_proc, 1 / range_proc)
# #             processor = RequestProcessor(OA)
# #             model = Modeller(generator, processor)
# #             result = model.time_based_modelling(step, time_modelling)[7]
# #             mas_i.append(result)
# #         mas.append(i)
# #         temp = abs(sum(mas_i)/(len(mas_i) + 1)) - 1
# #         if temp < 0:
# #             temp = 0
# #         res.append(temp)
# #         mas_i.clear()

# #         # if i < 0.1:
# #         #     i += 0.01
# #         # else:
# #         i += 0.05
# #         i = round(i, 2)

# #     mpl.style.use('seaborn')
# #     plt.plot(mas, res, '#2eb821')
# #     plt.grid(True)
# #     plt.title("Генератор: Рэлея; ОА: равномерный")
# #     plt.ylabel('Время пребывания заявки в СМО')
# #     plt.xlabel('Загрузка системы')
# #     plt.show()

# # def main():
# #     intensivity_gen = 3
# #     intensivity_proc = 4
# #     range_proc = 1

# #     step = 0.1
# #     time_modelling = 10000

# #     generator = RequestGenerator(RayleighGenerator(intensivity_gen))
# #     OA = UniformGenerator(1 / intensivity_proc, range_proc)
# #     processor = RequestProcessor(OA)
# #     model = Modeller(generator, processor)
# #     result_tb = model.time_based_modelling(step, time_modelling)

# #     p = intensivity_gen / intensivity_proc
# #     table = PrettyTable()
# #     column1 = ''
# #     names = [column1, 'Теоретич.', 'Фактич.']
# #     table.field_names = names
# #     row = ['Загруженность системы', round(p, 2), round(result_tb[5] / result_tb[6], 3)]
# #     table.add_row(row)
# #     # row = ['Средняя длина очереди', round(p ** 2 / (1 - p), 2)]
# #     # table.add_row(row)
# #     # row = ['Среднее время ожидания заявки в очереди', round((p ** 2) / ((1 - p) * intensivity_gen), 2)]
# #     # table.add_row(row)
# #     # row = ['Среднее число заявок в СМО', round(p / (1 - p), 2)]
# #     # table.add_row(row)
# #     row = ['Среднее время пребывания заявки в СМО', round(p / (1 - p) / intensivity_gen, 2), round(result_tb[7], 2)]
# #     table.add_row(row)
# #     # row = ['----------------', '--------']
# #     # table.add_row(row)
# #     row = ['Обработанные заявки', '########', result_tb[0]]
# #     table.add_row(row)
# #     # row = ['Максимальная длина очереди', result_tb[2]]
# #     # table.add_row(row)
# #     row = ['Общее время моделирования', '########', round(result_tb[3], 3)]
# #     table.add_row(row)
# #     # row = ['Загруженность системы', round(result_tb[5] / result_tb[6], 3)]
# #     # table.add_row(row)
# #     # row = ['Средняя длина очереди', round(result_tb[4], 3)]
# #     # table.add_row(row)

# #     # num_reports_teor = p / (1 - p)
# #     # num_reports_fact = result_tb[4]
# #     # k = num_reports_fact / num_reports_teor
# #     # row = ['Среднее время пребывания заявки в СМО', round(result_tb[7], 2)]
# #     # table.add_row(row)

# #     table.align = 'r'
# #     table.align[column1] = "l"
# #     print(table)
# #     print(str(table))
# #     # create_graph()