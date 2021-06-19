import csv
import math
import time
import concurrent.futures
import numpy as np

from main import one_dot
from model import Drum_with_podlozkda, Mishen
from integr import midpoint_double_multithread, midpoint_double1, midpoint_double_viz_multithread


def issled_one_dot_ksi(
    drum_with_podlozkda: Drum_with_podlozkda,
    mishen,
    ksi,
    seconds=60,
    k=0,
    nx=100,
    ny=100,
    time_step=0.15,
    thread_count=16,
):
    drum_with_podlozkda.make_custom_holder(holder_angle=0, point_angle=ksi)
    ress = [["omega_b", "omega_o", "ksi", "seconds", "k", "nx", "ny", "time_step", "thread_count", "time", "d"]]
    start = time.time()
    d = one_dot(
        drum_with_podlozkda, mishen, seconds=seconds, k=k, nx=nx, ny=ny, time_step=time_step, thread_count=thread_count
    )

    end = time.time()
    elapsed_time = end - start
    return [
        drum_with_podlozkda.rpm,
        drum_with_podlozkda.holders_rpm,
        ksi,
        seconds,
        k,
        nx,
        ny,
        time_step,
        thread_count,
        elapsed_time,
        d,
    ]


def issled_neravnomernosti(omega_b=1, omega_o=2, k=0):
    seconds = 60
    nx = ny = 100
    drum_with_podlozkda = Drum_with_podlozkda(rad=10, rpm=omega_b, holders_rad=1, holders_rpm=omega_o)
    mishen = Mishen(30, -25.5 / 2, 25.5 / 2, -11.5 / 2, 11.5 / 2)
    ress = [["omega_b", "omega_o", "ksi", "seconds", "k", "nx", "ny", "time_step", "thread_count", "time", "d"]]
    res = issled_one_dot_ksi(
        drum_with_podlozkda, mishen, ksi=0, seconds=seconds, k=k, nx=nx, ny=ny, time_step=0.15, thread_count=16
    )
    ress.append(res)
    res = issled_one_dot_ksi(
        drum_with_podlozkda, mishen, ksi=45, seconds=seconds, k=k, nx=nx, ny=ny, time_step=0.15, thread_count=16
    )
    ress.append(res)
    res = issled_one_dot_ksi(
        drum_with_podlozkda, mishen, ksi=90, seconds=seconds, k=k, nx=nx, ny=ny, time_step=0.15, thread_count=16
    )
    ress.append(res)
    res = issled_one_dot_ksi(
        drum_with_podlozkda, mishen, ksi=135, seconds=seconds, k=k, nx=nx, ny=ny, time_step=0.15, thread_count=16
    )
    ress.append(res)
    res = issled_one_dot_ksi(
        drum_with_podlozkda, mishen, ksi=180, seconds=seconds, k=k, nx=nx, ny=ny, time_step=0.15, thread_count=16
    )
    ress.append(res)
    res = issled_one_dot_ksi(
        drum_with_podlozkda, mishen, ksi=225, seconds=seconds, k=k, nx=nx, ny=ny, time_step=0.15, thread_count=16
    )
    ress.append(res)
    res = issled_one_dot_ksi(
        drum_with_podlozkda, mishen, ksi=270, seconds=seconds, k=k, nx=nx, ny=ny, time_step=0.15, thread_count=16
    )
    ress.append(res)
    res = issled_one_dot_ksi(
        drum_with_podlozkda, mishen, ksi=315, seconds=seconds, k=k, nx=nx, ny=ny, time_step=0.15, thread_count=16
    )

    file = open(
        f'table_neravnomernost_ob{drum_with_podlozkda.rpm}_oo{drum_with_podlozkda.holders_rpm}_m{seconds}_k{k}.csv', 'a'
    )
    writer = csv.writer(file)
    for elem in ress:
        writer.writerow(elem)
    file.close()


def issled_k():

    for e in np.arange(0.05, 1.05, 0.05):
        k = math.log(e) / 19
        # print(e, k)
        # issled_neravnomernosti(k=k)


