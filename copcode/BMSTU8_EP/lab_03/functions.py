from Modeller import Modeller
from EventGenerator import Generator
from Distributions import  RayleighDistribution, Exponentialistribution
from Processor import Processor
import math
from matplotlib import pyplot
from numpy import arange 

def modelling(clients_number, clients_proccessed, lambda_coming, lambda_obr, lambda_coming2=None, lambda_obr2=None): 
    sigma = (1/lambda_coming) * (math.pi / 2) ** (-1/2)
    sigma2 = sigma 
    if lambda_coming2: 
        sigma2 = (1/lambda_coming2) * (math.pi / 2) ** (-1/2)


    lam = (1/lambda_obr)
    lam2 = lam 
    if lambda_obr2:
        lam2 = (1/lambda_obr2) 

    generators = [
        Generator(
            RayleighDistribution(sigma),
            clients_number,
            0
        ), 
        Generator(
            RayleighDistribution(sigma2),
            clients_number,
            1
        ), 
    ]

    operators = [
            Processor(
                [Exponentialistribution(lam),
                Exponentialistribution(lam2)] 
            ),
        ]
        
    for generator in generators: 
        generator.receivers = operators.copy()

    model = Modeller(generators, operators)
    result = model.event_mode(clients_proccessed)
    print("Загрузка системы(расчетная): ", lambda_coming/lambda_obr, 
    "\nВремя работы:", result['time'], 
    "\nСреднее время ожидания: ", result['wait_time_middle'], 
    "\nКоличество обработанных заявок", clients_proccessed)
    return result


def view(start, end, N):
    print(start, end, N)
    Xdata = list()
    Ydata = list()

    lambda_obr = 100
    k = 2

    for lambda_coming in arange(int(start * 100), int(end * 100)/2, 1):
            result = modelling(
                clients_number=N+1000,
                clients_proccessed=N, 
                lambda_coming=lambda_coming,
                lambda_obr=lambda_obr
            )
            Xdata.append(lambda_coming*2/lambda_obr)
            Ydata.append(result['wait_time_middle'])

    pyplot.title('Среднее время ожидания')
    pyplot.grid(True)
    pyplot.plot(Xdata, Ydata)
    pyplot.xlabel("Коэффициент загрузки")
    pyplot.ylabel("Среднее время пребывания в очереди")
    pyplot.show()