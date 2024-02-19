import numpy as np
from distribution import UniformDistribution, WeibullDistribution
from event import Generator
from matplotlib import pyplot
from model import Modeller
from process import Processor


def modelling(clients_number, mean1, shape, standdev):
    generators = [Generator(UniformDistribution(mean1, standdev), clients_number)]
    operators = [Processor(WeibullDistribution(shape))]
    for generator in generators:
        generator.receivers = operators.copy()
    model = Modeller(generators, operators)
    return model.event_mode(clients_number)


def view(start, end, N, freq, standdev, exp_amount):
    Xdata = list()
    Ydata = list()

    step = 0.02
    for load_value in np.arange(start, end + step / 2, step):
        print(f"Loading progress: {load_value}")
        avg_wait_time_sum = 0
        for _ in range(exp_amount):
            result = modelling(N, 1 / (load_value * freq), 1 / freq, standdev)
            avg_wait_time_sum += result['avg_wait_time']

        Xdata.append(load_value)
        Ydata.append(avg_wait_time_sum / exp_amount)

    pyplot.title('График зависимости среднего времени пребывания в очереди от загрузки')
    pyplot.grid(True)
    pyplot.plot(Xdata, Ydata, "b")
    pyplot.xlabel("Коэффициент загрузки СМО")
    pyplot.ylabel("Среднее время пребывания в очереди")
    pyplot.show()
