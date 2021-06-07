import logging
import math
import colorama
from colorama import Fore, Style

def v_p_intrg(x, y):
    return math.cos(y) * math.sin(y)

def double_integr_trap(func=v_p_intrg, a1=0, b1=math.pi / 2, h1=0.1,
                       a2=0, b2=2 * math.pi, h2=0.1,
                       cond_enabled=False, ksi=0,
                       z_lower_border_target=-12.75,
                       z_higher_border_target=12.75,
                       y_left_border_target=-5.75,
                       y_right_border_target=5.75,
                       x_0=0, y_0=0, z_0=0, l=10):

    N = int((a2 + b2) / h2)
    M = int((a1 + b1) / h1)

    summ = 0

    coord_list = []

    for i in range(0, N):
        x = a1 + i * h2
        for j in range(0, M):
            y = a2 + j * h1

            logging.debug(f'Фи и Тета: {math.degrees(x):.5f}, {math.degrees(y):.5f}')
            if cond_enabled:

                s_1_podv = math.cos(y)
                s_2_podv = math.sin(y) * math.sin(x)
                s_3_podv = math.cos(y) * math.sin(x)
                logging.debug(f'Координаты вектора сигма в подвижной: {s_1_podv:.5f}, {s_2_podv:.5f}, {s_3_podv:.5f}')
                s_1_nepodv = math.cos(ksi) * s_1_podv - math.sin(ksi) * s_2_podv
                s_2_nepodv = math.sin(ksi) * s_1_podv + math.cos(ksi) * s_2_podv
                s_3_nepodv = s_3_podv
                logging.debug(f'Координаты вектора сигма в неподвижной: {s_1_nepodv:.5f}, {s_2_nepodv:.5f}, {s_3_nepodv:.5f}')
                if s_1_nepodv <= 0:
                    logging.debug(f"{Fore.RED}Сигма_1 отрицательная, пропускаем{Style.RESET_ALL}")
                    continue

                t = (l - x_0) / s_1_nepodv

                y_1 = y_0 + s_2_nepodv * t
                z_1 = z_0 + s_3_nepodv * t
                x_1 = l
                logging.debug(f'Координаты точки пересечения: {x_1:.3f}, {y_1:.3f}, {z_1:.3f}')
                if not ((z_lower_border_target <= z_1 <= z_higher_border_target) and (y_left_border_target <= y_1 <= y_right_border_target)):
                    logging.debug(f"{Fore.RED}Луч не пересекает поверхность{Style.RESET_ALL}")
                    coord_list.append([x_1, y_1, z_1, 0])
                    continue
                logging.debug(f"{Fore.GREEN}Луч пересекает поверхность{Style.RESET_ALL}")
                coord_list.append([x_1, y_1, z_1, 1])

            if (i > 0 and i < N and j > 0 and j < M):
                w = 1
            elif (i == 0 or i == M) and (j == 0 or j == N):
                w = 0.25
            else:
                w = 0.5

            summ += w * func(x, y)

    res = h1 * h2 * summ
    # / ((b1 - a1) * (b2 - a1))

    return res, coord_list


def test(x, y):
    return math.exp(math.sin(math.pi * x) * math.cos(math.pi * y)) + 1

if __name__ == "__main__":
    psi = 0
    n = 360
    print(f'{double_integr_trap(v_p_intrg, 0, math.pi/2, 0.1, 0, 2*math.pi, 0.1, 1, 0):.20f}')
