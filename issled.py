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
    mishen: Mishen,
    ksi,
    seconds=60,
    k=0,
    nx=100,
    ny=100,
    time_step=0.15,
    thread_count=16,
):
    drum_with_podlozkda_copy = drum_with_podlozkda.copy()
    drum_with_podlozkda_copy.make_custom_holder(holder_angle=0, point_angle=ksi)
    ress = [["omega_b", "omega_o", "ksi", "seconds", "k", "nx", "ny", "time_step", "thread_count", "time", "d", "mdist", "mshir", "mvis"]]
    start = time.time()
    d = one_dot(
        drum_with_podlozkda_copy, mishen, seconds=seconds, k=k, nx=nx, ny=ny, time_step=time_step, thread_count=thread_count
    )

    end = time.time()
    elapsed_time = end - start
    return [
        drum_with_podlozkda_copy.rpm,
        drum_with_podlozkda_copy.holders_rpm,
        ksi,
        seconds,
        k,
        nx,
        ny,
        time_step,
        thread_count,
        elapsed_time,
        d,
        mishen.x,
        mishen.z_higher_border_target * 2,
        mishen.y_right_border_target * 2
    ]


def issled_neravnomernosti(omega_b=1, omega_o=2, k=0, mishen=Mishen(30, -25.5 / 2, 25.5 / 2, -11.5 / 2, 11.5 / 2), drum_with_podlozkda=Drum_with_podlozkda(rad=10, rpm=1, holders_rad=1, holders_rpm=2)):
    seconds = 60
    nx = ny = 100
    time_step = 0.15
    ress = [["omega_b", "omega_o", "ksi", "seconds", "k", "nx", "ny", "time_step", "thread_count", "time", "d"]]
    res = issled_one_dot_ksi(
        drum_with_podlozkda, mishen, ksi=0, seconds=seconds, k=k, nx=nx, ny=ny, time_step=time_step, thread_count=16
    )
    ress.append(res)
    res = issled_one_dot_ksi(
        drum_with_podlozkda, mishen, ksi=45, seconds=seconds, k=k, nx=nx, ny=ny, time_step=time_step, thread_count=16
    )
    ress.append(res)
    res = issled_one_dot_ksi(
        drum_with_podlozkda, mishen, ksi=90, seconds=seconds, k=k, nx=nx, ny=ny, time_step=time_step, thread_count=16
    )
    ress.append(res)
    res = issled_one_dot_ksi(
        drum_with_podlozkda, mishen, ksi=135, seconds=seconds, k=k, nx=nx, ny=ny, time_step=time_step, thread_count=16
    )
    ress.append(res)
    res = issled_one_dot_ksi(
        drum_with_podlozkda, mishen, ksi=180, seconds=seconds, k=k, nx=nx, ny=ny, time_step=time_step, thread_count=16
    )
    ress.append(res)
    res = issled_one_dot_ksi(
        drum_with_podlozkda, mishen, ksi=225, seconds=seconds, k=k, nx=nx, ny=ny, time_step=time_step, thread_count=16
    )
    ress.append(res)
    res = issled_one_dot_ksi(
        drum_with_podlozkda, mishen, ksi=270, seconds=seconds, k=k, nx=nx, ny=ny, time_step=time_step, thread_count=16
    )
    ress.append(res)
    res = issled_one_dot_ksi(
        drum_with_podlozkda, mishen, ksi=315, seconds=seconds, k=k, nx=nx, ny=ny, time_step=0.15, thread_count=16
    )

    file = open(
        f'table_neravnomernost_ob{drum_with_podlozkda.rpm}_oo{drum_with_podlozkda.holders_rpm}_m{seconds}_k{k}_mx{mishen.x}_mvis{mishen.z_higher_border_target * 2}_mshir{mishen.y_right_border_target * 2}_rb{drum_with_podlozkda.rad}_ro{drum_with_podlozkda.holders_rad}.csv', 'a'
    )
    writer = csv.writer(file)
    for elem in ress:
        writer.writerow(elem)
    file.close()

def issled_step_po_rasstoyaniy():
    for distance in range(12, 14):
        mishen = Mishen(distance, -25.5 / 2, 25.5 / 2, -11.5 / 2, 11.5 / 2)
        issled_neravnomernosti(mishen=mishen)

def issled_step_po_size():
    for visota in np.arange(5, 50, 0.5):
        for shirina in np.arange(5, 50, 0.5):
            mishen = Mishen(30, -visota / 2, visota / 2, -shirina / 2, shirina / 2)
            issled_neravnomernosti(mishen=mishen)


def issled_step_po_rad():
    for rad_o in np.arange(1, 50, 2):
        for rad_b in np.arange(rad_o, 50, 4):
            drum_with_podlozkda = Drum_with_podlozkda(rad=rad_b, rpm=1, holders_rad=rad_o, holders_rpm=2)
            issled_neravnomernosti(drum_with_podlozkda=drum_with_podlozkda)


