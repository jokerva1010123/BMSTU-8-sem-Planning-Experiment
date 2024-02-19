from math import sqrt

from numpy.random import uniform, weibull


class UniformDistribution:
    def __init__(self, mean, sigma=1):
        self.mean = mean
        self.halfdiff = max((sqrt(12 * sigma)) / 2, self.mean)

    def generate(self):
        return uniform(self.mean - self.halfdiff, self.mean + self.halfdiff)


class WeibullDistribution:
    def __init__(self, shape):
        self.shape = shape

    def generate(self):
        return weibull(self.shape)
