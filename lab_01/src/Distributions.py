  
from numpy.random import rayleigh, exponential

# Вариант 14
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