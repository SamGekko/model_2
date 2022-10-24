import os.path
import random
from typing import Any, Generator
import inspect
from scipy.stats import pearsonr
import _tkinter
import seaborn as sns
from tqdm import trange
import matplotlib.pyplot as plt


# мультипликативный метод генерации последовательности псевдослучайных чисел
def rand(a: int, b: int, m: int, x: Any = 0) -> Generator[int, Any, None]:
    while True:
        x = (a * x + b) % m
        yield x


# рандомайзер чисел от а до b длиной n с заданием начальной точки мультипликативной генерации x0
def rand_num(a: Any, b: Any, n: int, x0: Any) -> list:
    a_seed = 22693477
    b_mult = 1
    m_mod = 2 ** 12

    p_list = rand(a_seed, b_mult, m_mod, x0)

    out_mas = []

    for _ in range(n):
        num = (b - a) * (next(p_list) / (m_mod - 1)) + a
        out_mas.append(num)

    return out_mas


# Математическое ожидание
def mat(x: list) -> float:
    out = 0
    for each in x:
        out += each
    out = out / len(x)
    return out


# Дисперсия
def dis(x: list) -> float:
    out = 0
    for each in x:
        out += each ** 2
    return (out / len(x) - mat(x) ** 2) * len(x) / (len(x) - 1)


# Период
def period(x: list):
    per = 0
    for k1 in range(len(x) - 1):
        for k2 in range(k1 + 1, len(x)):
            if (x[k1] == x[k2]) & (k1 != k2):
                per = k2 - k1
                return per
    if per == 0:
        return None


def his_out(x: list, title: str = 'Histogram'):
    for k in range(len(x)):
        sns.displot(x[k], bins=[0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10])
    try:
        plt.title(title)
        plt.show()

    except _tkinter.TclError:
        pass


def rand_def(a: float, b: float, ik: int) -> list:
    out_l = []
    for _ in range(10 ** (2 + ik)):
        out_l.append(random.uniform(a, b))
    return out_l


if __name__ == '__main__':
    print("----------Практическая работа номер 2---------------")
    print("Задание 1:\n"
          "Мультипликативный метод генерации последовательности псевдослучайных чисел:\n"
          "---------------------------------------------------------------------------\n"
          f"{inspect.getsource(rand)}\n"
          "---------------------------------------------------------------------------\n"
          "Задание 2:\n"
          "---------------------------------------------------------------------------")
    out_m = []
    out_m_default = []
    file_path = 'logs/random_numbers'
    if not os.path.exists(file_path):
        os.makedirs(file_path)
    for i in trange(4):
        ffile = open(f'{file_path}/log_{i + 1}.txt', 'w')
        out_m.append(rand_num(0, 10, 10 ** (2 + i), 1))
        out_m_default.append(rand_def(0, 10, i))
        f_ns = out_m[i]
        f_ns_default = out_m_default[i]
        ffile.write('--------------------\n'
                    f'Output_Number_{i + 1}\n'
                    f'Output_Length: ' + str(len(f_ns)) +
                    '\n----------------------\n'
                    + str(f_ns) + '\n'
                                  '------------------------\n'
                                  'Delault:\n'
                    + str(f_ns_default) + '\n')
        ffile.close()
    print(f"Все выходные данные получены и записаны. Смотрите {file_path}/\n"
          "--------------------------------------------------------------------------\n"
          "Задание 3:\n"
          "Математическое ожидание и дисперсия полученных последовательностей.\n"
          "--------------------------------------------------------------------------")
    for i in range(4):
        mato_exp = mat(out_m[i])
        mato_exp_default = mat(out_m_default[i])
        disp_exp = dis(out_m[i])
        disp_exp_default = dis(out_m_default[i])
        mato_t = 5
        disp_t = (10 ** 2) / 12
        print(f"Математическое ожидание M_{i + 1} = {mato_exp}\n"
              f"Дисперсия D_{i + 1} = {disp_exp}\n"
              "Погрешности:\n"
              f"Eps_M_{i + 1} = {abs((mato_t - mato_exp) / mato_t) * 100} %\n"
              f"Eps_D_{i + 1} = {abs((disp_t - disp_exp) / disp_t) * 100} %\n"
              "--------------------------------\n"
              f"Математическое ожидание для встроенного генератора Def_M_{i + 1} = {mato_exp_default}\n"
              f"Дисперсия для встроенного генератора Def_D_{i + 1} = {disp_exp_default}\n"
              "Погрешности:\n"
              f"Def_Eps_M_{i + 1} = {abs((mato_t - mato_exp_default) / mato_t) * 100} %\n"
              f"Def_Eps_D_{i + 1} = {abs((disp_t - disp_exp_default) / disp_t) * 100} %\n"
              "--------------------------------\n")
    print("Задание 4:\n"
          "Период сгенерированных последовательностей:")
    for i in range(4):
        print(f"Период {i + 1}-й последовательности p_{i + 1} = {period(out_m[i])}")
        print(f"Период {i + 1}-й последовательности для встроенного генератора "
              f"def_p_{i + 1} = {period(out_m_default[i])}")
    his_out(out_m, 'Histogram')
    his_out(out_m_default, 'Histogram Default')
    for i in range(4):
        x_m = []
        for j in range(10 ** (i + 1)):
            x_m.append(0)
            x_m.append(1)
            x_m.append(2)
            x_m.append(3)
            x_m.append(4)
            x_m.append(5)
            x_m.append(6)
            x_m.append(7)
            x_m.append(8)
            x_m.append(9)
        print(f"{i + 1} критерий Пирсона:\n{pearsonr(x_m, out_m[i])}")
        print(f"{i + 1} критерий Пирсона для вcтроенного генератора:\n{pearsonr(x_m, out_m_default[i])}")
