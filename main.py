import scipy.integrate as integrate
import scipy.constants as constants
import numpy as np
from numpy import ones, vstack
from numpy.linalg import lstsq
import matplotlib.pyplot as plt
import math
import tkinter as tk
import gui
from shapely.geometry import LineString

# https://www.reddit.com/r/Unity2D/comments/34qm8v/how_to_move_an_object_in_a_circular_pattern/
A_t = 15
ro_t = 10
N_a = constants.N_A
# Входные данные

R_max = 44
R_med = 22.5
R_min = 4
I_t = 5.7
L = 514 # Длина прямолинейного участка зоны распыления
M_P_distance = 0.08 # Мишень - подложка
D_baraban = 0.36 # Диаметр барабана
Velocity_baraban = 1.5 # Скорость вращения барабана
gamma_t = 0.01 # Коэффициент эмиссии
ro_t = 2700 # Плотность материала мишени
A_t = 27 # а.е.м
Y_t = 0.35 # коэффициент распыления
eps = 0.05 # заряд электрона
n = 0.5


# https://stackoverflow.com/questions/57065080/draw-perpendicular-line-of-fixed-length-at-a-point-of-another-line
def is_point_in_view(left_border_coord, right_border_coord, circle_center, point):
    k1, b1 = get_perpendicular(left_border_coord, circle_center)
    k2, b2 = get_perpendicular(right_border_coord, circle_center)

def get_perpendicular(border_coord, circle_center):
    ab = LineString([border_coord, circle_center])
    cd_length = 10
    left = ab.parallel_offset(cd_length / 2, 'left')
    right = ab.parallel_offset(cd_length / 2, 'right')
    c = left.boundary[1]
    d = right.boundary[0]  # note the different orientation for right offset
    cd = LineString([c, d])
    k, b = get_line_equation_by_two_coords(c, d)
    return k, b

# https://stackoverflow.com/questions/21565994/method-to-return-the-equation-of-a-straight-line-given-two-points
def get_line_equation_by_two_coords(a, b):
    points = [a, b]
    x_coords, y_coords = zip(*points)
    A = vstack([x_coords, ones(len(x_coords))]).T
    m, c = lstsq(A, y_coords)[0]
    return m, c


# Количество атомов материала мишени в единицу времени с определенного участка мишени
def v_t(r_1):
    return Y_t * (j_i) / eps

def j_i(r_1):
    return j_t(r_1) / (1 + gamma_t)

def j_t(r_1):
    f_integr = integrate.quad(lambda r_1: f(r_1), 0, np.inf)
    return (I_t / (math.pi * (R_max + R_min) + 2 * L)) * (f(r_1) / f_integr[0])

def f(r_1):
    sigma = (R_max - R_min) / 6
    sigma_1 = (R_med - R_min) / 3
    sigma_2 = (R_max - R_med) / 3

    left_side = 1 / (math.sqrt(2 * math.pi) * sigma)

    if (math.fabs(r_1) <= R_med):
        return left_side * math.exp(-((r_1 - R_med)**2) / (2 * (sigma_1**2)))
    else:
        return left_side * math.exp(-((r_1 - R_med)**2) / (2 * (sigma_2**2)))


def ips_t(r_1):
    return Y_t * j_t(r_1) * A_t / (N_a * eps * ro_t * (1 + gamma_t))

def t_dep(gamma_max, V_s):
    return 2 * gamma_max / V_s


def w(x_2):
    return integrate.quad(lambda t: V(x_2, t * V_s), -t_dep / 2, t_dep / 2)

def W(x_2, z_k):
    return w(x_2) * z_k

def V(x_2, y_2):
    return V_1(x_2, y_2) + V_2(x_2, y_2) + V_3(x_2, y_2) + V_4(x_2, y_2)


def V_1(x2, y2):
    l = 5 # расстояние от точки распыления
    return 1 / math.pi * integrate.dblquad(lambda r_1, teta: (r_1 * ips_t(r_1) * math.cos(TODO1) * (math.cos(TODO2)**n)) / (l**2), R_min, R_max, lambda teta: -math.pi / 2, lambda teta: math.pi / 2)

def V_3(x2, y2):
    l = 5 # расстояние от точки распыления
    return 1 / math.pi * integrate.dblquad(lambda x_1, y_1: (ips_t(x_1) * math.cos(x_1, y_1) * (math.cos(x_1, y_1)**n)) / (l**2), R_min, R_max, lambda y_1: - L / 2, lambda y_1: L / 2)


