import logging
import math
import colorama
from colorama import Fore, Style
import threading
import concurrent.futures
import time


def v_p_intrg(x, y):
    return math.cos(y) * math.sin(y)


def double_integr_trap(
    func=v_p_intrg,
    a1=0,
    b1=math.pi / 2,
    h1=0.1,
    a2=0,
    b2=2 * math.pi,
    h2=0.1,
    cond_enabled=False,
    ksi=0,
    z_lower_border_target=-12.75,
    z_higher_border_target=12.75,
    y_left_border_target=-5.75,
    y_right_border_target=5.75,
    x_0=0,
    y_0=0,
    z_0=0,
    l=10,
):

    N = int((b2 - a2) / h2)
    M = int((b1 - a1) / h1)

    summ = 0

    coord_list = []
    for i in range(0, N + 1):
        x = a1 + i * h2
        for j in range(0, M + 1):
            y = a2 + j * h1

            logging.debug(f'Фи и Тета: {math.degrees(x):.5f}, {math.degrees(y):.5f}')
            if cond_enabled:

                s_1_podv = math.cos(y)
                s_2_podv = math.sin(y) * math.sin(x)
                s_3_podv = math.sin(y) * math.cos(x)
                logging.debug(f'Координаты вектора сигмаaa в подвижной: {s_1_podv:.5f}, {s_2_podv:.5f}, {s_3_podv:.5f}')
                s_1_nepodv = math.cos(ksi) * s_1_podv - math.sin(ksi) * s_2_podv
                s_2_nepodv = math.sin(ksi) * s_1_podv + math.cos(ksi) * s_2_podv
                s_3_nepodv = s_3_podv
                logging.debug(
                    f'Координаты вектора сигма в неподвижной: {s_1_nepodv:.5f}, {s_2_nepodv:.5f}, {s_3_nepodv:.5f}'
                )
                if s_1_nepodv <= 0:
                    logging.debug(f"{Fore.RED}Сигма_1 отрицательная, пропускаем{Style.RESET_ALL}")
                    continue

                t = (l - x_0) / s_1_nepodv

                y_1 = y_0 + s_2_nepodv * t
                z_1 = z_0 + s_3_nepodv * t
                x_1 = l
                logging.debug(f'Координаты точки пересечения: {x_1:.3f}, {y_1:.3f}, {z_1:.3f}')
                if not (
                    (z_lower_border_target <= z_1 <= z_higher_border_target)
                    and (y_left_border_target <= y_1 <= y_right_border_target)
                ):
                    logging.debug(f"{Fore.RED}Луч не пересекает поверхность{Style.RESET_ALL}")
                    coord_list.append([x_1, y_1, z_1, 0])
                    continue
                logging.debug(f"{Fore.GREEN}Луч пересекает поверхность{Style.RESET_ALL}")
                coord_list.append([x_1, y_1, z_1, 1])

            if i > 0 and i < N and j > 0 and j < M:
                w = 1
            elif (i == 0 or i == M) and (j == 0 or j == N):
                w = 0.25
            else:
                w = 0.5
            summ += w * func(x, y)

    # logging.debug(f"{summ}")
    res = h1 * h2 * summ
    # / ((b1 - a1) * (b2 - a1))

    return res, coord_list


def double_integr_trap_multithread(
    func=v_p_intrg,
    a1=0,
    b1=math.pi / 2,
    h1=0.1,
    a2=0,
    b2=2 * math.pi,
    h2=0.1,
    cond_enabled=False,
    ksi=0,
    k=1,
    thread_count=4,
    z_lower_border_target=-12.75,
    z_higher_border_target=12.75,
    y_left_border_target=-5.75,
    y_right_border_target=5.75,
    x_0=0,
    y_0=0,
    z_0=0,
    l=10,
):

    N = int((b2 - a2) / h2)
    M = int((b1 - a1) / h1)

    curr = 0
    end = N
    pack = int(N / thread_count)
    if N % thread_count:
        pack += 1

    results_array = []
    with concurrent.futures.ProcessPoolExecutor() as executor:
        futures = []
        while curr != end or curr != N:
            prev = curr
            curr += pack
            if curr > N:
                curr = N

            # print(curr)

            futures.append(
                executor.submit(
                    calc_for,
                    func,
                    a1,
                    b1,
                    h1,
                    a2,
                    b2,
                    h2,
                    cond_enabled,
                    ksi,
                    k,
                    z_lower_border_target,
                    z_higher_border_target,
                    y_left_border_target,
                    y_right_border_target,
                    x_0,
                    y_0,
                    z_0,
                    l,
                    prev,
                    curr,
                    N,
                    M,
                )
            )
            logging.debug("started thread")

        for future in concurrent.futures.as_completed(futures):
            results_array.append(future.result())

    # print(results_array)
    res = h1 * h2 * sum(results_array)
    # / ((b1 - a1) * (b2 - a1))

    return res, []


