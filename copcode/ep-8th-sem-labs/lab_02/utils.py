from distribution import UniformDistribution, WeibullDistribution
from event import Generator
from model import Modeller
from process import Processor


def modelling(clients_number, mean1, shape, standdev):
    generators = [Generator(UniformDistribution(mean1, standdev), clients_number)]
    operators = [Processor(WeibullDistribution(shape))]
    for generator in generators:
        generator.receivers = operators.copy()
    model = Modeller(generators, operators)
    return model.event_mode(clients_number)