def issled_one_dot(drum_with_podlozkda, mishen, seconds=60, k=0, nx=100, ny=100):

    drum_with_podlozkda = Drum_with_podlozkda(rad=10, rpm=1, holders_rad=1, holders_rpm=2)
    drum_with_podlozkda.make_custom_holder(holder_angle=0, point_angle=0)
    mishen = Mishen(30, -25.5 / 2, 25.5 / 2, -11.5 / 2, 11.5 / 2)

    file = open(f'table_ob{drum_with_podlozkda.rpm}_oo{drum_with_podlozkda.holders_rpm}_m{seconds}_k{k}.csv', 'w')
    writer = csv.writer(file)

    writer.writerow(
        [f"omega_b={drum_with_podlozkda.rpm}", f"omega_o={drum_with_podlozkda.holders_rpm}", f"seconds={seconds}"]
    )
    writer.writerow(["angle", "d"])
    d = one_dot(drum_with_podlozkda, mishen, seconds=seconds, k=k, nx=nx, ny=ny)
    writer.writerow(["0", f"{d}"])
    d = one_dot(drum_with_podlozkda, mishen, seconds=seconds, k=k, nx=nx, ny=ny)
    writer.writerow(["45", f"{d}"])
    d = one_dot(drum_with_podlozkda, mishen, seconds=seconds, k=k, nx=nx, ny=ny)
    writer.writerow(["90", f"{d}"])
    d = one_dot(drum_with_podlozkda, mishen, seconds=seconds, k=k, nx=nx, ny=ny)
    writer.writerow(["135", f"{d}"])
    d = one_dot(drum_with_podlozkda, mishen, seconds=seconds, k=k, nx=nx, ny=ny)
    writer.writerow(["180", f"{d}"])
    d = one_dot(drum_with_podlozkda, mishen, seconds=seconds, k=k, nx=nx, ny=ny)
    writer.writerow(["225", f"{d}"])
    d = one_dot(drum_with_podlozkda, mishen, seconds=seconds, k=k, nx=nx, ny=ny)
    writer.writerow(["270", f"{d}"])
    d = one_dot(drum_with_podlozkda, mishen, seconds=seconds, k=k, nx=nx, ny=ny)
    writer.writerow(["315", f"{d}"])
    file.close()


def issled_one_dot_omega():
    counter = 0
    with concurrent.futures.ProcessPoolExecutor() as executor:
        futures = []
        for i in range(1, 12):
            for j in range(1, 12):
                if i == j and i != 1:
                    continue
                futures.append(executor.submit(issled_neravnomernosti, omega_b=i, omega_o=j))

        for future in concurrent.futures.as_completed(futures):
            counter += 1
            print(counter)

    print(counter)


def issled_time(omega_b=1, omega_o=2, seconds=1, ksi=0, k=0, hx=0.01, hy=0.01, time_step=0.15, thread_count=16):
    start = time.time()
    res = one_dot(
        omega_b=omega_b,
        omega_o=omega_o,
        seconds=seconds,
        ksi=ksi,
        k=k,
        h1=hx,
        h2=hy,
        time_step=time_step,
        thread_count=thread_count,
    )
    end = time.time()
    print(end - start)
    return [omega_b, omega_o, seconds, ksi, k, hx, hy, time_step, thread_count, end - start, res]


def issled_time_hx_hy():
    file = open('table_time.csv', 'a')
    writer = csv.writer(file)
    ress = [["omega_b", "omega_o", "seconds", "ksi", "k", "h1", "h2", "time_step", "thread_count", "time", "res"]]
    res = issled_time(omega_b=1, omega_o=2, seconds=60, ksi=0, k=0, hx=1000, hy=1000, time_step=0.01, thread_count=16)
    ress.append(res)
    res = issled_time(omega_b=1, omega_o=2, seconds=60, ksi=0, k=0, hx=1000, hy=1000, time_step=0.05, thread_count=16)
    ress.append(res)
    res = issled_time(omega_b=1, omega_o=2, seconds=60, ksi=0, k=0, hx=1000, hy=1000, time_step=0.10, thread_count=16)
    ress.append(res)
    res = issled_time(omega_b=1, omega_o=2, seconds=60, ksi=0, k=0, hx=1000, hy=1000, time_step=0.15, thread_count=16)
    ress.append(res)
    res = issled_time(omega_b=1, omega_o=2, seconds=60, ksi=0, k=0, hx=1000, hy=1000, time_step=0.30, thread_count=16)
    ress.append(res)
    res = issled_time(omega_b=1, omega_o=2, seconds=60, ksi=0, k=0, hx=1000, hy=1000, time_step=0.20, thread_count=16)
    ress.append(res)
    res = issled_time(omega_b=1, omega_o=2, seconds=60, ksi=0, k=0, hx=1000, hy=1000, time_step=0.50, thread_count=16)
    ress.append(res)
    res = issled_time(omega_b=1, omega_o=2, seconds=60, ksi=0, k=0, hx=1000, hy=1000, time_step=0.60, thread_count=16)
    ress.append(res)
    res = issled_time(omega_b=1, omega_o=2, seconds=60, ksi=0, k=0, hx=1000, hy=1000, time_step=1, thread_count=16)
    ress.append(res)
    res = issled_time(omega_b=1, omega_o=2, seconds=60, ksi=0, k=0, hx=1000, hy=1000, time_step=2, thread_count=16)
    ress.append(res)

    for elem in ress:
        writer.writerow(elem)
    file.close()