def calc_for(
    func=v_p_intrg,
    a1=0,
    b1=math.pi / 2,
    h1=0.1,
    a2=0,
    b2=2 * math.pi,
    h2=0.1,
    cond_enabled=False,
    ksi=0,
    k=1,
    z_lower_border_target=-12.75,
    z_higher_border_target=12.75,
    y_left_border_target=-5.75,
    y_right_border_target=5.75,
    x_0=0,
    y_0=0,
    z_0=0,
    l=10,
    prev=0,
    curr=0,
    N=0,
    M=0,
):

    summ = 0
    coord_list = []
    for i in range(prev, curr):
        x = a1 + i * h2
        for j in range(0, M):
            y = a2 + j * h1

            logging.debug(f'Фи и Тета: {math.degrees(x):.5f}, {math.degrees(y):.5f}')
            distance = 0

            if cond_enabled:
                s_1_podv = math.cos(y)
                s_2_podv = math.sin(y) * math.sin(x)
                s_3_podv = math.sin(y) * math.cos(x)
                logging.debug(f'Координаты вектора сигма в подвижной: {s_1_podv:.5f}, {s_2_podv:.5f}, {s_3_podv:.5f}')
                s_1_nepodv = math.cos(ksi) * s_1_podv - math.sin(ksi) * s_2_podv
                s_2_nepodv = math.sin(ksi) * s_1_podv + math.cos(ksi) * s_2_podv
                s_3_nepodv = s_3_podv
                logging.debug(
                    f'Координаты вектора сигма в неподвижной: {s_1_nepodv:.5f}, {s_2_nepodv:.5f}, {s_3_nepodv:.5f}'
                )
                if s_1_nepodv <= 0:
                    logging.debug(f"{Fore.RED}Сигма_1 отрицательная, пропускаем{Style.RESET_ALL}")
                    continue

                t = (l - x_0) / s_1_nepodv

                y_1 = y_0 + s_2_nepodv * t
                z_1 = z_0 + s_3_nepodv * t
                x_1 = l
                logging.debug(f'Координаты точки пересечения: {x_1:.3f}, {y_1:.3f}, {z_1:.3f}')
                if not (
                    (z_lower_border_target <= z_1 <= z_higher_border_target)
                    and (y_left_border_target <= y_1 <= y_right_border_target)
                ):
                    logging.debug(f"{Fore.RED}Луч не пересекает поверхность{Style.RESET_ALL}")
                    coord_list.append([x_1, y_1, z_1, 0])
                    continue
                logging.debug(f"{Fore.GREEN}Луч пересекает поверхность{Style.RESET_ALL}")
                coord_list.append([x_1, y_1, z_1, 1])

                distance = math.sqrt((x_1 - x_0) ** 2 + (y_1 - y_0) ** 2 + (z_1 - z_0) ** 2)

            if i > 0 and i < N and j > 0 and j < M:
                w = 1
            elif (i == 0 or i == M) and (j == 0 or j == N):
                w = 0.25
            else:
                w = 0.5

            logging.debug(f"{w * func(x, y)}")
            # print(distance)
            # print(k)
            # print(-k * distance)
            # print(math.exp(-k * distance))
            summ += w * func(x, y) * math.exp(-k * distance)
            # summ += (w * func(x, y)) / ((1) ** 2)

    return summ


def test(x, y):
    return math.exp(math.sin(y) * math.cos(y))


if __name__ == "__main__":
    psi = 0
    n = 360

    start = time.time()
    # print(f'{double_integr_trap_multithread(test, 0, math.pi, 0.0001, 0, math.pi, 0.001, False, 0, thread_count=8):.20f}')
    end = time.time()
    print(end - start)

    start = time.time()
    print(f'{double_integr_trap(test, 0, math.pi, 0.0001, 0, math.pi, 0.001, False, 0)[0]:.20f}')
    end = time.time()
    print(end - start)
