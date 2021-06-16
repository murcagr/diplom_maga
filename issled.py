import csv
import time
import concurrent.futures

from main import one_dot
from model import Drum_with_podlozkda, Mishen


def issled_one_dot_ksi(drum_with_podlozkda: Drum_with_podlozkda, mishen, ksi, minutes=1, k=0, nx=100, ny=100, time_step=0.15, thread_count=16):
    drum_with_podlozkda.make_custom_holder(holder_angle=0, point_angle=ksi)
    ress = [["omega_b", "omega_o", "ksi", "minutes", "k", "nx", "ny", "time_step", "thread_count", "time", "d"]]
    start = time.time()
    d = one_dot(drum_with_podlozkda, mishen, minutes=minutes, k=k, nx=nx, ny=ny, time_step=time_step, thread_count=thread_count)
    end = time.time()
    elapsed_time = end - start
    return [drum_with_podlozkda.rpm, drum_with_podlozkda.holders_rpm, ksi, minutes, k, nx, ny, time_step, thread_count, elapsed_time, d]

def issled_neravnomernosti(omega_b=1, omega_o=2):
    minutes = 1
    k = 0
    nx = ny = 10
    drum_with_podlozkda = Drum_with_podlozkda(rad=10, rpm=omega_b, holders_rad=1, holders_rpm=omega_o)
    drum_with_podlozkda.make_custom_holder(holder_angle=0, point_angle=0)
    mishen = Mishen(30, -25.5 / 2, 25.5 / 2, -11.5 / 2, 11.5 / 2)
    ress = [["omega_b", "omega_o", "ksi", "minutes", "k", "nx", "ny", "time_step", "thread_count", "time", "d"]]
    res = issled_one_dot_ksi(drum_with_podlozkda, mishen, ksi=0, minutes=minutes, k=k, nx=nx, ny=ny, time_step=0.15, thread_count=16)
    ress.append(res)
    res = issled_one_dot_ksi(drum_with_podlozkda, mishen, ksi=45, minutes=minutes, k=k, nx=nx, ny=ny, time_step=0.15, thread_count=16)
    ress.append(res)
    res = issled_one_dot_ksi(drum_with_podlozkda, mishen, ksi=90, minutes=minutes, k=k, nx=nx, ny=ny, time_step=0.15, thread_count=16)
    ress.append(res)
    res = issled_one_dot_ksi(drum_with_podlozkda, mishen, ksi=135, minutes=minutes, k=k, nx=nx, ny=ny, time_step=0.15, thread_count=16)
    ress.append(res)
    res = issled_one_dot_ksi(drum_with_podlozkda, mishen, ksi=180, minutes=minutes, k=k, nx=nx, ny=ny, time_step=0.15, thread_count=16)
    ress.append(res)
    res = issled_one_dot_ksi(drum_with_podlozkda, mishen, ksi=225, minutes=minutes, k=k, nx=nx, ny=ny, time_step=0.15, thread_count=16)
    ress.append(res)
    res = issled_one_dot_ksi(drum_with_podlozkda, mishen, ksi=270, minutes=minutes, k=k, nx=nx, ny=ny, time_step=0.15, thread_count=16)
    ress.append(res)
    res = issled_one_dot_ksi(drum_with_podlozkda, mishen, ksi=315, minutes=minutes, k=k, nx=nx, ny=ny, time_step=0.15, thread_count=16)

    file = open(f'table_neravnomernost_ob{drum_with_podlozkda.rpm}_oo{drum_with_podlozkda.holders_rpm}_m{minutes}_k{k}.csv', 'a')
    writer = csv.writer(file)
    for elem in ress:
        writer.writerow(elem)
    file.close()

def issled_one_dot(drum_with_podlozkda, mishen, minutes=1, k=0, nx=100, ny=100):

    drum_with_podlozkda = Drum_with_podlozkda(rad=10, rpm=1, holders_rad=1, holders_rpm=2)
    drum_with_podlozkda.make_custom_holder(holder_angle=0, point_angle=0)
    mishen = Mishen(30, -25.5 / 2, 25.5 / 2, -11.5 / 2, 11.5 / 2)

    file = open(f'table_ob{drum_with_podlozkda.rpm}_oo{drum_with_podlozkda.holders_rpm}_m{minutes}_k{k}.csv', 'w')
    writer = csv.writer(file)

    writer.writerow([f"omega_b={drum_with_podlozkda.rpm}", f"omega_o={drum_with_podlozkda.holders_rpm}", f"minutes={minutes}"])
    writer.writerow(["angle", "d"])
    d = one_dot(drum_with_podlozkda, mishen, minutes=minutes, k=k, nx=nx, ny=ny)
    writer.writerow(["0", f"{d}"])
    d = one_dot(drum_with_podlozkda, mishen, minutes=minutes, k=k, nx=nx, ny=ny)
    writer.writerow(["45", f"{d}"])
    d = one_dot(drum_with_podlozkda, mishen, minutes=minutes, k=k, nx=nx, ny=ny)
    writer.writerow(["90", f"{d}"])
    d = one_dot(drum_with_podlozkda, mishen, minutes=minutes, k=k, nx=nx, ny=ny)
    writer.writerow(["135", f"{d}"])
    d = one_dot(drum_with_podlozkda, mishen, minutes=minutes, k=k, nx=nx, ny=ny)
    writer.writerow(["180", f"{d}"])
    d = one_dot(drum_with_podlozkda, mishen, minutes=minutes, k=k, nx=nx, ny=ny)
    writer.writerow(["225", f"{d}"])
    d = one_dot(drum_with_podlozkda, mishen, minutes=minutes, k=k, nx=nx, ny=ny)
    writer.writerow(["270", f"{d}"])
    d = one_dot(drum_with_podlozkda, mishen, minutes=minutes, k=k, nx=nx, ny=ny)
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


