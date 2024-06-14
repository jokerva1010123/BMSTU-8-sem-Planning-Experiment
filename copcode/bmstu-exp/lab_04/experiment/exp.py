import numpy as np
from matplotlib import pyplot as plt

from .distrib import RayleighDistribution, UniformDistribution, ExponentialDistribution
from .processor import Processor
from .generator import Generator
from .modeller import Modeller


def modelling(clients_number, mean1, mean2, mean3, standdev): 
    generators = [Generator(RayleighDistribution(mean1), clients_number, reqtype=0), Generator(RayleighDistribution(mean2), clients_number, reqtype=1)]
    operators = [Processor([ExponentialDistribution(mean3), ExponentialDistribution(mean3 + 0.25 * mean3)])]
    # operators = [Processor(UniformDistribution(mean3, standdev))]
    for generator in generators: 
        generator.receivers = operators.copy()

    model = Modeller(generators, operators)
    result = model.event_mode(clients_number)

    print(
        "###############\nЗагрузка системы (расчетная): ", mean2 / mean1,
        "\n\tВремя работы:", result['time'],
        "\n\tСреднее время пребывания: ", result['avg_wait_time'],
        "\n\tКоличество обработанных заявок", clients_number,
        "\n###############"
    )
    return result


def view(start=0.01, end=1.0, N=1000, freq=0.5, standdev=1.0, exp_amount=80):
    Xdata = []
    Ydata = []

    step = 0.02
    for load_value in np.arange(start, end + step / 2, step):
        print(f"<CURRENT VALUE>: {load_value}")
        avg_wait_time_sum = 0
        for _ in range(exp_amount):
            result = modelling(N, 1 / (load_value * 0.7), 1 / freq, standdev)
            # result = _modelling(N, load_value * 1e2, 35, standdev)
            avg_wait_time_sum += result['avg_wait_time']

        Xdata.append(load_value)
        Ydata.append(avg_wait_time_sum / exp_amount)

    plt.title("График зависимости среднего времени пребывания в очереди от загрузки\nГенератор: Рэлея; ОА: равномерный")
    plt.grid(True)
    plt.plot(Xdata, Ydata, "#2eb821")
    plt.xlabel("Коэффициент загрузки СМО")
    plt.ylabel("Среднее время пребывания в очереди")
    plt.show()
