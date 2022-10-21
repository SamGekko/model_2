import os.path
from typing import Any, Generator
import inspect
from tqdm import tqdm, trange


# мультипликативный метод генерации последовательности псевдослучайных чисел
def rand(a: int, b: int, m: int, x: Any = 0) -> Generator[int, Any, None]:
    while True:
        x = (a * x + b) % m
        yield x


# рандомайзер чисел от а до b длиной n с заданием начальной точки мультипликативной генерации x0
def rand_num(a: Any, b: Any, n: int, x0: Any) -> list:
    #a_seed = 22693477
    #a_seed = 0.1234567 * ((n / 10**4)+10**2)
    #b_mult = 1
    m_mod = 2 ** 12
    #m_mod = ((n / 10**4)+10**2)
    #a_seed = 22693477 --
    #b_mult = 1 --
    #m_mod = 10**5+1
    #m_mod = 2**13 --
    a_seed = 777
    b_mult = 2
    #m_mod = 2134

    p_list = rand(a_seed, b_mult, m_mod, x0)

    out_mas = []

    for _ in range(n):
        num = (b - a) * (next(p_list) / (m_mod - 1)) + a
        out_mas.append(round(num))

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


#Алгоритм z
def compute_z(x: list) -> list:
    n = len(x)
    z = [0] * n

    zbox_l, zbox_r, z[0] = 0, 0, n
    for k in range(1, n):
        if k < zbox_r:              # k is within a zbox
            k = k - zbox_l
            if z[k] < zbox_r - k:
                z[k] = z[k]         # Full optimization
                continue
            zbox_l = k              # Partial optimization
        else:
            zbox_l = zbox_r = k     # Match from scratch
        while zbox_r < n and x[zbox_r - zbox_l] == x[zbox_r]:
            zbox_r += 1
        z[k] = zbox_r - zbox_l
    return z


# Период последовательности
def period(x: list) -> int:
    z = compute_z(x)
    for k in range(1, len(z)):
        if (k+z[k] == len(x)) & (len(x) % k == 0):
            return k


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
    file_path = 'logs/random_numbers'
    if not os.path.exists(file_path):
        os.makedirs(file_path)
    for i in trange(5):
        ffile = open(f'{file_path}/log_{i + 1}.txt', 'w')
        out_m.append(rand_num(0, 10, 10 ** (4 + i), 1))
        f_ns = out_m[i]
        ffile.write('--------------------\n'
                    f'Output_Number_{i + 1}\n'
                    f'Output_Length: ' + str(len(f_ns)) +
                    '\n----------------------\n'
                    + str(f_ns) + '\n')
        ffile.close()
    print(f"Все выходные данные получены и записаны. Смотрите {file_path}/\n"
          "--------------------------------------------------------------------------\n"
          "Задание 3:\n"
          "Математическое ожидание и дисперсия полученных последовательностей.\n"
          "--------------------------------------------------------------------------")
    for i in range(5):
        mato_exp = mat(out_m[i])
        disp_exp = dis(out_m[i])
        mato_t = 5
        disp_t = (10 ** 2) / 12
        print(f"Математическое ожидание M_{i + 1} = {mato_exp}\n"
              f"Дисперсия D_{i + 1} = {disp_exp}\n"
              "Погрешности:\n"
              f"Eps_M_{i + 1} = {abs((mato_t - mato_exp) / mato_t) * 100} %\n"
              f"Eps_D_{i + 1} = {abs((disp_t - disp_exp) / disp_t) * 100} %\n"
              "--------------------------------")
    print("Задание 4:\n"
          "Период сгенерированных последовательностей:")
    print(out_m[0])
    print(period(out_m[0]))
    for i in range(5):
        print(f"Период {i+1}-й последовательности p_{i+1} = {period(out_m[i])}")
