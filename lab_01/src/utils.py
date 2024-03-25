import numpy as np
from distribution import UniformDistribution, WeibullDistribution, NormalDistribution
from event import Generator
import matplotlib.pyplot as plt
import numpy as np
from model import Modeller
from process import Processor


def modelling(clients_number, mx, sigma, a, b):
    generators = [Generator(NormalDistribution(mx, sigma), clients_number)]
    operators = [Processor(UniformDistribution(a, b))]
    for generator in generators:
        generator.receivers = operators.copy()
    model = Modeller(generators, operators)
    return model.event_mode(clients_number)

# Почему при убывании MX растет время ожидания. Потому что интервалы между генерацией уменьшаются.
# Надо ли выводить фактическое и рассчетное значение загрузки системы
# Как считать загрузку системы - интенсивность генератора / интенсивность обработчика
# Мы должны загруженность менять только для генераторов?
# Как для норм распре и равном считать параметры разброса?
def view(start, end, N, freq_gen, dev_gen, freq_proc, dev_proc, exp_amount):
    Xdata1 = list()
    Ydata1 = list()
    
    step = 0.02
    a = freq_gen / start - dev_proc
    b = freq_gen / start + dev_proc
    a = 0
    b = 1
    
    start = 0.01
    end = 1
    for load_value in np.arange(start, end + step / 2, step):
        print(f"Loading progress: {load_value}")
        avg_wait_time_sum = 0
        mx = ((a + b) / 2) * load_value
        mx = 1 / mx
        print(mx, (a + b) / 2, mx / ((a + b) / 2))
        for _ in range(exp_amount):
            result = modelling(N, mx, dev_gen, a, b)
            avg_wait_time_sum += result['avg_wait_time']

        Xdata1.append(load_value)
        Ydata1.append(avg_wait_time_sum / exp_amount)

    
    Xdata2 = list()
    Ydata2 = list()
   
    for load_value in np.arange(start, end + step / 2, step):
        print(f"Loading progress: {load_value}")
        avg_wait_time_sum = 0
        mx = ((a + b) / 2) * load_value
        mx = 1 / mx
        print(mx, (a + b) / 2, mx / ((a + b) / 2))
        for _ in range(exp_amount):
            result = modelling(N, mx, dev_gen, a, b)
            avg_wait_time_sum += result['avg_wait_time']

        Xdata2.append(load_value)
        Ydata2.append(avg_wait_time_sum / exp_amount)
        
    
    Xdata3 = list()
    Ydata3 = list()
   
    step = 0.5
    mx = 10
    dx = 5
    proc_intense_start = 5
    proc_intense_end = 20
    proc_dev = 2
    for proc_intense in np.arange(proc_intense_start, proc_intense_end + step / 2, step):
        print(f"Loading progress: {proc_intense}")
        avg_wait_time_sum = 0
        
        a = proc_intense - proc_dev
        b = proc_intense + proc_dev
        a = 1 / a
        b = 1 / b
        for _ in range(exp_amount):
            result = modelling(N, mx, dx, a, b)
            avg_wait_time_sum += result['avg_wait_time']

        Xdata3.append(proc_intense)
        Ydata3.append(avg_wait_time_sum / exp_amount)


    plt.figure(figsize=(10, 5))  # Задаем размер окна

    # Первый подграфик
    plt.subplot(2, 2, 1) 
    plt.title('Зависимость времени ожидания в очереди от загруженности системы')
    plt.grid(True)
    plt.plot(Xdata1, Ydata1, "b")
    plt.xlabel("Коэффициент загрузки СМО")
    plt.ylabel("Среднее время пребывания в очереди")

    # Второй подграфик
    plt.subplot(2, 2, 3)  
    plt.title("Зависимость времени ожидания в очереди от интенсивности генерации")
    #plt.title(f"Зависимость времени ожидания в очереди от интенсивности генерации (инт. обр = {2 / (b - a)})")
    plt.grid(True)
    plt.plot(Xdata2, Ydata2, "r")
    plt.xlabel("Интенсивность генерации")
    plt.ylabel("Среднее время пребывания в очереди")
    
    # Третий подграфик 
    plt.subplot(2, 2, 4)  
    plt.title('Зависимость времени ожидания в очереди от интенсивности обработки')
    plt.grid(True)
    plt.plot(Xdata3, Ydata3, "r")
    plt.xlabel("Интенсивность обработки")
    plt.ylabel("Среднее время пребывания в очереди")

    plt.tight_layout()  # Автоматически корректирует расположение подграфиков
    plt.show()
