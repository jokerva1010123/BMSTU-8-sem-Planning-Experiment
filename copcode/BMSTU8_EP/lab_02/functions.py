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
        ), 
    ]

    operators = [
            Processor(
                Exponentialistribution(1/lambda_obr)
            ),]

    for generator in generators: 
        generator.receivers = operators.copy()

    model = Modeller(generators, operators)
    result = model.event_mode(clients_proccessed)
    print("Загрузка системы(расчетная): ", lambda_coming/lambda_obr, 
    "\nВремя работы:", result['time'], 
    "\nСреднее время ожидания: ", result['wait_time_middle'], 
    "\nКоличество обработанных заявок", clients_proccessed)
    return result