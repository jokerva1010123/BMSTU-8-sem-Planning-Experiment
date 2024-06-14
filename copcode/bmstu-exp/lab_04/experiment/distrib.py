import math
import numpy as np


class RayleighDistribution:
    def __init__(self, sigma):
        self.sigma = sigma

    def generate(self):
        t = np.random.rayleigh(self.sigma, 1)[0]
        while t < 0:
            t = np.random.rayleigh(self.sigma, 1)[0]
        return t


class UniformDistribution:
    def __init__(self, mean, sigma=1):
        self.mean = mean
        self.halfdiff = max((math.sqrt(12 * sigma)) / 2, self.mean)

    def generate(self):
        return np.random.uniform(self.mean - self.halfdiff, self.mean + self.halfdiff)


class ExponentialDistribution:
    def __init__(self, mean):
        self.mean = mean

    def generate(self):
        return np.random.exponential(self.mean)