class Magnetron(object):
    def __init__(self, x_center, y_center, z_center, length, width, R_min, R_max, R_med, mishen, current) -> None:
        self.center_coord = [x_center, y_center, z_center]
        self.length = length
        self.width = width
        self.R_min = R_min
        self.R_max = R_max
        self.R_med = R_med
        self.current = current
        self.mishen = mishen
        self.R_left_center_coord = [x_center, y_center - self.length / 2, z_center]
        self.R_left_center_coord = [x_center, y_center + self.length / 2, z_center]
        self.max_angle = 60 # градусы


class Mishen(object):
    def __init__(self, Y, gamma, A, ro, n) -> None:
        self.Y = Y
        self.gamma = gamma
        self.A = A
        self.ro = ro
        self.n = n

class Ustanovka(object):
    def __init__(self, x_center, y_center, z_center, rad, M_P_distance, rpm) -> None:
        self.center_3d = [x_center, y_center, z_center]
        self.rad = rad
        self.rpm = rpm
        self.rad_per_m = self.rpm * math.pi * 2
        self.rad_per_s = self.rad_per_m / 60

    def calc_time_in_view(self, gamma_angle_max):
        return 2 * gamma_angle_max / self.rad_per_s


# def calc_f_angle_max(Ustanovka):
class UstanovkaWithPodlozkda(Ustanovka):
    def __init__(self, x_center, y_center, z_center, rad, M_P_distance, rpm, holders_rad, holders_rpm, holders_count) -> None:
        super().__init__(x_center, y_center, z_center, rad, M_P_distance, rpm)
        self.holders_count = holders_count
        self.holders_rpm = holders_rpm
        self.holders_rad = holders_rad
        self.holders_rad_per_m = self.holders_rpm * math.pi * 2
        self.holders_rad_per_s = self.holders_rad_per_m / 60
        self.holders = []

    def make_holders(self):
        shift_rad = 2 * math.pi / self.holders_count
        cur_rad = 0
        for i in range(self.holders_count):
            z = self.rad * math.cos(cur_rad) + self.center_3d[1]
            y = self.rad * math.sin(cur_rad) + self.center_3d[2]
            holder = Holder(0, y, z, 50, self.holders_rad, self.holders_rpm) # TODO 50 HARDCODED!!!!
            holder.make_points()
            self.holders.append(holder)
            cur_rad += shift_rad

class Circle_point(object):
    def __init__(self, x, y, z, radian) -> None:
        self.x = x
        self.y = y
        self.z = z
        self.radian = radian

class Holder(object):
    def __init__(self, x_center, y_center, z_center, points_count, rad, rpm) -> None:
        self.center_3d = [x_center, y_center, z_center]
        self.rad = rad
        self.rpm = rpm
        self.rad_per_m = self.rpm * math.pi * 2
        self.rad_per_s = self.rad_per_m / 60
        self.points_count = points_count
        self.points = []

    def make_points(self):
        shift_rad = 2 * math.pi / self.points_count
        i = 0
        cur_rad = 0
        for i in range(self.points_count):
            z = self.rad * math.cos(i) + self.center_3d[1]
            y = self.rad * math.sin(i) + self.center_3d[2]
            self.points.append([0, y, z, i])
            cur_rad += shift_rad

    def move_dt(self, dt):
        moved = self.rad_per_s * dt
        for point in self.points:
            prev_angle = self.center_3d[1]
            point[1] = point[1] + math.cos(moved) * self.rad
            point[2] = point[2] + math.sin(moved) * self.rad



if __name__ == "__main__":
    ustanovka = UstanovkaWithPodlozkda(0, 0, 0, 360, 50, 7.5, 50, 7.5, 8)
    ustanovka.make_holders()
    print("")

    # Рисуем центры подложек
    x_val = [holder.center_3d[1] for holder in ustanovka.holders]
    y_val = [holder.center_3d[2] for holder in ustanovka.holders]
    #plt.scatter(x_val, y_val)
    # plt.show()
    # Рисуем точки подложек
    x_val = []
    y_val = []
    # for holder in ustanovka.holders:
    #     for point in holder.points:
    #         x_val.append(point[1])
    #         y_val.append(point[2])

    # for time in np.arange(0, 10, 0.5):
    #     x_val = []
    #     y_val = []
    #     for holder in ustanovka.holders:
    #         #holder.move_dt(time)
    #         for point in holder.points:
    #             x_val.append(point[1])
    #             y_val.append(point[2])
    #     plt.scatter(x_val, y_val)
    #     plt.draw()
    #     plt.pause(1)
    #     plt.clf()

    # plt.show()

    x = []
    y = []
    r_1 = 0
    for i in np.arange(0, 50, 1):
        x.append(r_1)
        y.append(j_i(r_1))
        r_1 += 1

    print(x)
    plt.plot(x, y)
    plt.show()
    print("5")
    # a = gui.Gui()

