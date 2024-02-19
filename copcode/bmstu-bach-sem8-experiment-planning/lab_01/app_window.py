from PyQt5 import QtWidgets, QtCore
from tqdm import tqdm
from distributions import ExponentialDistr, NormalDistr
from interface import Ui_MainWindow
import matplotlib.pyplot as plt

import numpy as np

from scipy.interpolate import make_interp_spline
from PyQt5.QtWidgets import QMessageBox

from model import Model
from request import RequestGenerator, RequestProcessor


class AppWindow(QtWidgets.QMainWindow):
    def __init__(self) -> None:
        super(AppWindow, self).__init__()
        self.ui_setup()

    def ui_setup(self) -> None:
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)

        self.bind_buttons()
        self.show()

    def bind_buttons(self) -> None:
        self.ui.calc_button.clicked.connect(self.calc_perform)
        self.ui.graph_button.clicked.connect(self.graph_perform)

    def calc_perform(self) -> None:
        try:
            gen_intensity = float(self.ui.exponential_intensity_entry.text())
            proc_intensity = float(self.ui.normal_intensity_entry.text())
            proc_range = float(self.ui.normal_delta_entry.text())
            time = float(self.ui.time_entry.text())

            processor = RequestProcessor(
                NormalDistr(proc_intensity, proc_range))
            generator = RequestGenerator(
                ExponentialDistr(gen_intensity), [processor])
            model = Model([generator], [processor])
            result = model.simulate_event_based(time)

            lambda_real = 1 / \
                (result.generators_results[0].total_generation_time /
                 result.generators_results[0].total_requests)
            mu_real = 1 / \
                (result.processors_results[0].total_processing_time /
                 result.processors_results[0].total_requests)

            system_load_real = lambda_real / mu_real
            system_load_exp = gen_intensity / proc_intensity

            QMessageBox.about(
                self, "Ответ", "Расчетная загрузка = {:.2f}\nРеальная загрузка = {:.2f}".format(
                    system_load_exp, system_load_real))

        except:
            QMessageBox.warning(self, "Внимание!",
                                "Некорректные входные данные")

    def model_benchmark(self,
                        time: float = 1000,
                        runs: int = 100,
                        load_range: tuple = (0.01, 1.01, 0.01),
                        gen_base_intensity: float = 1,
                        proc_base_intensity: float = 1,
                        proc_base_range: float = 0.02) -> tuple[list[float], list[float]]:
        load_list = np.arange(*load_range).tolist()

        avg_waiting_time_list = []

        for system_load in tqdm(load_list):
            total_runs_waiting_time = 0

            gen_intensity = gen_base_intensity * system_load
            proc_intensity = proc_base_intensity
            proc_range = proc_base_range

            for _ in range(runs):
                processor = RequestProcessor(
                    NormalDistr(proc_intensity, proc_range))

                generator = RequestGenerator(
                    ExponentialDistr(gen_intensity), [processor])

                model = Model([generator], [processor])
                result = model.simulate_event_based(time)
                total_runs_waiting_time += result.processors_results[0].avg_waiting_time

            avg_waiting_time_list.append(total_runs_waiting_time / runs)

        load_list.insert(0, 0)
        avg_waiting_time_list.insert(0, 0)

        return (load_list, avg_waiting_time_list)

    def graph_perform(self) -> None:
        load_list, avg_waiting_time_list = self.model_benchmark()

        avg_list_spline = make_interp_spline(load_list, avg_waiting_time_list)
        load_list_spline = np.linspace(load_list[0], load_list[-1], 20)
        avg_list_spline = make_interp_spline(load_list_spline, avg_list_spline(load_list_spline))
        load_list_spline = np.linspace(load_list[0], load_list[-1], 1000)

        plt.rcParams.update({'font.size': 22})
        plt.plot(load_list_spline, avg_list_spline(load_list_spline))
        plt.xlabel('Загрузка системы')
        plt.ylabel('Время ожидания')
        plt.title(
            'График зависимости среднего времени ожидания от загрузки системы')
        plt.grid(True)
        plt.show()