def issled_time(omega_b=1, omega_o=2, minutes=1, ksi=0, k=0, hx=0.01, hy=0.01, time_step=0.15, thread_count=16):
    start = time.time()
    res = one_dot(omega_b=omega_b, omega_o=omega_o, minutes=minutes, ksi=ksi, k=k, h1=hx, h2=hy, time_step=time_step, thread_count=thread_count)
    end = time.time()
    print(end - start)
    return [omega_b, omega_o, minutes, ksi, k, hx, hy, time_step, thread_count, end - start, res]

def issled_time_hx_hy():
    file = open('table_time.csv', 'a')
    writer = csv.writer(file)
    ress = [["omega_b", "omega_o", "minutes", "ksi", "k", "h1", "h2", "time_step", "thread_count", "time", "res"]]
    res = issled_time(omega_b=1, omega_o=2, minutes=1, ksi=0, k=0, hx=1000, hy=1000, time_step=0.01, thread_count=16)
    ress.append(res)
    res = issled_time(omega_b=1, omega_o=2, minutes=1, ksi=0, k=0, hx=1000, hy=1000, time_step=0.05, thread_count=16)
    ress.append(res)
    res = issled_time(omega_b=1, omega_o=2, minutes=1, ksi=0, k=0, hx=1000, hy=1000, time_step=0.10, thread_count=16)
    ress.append(res)
    res = issled_time(omega_b=1, omega_o=2, minutes=1, ksi=0, k=0, hx=1000, hy=1000, time_step=0.15, thread_count=16)
    ress.append(res)
    res = issled_time(omega_b=1, omega_o=2, minutes=1, ksi=0, k=0, hx=1000, hy=1000, time_step=0.30, thread_count=16)
    ress.append(res)
    res = issled_time(omega_b=1, omega_o=2, minutes=1, ksi=0, k=0, hx=1000, hy=1000, time_step=0.20, thread_count=16)
    ress.append(res)
    res = issled_time(omega_b=1, omega_o=2, minutes=1, ksi=0, k=0, hx=1000, hy=1000, time_step=0.50, thread_count=16)
    ress.append(res)
    res = issled_time(omega_b=1, omega_o=2, minutes=1, ksi=0, k=0, hx=1000, hy=1000, time_step=0.60, thread_count=16)
    ress.append(res)
    res = issled_time(omega_b=1, omega_o=2, minutes=1, ksi=0, k=0, hx=1000, hy=1000, time_step=1, thread_count=16)
    ress.append(res)
    res = issled_time(omega_b=1, omega_o=2, minutes=1, ksi=0, k=0, hx=1000, hy=1000, time_step=2, thread_count=16)
    ress.append(res)

    for elem in ress:
        writer.writerow(elem)
    file.close()

def issled_time_multiple():
    file = open('table_time.csv', 'a')

    writer = csv.writer(file)
    ress = [["omega_b", "omega_o", "minutes", "ksi", "k", "h1", "h2", "time_step", "thread_count", "time", "res"]]
    res = issled_time(omega_b=1, omega_o=2, minutes=1, ksi=0, k=0, hx=1000, hy=1000, time_step=0.01, thread_count=16)
    ress.append(res)
    res = issled_time(omega_b=1, omega_o=2, minutes=1, ksi=0, k=0, hx=1000, hy=1000, time_step=0.05, thread_count=16)
    ress.append(res)
    res = issled_time(omega_b=1, omega_o=2, minutes=1, ksi=0, k=0, hx=1000, hy=1000, time_step=0.10, thread_count=16)
    ress.append(res)
    res = issled_time(omega_b=1, omega_o=2, minutes=1, ksi=0, k=0, hx=1000, hy=1000, time_step=0.15, thread_count=16)
    ress.append(res)
    res = issled_time(omega_b=1, omega_o=2, minutes=1, ksi=0, k=0, hx=1000, hy=1000, time_step=0.30, thread_count=16)
    ress.append(res)
    res = issled_time(omega_b=1, omega_o=2, minutes=1, ksi=0, k=0, hx=1000, hy=1000, time_step=0.20, thread_count=16)
    ress.append(res)
    res = issled_time(omega_b=1, omega_o=2, minutes=1, ksi=0, k=0, hx=1000, hy=1000, time_step=0.50, thread_count=16)
    ress.append(res)
    res = issled_time(omega_b=1, omega_o=2, minutes=1, ksi=0, k=0, hx=1000, hy=1000, time_step=0.60, thread_count=16)
    ress.append(res)
    res = issled_time(omega_b=1, omega_o=2, minutes=1, ksi=0, k=0, hx=1000, hy=1000, time_step=1, thread_count=16)
    ress.append(res)
    res = issled_time(omega_b=1, omega_o=2, minutes=1, ksi=0, k=0, hx=1000, hy=1000, time_step=2, thread_count=16)
    ress.append(res)

    for elem in ress:
        writer.writerow(elem)
    file.close()


if __name__ == "___main__":