def issled_k():
    for e in np.arange(0, 1.05, 0.05):
        if e == 0:
            k = 0
        else:
            k = -math.log(e) / 19
        # print(k)
        issled_neravnomernosti(k=k)


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


def issled_time(omega_b=1, omega_o=2, seconds=1, ksi=0, k=0, nx=100, ny=100, time_step=0.15, thread_count=16, cond_enabled=True):
    drum_with_podlozkda = Drum_with_podlozkda(rad=10, rpm=omega_b, holders_rad=1, holders_rpm=omega_o)
    drum_with_podlozkda.make_custom_holder(holder_angle=0, point_angle=0)
    mishen = Mishen(30, -25.5 / 2, 25.5 / 2, -11.5 / 2, 11.5 / 2)
    start = time.time()
    res = one_dot(drum_with_podlozkda, mishen, seconds=seconds, k=k, nx=nx, ny=ny, time_step=time_step, cond_enabled=cond_enabled)
    end = time.time()
    print(end - start)
    return [omega_b, omega_o, seconds, ksi, k, nx, nx, time_step, thread_count, end - start, res, nx * ny]


def issled_time_hx_hy():
    file = open('table_time.csv', 'a')
    writer = csv.writer(file)
    ress = [["omega_b", "omega_o", "seconds", "ksi", "k", "h1", "h2", "time_step", "thread_count", "time", "res"]]
    res = issled_time(omega_b=1, omega_o=2, seconds=60, ksi=0, k=0, nx=100, ny=100, time_step=0.01, thread_count=16)
    ress.append(res)
    res = issled_time(omega_b=1, omega_o=2, seconds=60, ksi=0, k=0, nx=100, ny=100, time_step=0.05, thread_count=16)
    ress.append(res)
    res = issled_time(omega_b=1, omega_o=2, seconds=60, ksi=0, k=0, nx=100, ny=100, time_step=0.10, thread_count=16)
    ress.append(res)
    res = issled_time(omega_b=1, omega_o=2, seconds=60, ksi=0, k=0, nx=100, ny=100, time_step=0.15, thread_count=16)
    ress.append(res)
    res = issled_time(omega_b=1, omega_o=2, seconds=60, ksi=0, k=0, nx=100, ny=100, time_step=0.30, thread_count=16)
    ress.append(res)
    res = issled_time(omega_b=1, omega_o=2, seconds=60, ksi=0, k=0, nx=100, ny=100, time_step=0.20, thread_count=16)
    ress.append(res)
    res = issled_time(omega_b=1, omega_o=2, seconds=60, ksi=0, k=0, nx=100, ny=100, time_step=0.50, thread_count=16)
    ress.append(res)
    res = issled_time(omega_b=1, omega_o=2, seconds=60, ksi=0, k=0, nx=100, ny=100, time_step=0.60, thread_count=16)
    ress.append(res)
    res = issled_time(omega_b=1, omega_o=2, seconds=60, ksi=0, k=0, nx=100, ny=100, time_step=1, thread_count=16)
    ress.append(res)
    res = issled_time(omega_b=1, omega_o=2, seconds=60, ksi=0, k=0, nx=100, ny=100, time_step=2, thread_count=16)
    ress.append(res)

    for elem in ress:
        writer.writerow(elem)
    file.close()


def issled_time_method_step(cond_enabled=True, nx=100, ny=100):

    ress = [["omega_b", "omega_o", "seconds", "ksi", "k", "h1", "h2", "time_step", "thread_count", "time", "res"]]
    res = issled_time(omega_b=1, omega_o=2, seconds=60, ksi=0, k=0, nx=nx, ny=ny, time_step=0.01, thread_count=16, cond_enabled=cond_enabled)
    ress.append(res)
    res = issled_time(omega_b=1, omega_o=2, seconds=60, ksi=0, k=0, nx=nx, ny=ny, time_step=0.05, thread_count=16)
    ress.append(res)
    res = issled_time(omega_b=1, omega_o=2, seconds=60, ksi=0, k=0, nx=nx, ny=ny, time_step=0.10, thread_count=16)
    ress.append(res)
    res = issled_time(omega_b=1, omega_o=2, seconds=60, ksi=0, k=0, nx=nx, ny=ny, time_step=0.15, thread_count=16)
    ress.append(res)
    res = issled_time(omega_b=1, omega_o=2, seconds=60, ksi=0, k=0, nx=nx, ny=ny, time_step=0.30, thread_count=16)
    ress.append(res)
    res = issled_time(omega_b=1, omega_o=2, seconds=60, ksi=0, k=0, nx=nx, ny=ny, time_step=0.20, thread_count=16)
    ress.append(res)
    res = issled_time(omega_b=1, omega_o=2, seconds=60, ksi=0, k=0, nx=nx, ny=ny, time_step=0.50, thread_count=16)
    ress.append(res)
    res = issled_time(omega_b=1, omega_o=2, seconds=60, ksi=0, k=0, nx=nx, ny=ny, time_step=0.60, thread_count=16)
    ress.append(res)
    res = issled_time(omega_b=1, omega_o=2, seconds=60, ksi=0, k=0, nx=nx, ny=ny, time_step=1, thread_count=16)
    ress.append(res)
    res = issled_time(omega_b=1, omega_o=2, seconds=60, ksi=0, k=0, nx=nx, ny=ny, time_step=2, thread_count=16)
    ress.append(res)

    file = open(f'table_time_{nx}_{cond_enabled}.csv', 'a')
    writer = csv.writer(file)
    for elem in ress:
        writer.writerow(elem)
    file.close()


