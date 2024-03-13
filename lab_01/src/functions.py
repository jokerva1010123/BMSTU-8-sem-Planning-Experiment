from Modeller import Modeller
from EventGenerator import Generator
from Distributions import  RayleighDistribution, Exponentialistribution
from Processor import Processor
import math
from matplotlib import pyplot

def modelling(clients_number, clients_proccessed, lambda_coming, lambda_obr): 
    sigma = (1/lambda_coming) * (math.pi / 2) ** (-1/2)

    generators = [
        Generator(
            RayleighDistribution(sigma),
            clients_number,
        ),]

    operators = [
            Processor(
                Exponentialistribution(1/lambda_obr)
            ),]

    for generator in generators: 
        generator.receivers = operators.copy()

    model = Modeller(generators, operators)
    result = model.event_mode(clients_proccessed)
    return result


def view(start, end, N):
    Xdata = list()
    Ydata = list()

    lambda_obr = 100

    for lambda_coming in range(int(start * 100), int(end * 100), 5):
        print("lambda_coming = {}".format(lambda_coming))
        wait_time_middles = []
        for _ in range(100):
            result = modelling(
                clients_number=N+1000,
                clients_proccessed=N, 
                lambda_coming=lambda_coming,
                lambda_obr=lambda_obr
            )
            wait_time_middles.append(result['wait_time_middle'])

        Xdata.append(lambda_coming/lambda_obr)
        Ydata.append(sum(wait_time_middles) / len(wait_time_middles))

    pyplot.title('Зависимость от загрузки заявок')
    pyplot.grid(True)
    pyplot.plot(Xdata, Ydata)
    pyplot.xlabel("Коэффикиент загрузки СМО")
    pyplot.ylabel("Среднее время ожидание в очереди")
    pyplot.show()

def view1(start, end, N):
    Xdata = list()
    Ydata = list()

    lambda_obr = 100

    for lambda_coming in range(int(start * 100), int(end * 100), 7):
        print("lambda_coming = {}".format(lambda_coming))
        wait_time_middles = []
        for _ in range(100):
            result = modelling(
                clients_number=N+1000,
                clients_proccessed=N, 
                lambda_coming=lambda_coming,
                lambda_obr=lambda_obr
            )
            wait_time_middles.append(result['wait_time_middle'])

        Ydata.append(lambda_coming)
        Xdata.append(sum(wait_time_middles) / len(wait_time_middles))

    pyplot.title('Зависимость от интенсивности генерации заявок')
    pyplot.grid(True)
    pyplot.plot(Xdata, Ydata)
    pyplot.xlabel("Среднее время ожидание в очереди")
    pyplot.ylabel("Интенсивности генерации")
    pyplot.show()