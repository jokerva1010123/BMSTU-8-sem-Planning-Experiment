from math import sqrt

from numpy.random import uniform, weibull, rayleigh, exponential

import random

class UniformDistribution2:
    def __init__(self, mean, sigma=1):
        self.mean = mean
        self.halfdiff = max((sqrt(12 * sigma)) / 2, self.mean)

    def generate(self):
        return uniform(self.mean - self.halfdiff, self.mean + self.halfdiff)


class WeibullDistribution2:
    def __init__(self, shape):
        self.shape = shape

    def generate(self):
        return weibull(self.shape)
        
class WeibullDistribution:
    def __init__(self, k: float, lambd: float):
        self._k = k
        self._lambd = lambd

    def generation_time(self):
        return weibull_min.rvs(self._k, loc=0, scale=self._lambd)
        
class UniformDistribution:
    def __init__(self, a, b):
        self.a = a
        self.b = b

    def generate(self):
        return random.uniform(self.a, self.b)
        
class NormalDistribution:
    def __init__(self, mx, sigma):
        self.mx = mx
        self.sigma = sigma

    def generate(self):
        return random.gauss(self.mx, self.sigma)
        
class UniformDistributionIntense:
    def __init__(self, a, b):
        self.a = a
        self.b = b

    def generate(self):
        return random.uniform(1 / self.a, 1 / self.b)
        
class NormalDistributionIntense:
    def __init__(self, mx, sigma):
        self.mx = mx
        self.sigma = sigma

    def generate(self):
        return random.gauss(1 / self.mx, self.sigma)
        
class RayleighDistribution:
    def __init__(self, sigma: float):
        self.sigma = sigma

    def generate(self):
        return rayleigh(self.sigma)
    
class Exponentialistribution:
    def __init__(self, lambdaParam: float):
        self.lambdaParam = lambdaParam

    def generate(self):
        return exponential(self.lambdaParam)