def issled_time_method_cond(cond_enabled=True):
    ress = [["omega_b", "omega_o", "seconds", "ksi", "k", "h1", "h2", "time_step", "thread_count", "time", "res", "points"]]
    points = 2
    while points <= 2 ** 10:
        res = issled_time(omega_b=1, omega_o=2, seconds=60, ksi=0, k=0, nx=points, ny=points, time_step=2, thread_count=16, cond_enabled=cond_enabled)
        points = points * 2
        ress.append(res)

    file = open(f'table_time_cond_{cond_enabled}.csv', 'a')
    writer = csv.writer(file)
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
    res = midpoint_double_multithread(func=int_func4, a1=a1, b1=b1, a2=a2, b2=b2, ny=ny, nx=nx, thread_count=1)
    end = time.time()

    acc = (res - real_val) / real_val

    return [res, acc, end - start, nx, ny]


def issled_integr_diff_nx_ny(func, a1, b1, a2, b2, real_val):
    points = 2
    usred = 0
    while points * points <= 4194304:
        usred = 0
        for k in range(0, 10):
            res = issled_integr(func, a1, b1, a2, b2, points, points, real_val)
            usred = usred + res[2]
        usred = usred / 10
        res[2] = usred
        res.append(points * points)
        points = points + 100
        print(res)

    # res = issled_integr(func, a1, b1, a2, b2, 1024, 1024, real_val)
    # res.append(1024 * 1024)
    # print(res)

if __name__ == "__main__":
    res = issled_integr_diff_nx_ny(int_func3, 0, math.pi / 2, 0, math.pi / 2, math.pi / 4)
    # tart = time.time()
    # res,_ = midpoint_double_viz_multithread(func=int_func4, a1=0, b1=math.pi * 2, a2=0, b2=math.pi / 2, ny=100, nx=100)
    # end = time.time()
    # print(end - tart)
    # tart = time.time()
    # res = midpoint_double_multithread(func=int_func4, a1=0, b1=math.pi * 2, a2=0, b2=math.pi / 2, ny=100, nx=100)
    # end = time.time()
    # print(end - tart)

    # issled_k()
    # issled_step_po_rasstoyaniy()
    # issled_step_po_rad()
    # drum_with_podlozkda = Drum_with_podlozkda(rad=10, rpm=1, holders_rad=1, holders_rpm=2)
    # mishen = Mishen(300, -25.5 / 2, 25.5 / 2, -11.5 / 2, 11.5 / 2)
    # issled_neravnomernosti(mishen=mishen, drum_with_podlozkda=drum_with_podlozkda)

    # drum_with_podlozkda = Drum_with_podlozkda(rad=10, rpm=15, holders_rad=1, holders_rpm=23)
    # mishen = Mishen(300, -400 / 2, 400 / 2, -11.5 / 2, 11.5 / 2)
    # issled_neravnomernosti(mishen=mishen, drum_with_podlozkda=drum_with_podlozkda)

    # drum_with_podlozkda = Drum_with_podlozkda(rad=10, rpm=15, holders_rad=1, holders_rpm=23)
    # mishen = Mishen(300, -20 / 2, 20 / 2, -11.5 / 2, 11.5 / 2)
    # issled_neravnomernosti(mishen=mishen, drum_with_podlozkda=drum_with_podlozkda)


    # # issled_neravnomernosti(omega_b=15, omega_o=23)
    # issled_time_method_cond(cond_enabled=True)
    # issled_time_method_cond(cond_enabled=False)
    # drum_with_podlozkda = Drum_with_podlozkda(rad=10, rpm=1, holders_rad=1, holders_rpm=2)
    # drum_with_podlozkda.make_custom_holder(holder_angle=0, point_angle=0)
    # mishen = Mishen(30, -25.5 / 2, 25.5 / 2, -11.5 / 2, 11.5 / 2)
    # issled_one_dot_ksi(drum_with_podlozkda, mishen, ksi=0, seconds=60, k=0, nx=2048, ny=2048, time_step=0.15, thread_count=16)