def issled_time_multiple():
    file = open('table_time.csv', 'a')

    writer = csv.writer(file)
    ress = [["omega_b", "omega_o", "seconds", "ksi", "k", "h1", "h2", "time_step", "thread_count", "time", "res"]]
    res = issled_time(omega_b=1, omega_o=2, seconds=60, ksi=0, k=0, hx=1000, hy=1000, time_step=0.01, thread_count=16)
    ress.append(res)
    res = issled_time(omega_b=1, omega_o=2, seconds=60, ksi=0, k=0, hx=1000, hy=1000, time_step=0.05, thread_count=16)
    ress.append(res)
    res = issled_time(omega_b=1, omega_o=2, seconds=60, ksi=0, k=0, hx=1000, hy=1000, time_step=0.10, thread_count=16)
    ress.append(res)
    res = issled_time(omega_b=1, omega_o=2, seconds=60, ksi=0, k=0, hx=1000, hy=1000, time_step=0.15, thread_count=16)
    ress.append(res)
    res = issled_time(omega_b=1, omega_o=2, seconds=60, ksi=0, k=0, hx=1000, hy=1000, time_step=0.30, thread_count=16)
    ress.append(res)
    res = issled_time(omega_b=1, omega_o=2, seconds=60, ksi=0, k=0, hx=1000, hy=1000, time_step=0.20, thread_count=16)
    ress.append(res)
    res = issled_time(omega_b=1, omega_o=2, seconds=60, ksi=0, k=0, hx=1000, hy=1000, time_step=0.50, thread_count=16)
    ress.append(res)
    res = issled_time(omega_b=1, omega_o=2, seconds=60, ksi=0, k=0, hx=1000, hy=1000, time_step=0.60, thread_count=16)
    ress.append(res)
    res = issled_time(omega_b=1, omega_o=2, seconds=60, ksi=0, k=0, hx=1000, hy=1000, time_step=1, thread_count=16)
    ress.append(res)
    res = issled_time(omega_b=1, omega_o=2, seconds=60, ksi=0, k=0, hx=1000, hy=1000, time_step=2, thread_count=16)
    ress.append(res)

    for elem in ress:
        writer.writerow(elem)
    file.close()


# 2/3
def int_func1(x, y):
    return x * y ** 2


def int_func2(x, y):
    return math.cos(y) * x ** 2 + 1


def int_func3(x, y):
    return math.cos(x + y)


def int_func4(x, y):
    return math.cos(y) * math.sin(y)


def issled_integr(func, a1, b1, a2, b2, nx, ny, real_val):
    start = time.time()
    res = midpoint_double_multithread(func=int_func4, a1=a1, b1=b1, a2=a2, b2=b2, ny=ny, nx=nx)
    end = time.time()

    acc = (res - real_val) / real_val

    return [res, acc, end - start, nx, ny]


def issled_integr_diff_nx_ny(func, a1, b1, a2, b2, real_val):
    points = 2
    while points <= 2 ** 20:
        res = issled_integr(func, a1, b1, a2, b2, points, points, real_val)
        res.append(points * points)
        points = points * 2
        print(res)


if __name__ == "__main__":
    # res = issled_integr_diff_nx_ny(int_func3, 0, math.pi / 2, 0, math.pi / 2, math.pi / 4)
    # tart = time.time()
    # res,_ = midpoint_double_viz_multithread(func=int_func4, a1=0, b1=math.pi * 2, a2=0, b2=math.pi / 2, ny=100, nx=100)
    # end = time.time()
    # print(end - tart)
    # tart = time.time()
    # res = midpoint_double_multithread(func=int_func4, a1=0, b1=math.pi * 2, a2=0, b2=math.pi / 2, ny=100, nx=100)
    # end = time.time()
    # print(end - tart)

    issled_k()
    # drum_with_podlozkda = Drum_with_podlozkda(rad=10, rpm=1, holders_rad=1, holders_rpm=2)
    # drum_with_podlozkda.make_custom_holder(holder_angle=0, point_angle=0)
    # mishen = Mishen(30, -25.5 / 2, 25.5 / 2, -11.5 / 2, 11.5 / 2)
    # issled_one_dot_ksi(drum_with_podlozkda, mishen, ksi=0, seconds=60, k=0, nx=2048, ny=2048, time_step=0.15, thread_count=16)
