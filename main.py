import logging
import scipy.integrate as integrate
import scipy.constants as constants
import numpy as np
from numpy import ones, vstack
from numpy.linalg import lstsq
import matplotlib.pyplot as plt
import math
import tkinter as tk
from shapely.geometry import LineString

from integr import double_integr_trap, double_integr_trap_multithread

# https://www.reddit.com/r/Unity2D/comments/34qm8v/how_to_move_an_object_in_a_circular_pattern/
A_t = 15
ro_t = 10
N_a = constants.N_A
# Входные данные

R_max = 44
R_med = 22.5
R_min = 4
I_t = 5.7
L = 514  # Длина прямолинейного участка зоны распыления
M_P_distance = 0.08  # Мишень - подложка
D_baraban = 0.36  # Диаметр барабана
Velocity_baraban = 1.5  # Скорость вращения барабана
gamma_t = 0.01  # Коэффициент эмиссии
ro_t = 2700  # Плотность материала мишени
A_t = 27  # а.е.м
Y_t = 0.35  # коэффициент распыления
eps = 0.05  # заряд электрона
n = 0.5


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
        self.max_angle = 60  # градусы


class Mishen(object):
    def __init__(self, x, z_lower_border_target, z_higher_border_target, y_left_border_target, y_right_border_target):
        self.z_lower_border_target = z_lower_border_target
        self.z_higher_border_target = z_higher_border_target
        self.y_left_border_target = y_left_border_target
        self.y_right_border_target = y_right_border_target
        self.x = x


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
    def __init__(self, x_center, y_center, z_center, rad, rpm, holders_rad, holders_rpm) -> None:
        super().__init__(x_center, y_center, z_center, rad, M_P_distance, rpm)

        self.holders_rpm = holders_rpm
        self.rad = rad
        self.rpm = rpm
        self.rad_per_m = self.rpm * math.pi * 2
        self.rad_per_s = self.rad_per_m / 60
        self.holders_rad = holders_rad
        self.holders_rad_per_m = self.holders_rpm * math.pi * 2
        self.holders_rad_per_s = self.holders_rad_per_m / 60
        self.holders = []

    def make_holders(self, holders_count, points_count):
        self.holders_count = holders_count
        shift_rad = 2 * math.pi / self.holders_count
        cur_angle = 0
        for i in range(self.holders_count):
            x = self.rad * math.cos(cur_angle) + self.center_3d[0]
            y = self.rad * math.sin(cur_angle) + self.center_3d[1]
            holder = Holder(x, y, 0, cur_angle, self.holders_rad, self.holders_rpm)
            holder.make_points(points_count)
            self.holders.append(holder)
            cur_angle += shift_rad

    def make_custom_holder(self, holder_angle, point_angle):
        x = self.rad * math.cos(holder_angle) + self.center_3d[0]
        y = self.rad * math.sin(holder_angle) + self.center_3d[1]
        holder = Holder(x, y, 0, holder_angle, self.holders_rad, self.holders_rpm)
        holder.make_custom_point(point_angle)
        self.holders.append(holder)

    def move_dt(self, dt):
        moved = self.rad_per_s * dt
        for holder in self.holders:
            holder.current_angle = holder.current_angle + moved
            holder.center_3d[0] = math.cos(holder.current_angle) * self.rad
            holder.center_3d[1] = math.sin(holder.current_angle) * self.rad
            holder.move_dt(dt)


class Holder_point(object):
    def __init__(self, x, y, z, curr_angle) -> None:
        self.coord = [x, y, z]
        self.current_angle = curr_angle
        self.thin = 0


class Holder(object):
    def __init__(self, x_center, y_center, z_center, curr_angle, rad, rpm) -> None:
        self.center_3d = [x_center, y_center, z_center]
        self.rad = rad
        self.rpm = rpm
        self.rad_per_m = self.rpm * math.pi * 2
        self.rad_per_s = self.rad_per_m / 60
        self.points = []
        self.current_angle = curr_angle

    def make_points(self, points_count):
        self.points_count = points_count
        shift_rad = 2 * math.pi / self.points_count
        i = 0
        cur_rad = 0
        for i in range(self.points_count):
            x = self.rad * math.cos(cur_rad) + self.center_3d[0]
            y = self.rad * math.sin(cur_rad) + self.center_3d[1]
            new_point = Holder_point(x, y, 0, cur_rad)
            cur_rad += shift_rad
            self.points.append(new_point)

    def make_custom_point(self, angle):
        x = self.rad * math.cos(angle) + self.center_3d[0]
        y = self.rad * math.sin(angle) + self.center_3d[1]
        new_point = Holder_point(x, y, 0, angle)
        self.points.append(new_point)

    def move_dt(self, dt):
        moved = self.rad_per_s * dt
        for point in self.points:
            point.current_angle = point.current_angle + moved
            point.coord[0] = self.center_3d[0] + math.cos(point.current_angle) * self.rad
            point.coord[1] = self.center_3d[1] + math.sin(point.current_angle) * self.rad


def calc_plain_z_axis_multiple_points():
    mishen = Mishen(30, -25.5 / 2, 25.5 / 2, -11.5 / 2, 11.5 / 2)

    ustanovka = UstanovkaWithPodlozkda(0, 0, 0, 10, 7.5, 1, 7.5)
    ustanovka.make_holders(6, 50)
    time_step = 0.4

    # fig = plt.figure()
    # fig.canvas.mpl_connect('close_event', exit(0))

    for time in np.arange(0, 20, time_step):
        x_val = []
        y_val = []
        color_val = []
        for holder in ustanovka.holders:
            x_val.append(holder.center_3d[0])
            y_val.append(holder.center_3d[1])
            color_val.append("blue")
            for point in holder.points:
                x_val.append(point.coord[0])
                y_val.append(point.coord[1])

                v_p, coord_intersections = double_integr_trap(
                    cond_enabled=True,
                    x_0=point.coord[0],
                    y_0=point.coord[1],
                    z_0=point.coord[2],
                    y_left_border_target=mishen.y_left_border_target,
                    y_right_border_target=mishen.y_right_border_target,
                    z_lower_border_target=mishen.z_lower_border_target,
                    z_higher_border_target=mishen.z_higher_border_target,
                    l=mishen.x,
                    ksi=point.current_angle,
                )
                if v_p != 0:
                    color_val.append("lime")
                    for coord_intersection in coord_intersections:
                        x_val.append(coord_intersection[0])
                        y_val.append(coord_intersection[1])
                        if coord_intersection[3] == 1:
                            color_val.append("green")
                        else:
                            color_val.append("red")
                else:
                    color_val.append("red")

        ustanovka.move_dt(time_step)

        plt.xlim(-abs(ustanovka.rad) - 5, mishen.x + 5)
        plt.ylim(-15, 15)

        # plt.axline((mishen.x, mishen.y_left_border_target), (mishen.x, mishen.y_right_border_target))

        plt.scatter(x_val, y_val, color=color_val, s=1)
        plt.draw()
        plt.pause(0.4)
        plt.clf()


def one_dot__with_visualization():
    ustanovka = UstanovkaWithPodlozkda(0, 0, 0, 10, 7.5, 1, 7.5)
    ustanovka.make_custom_holder(0, 0)
    mishen = Mishen(30, -25.5 / 2, 25.5 / 2, -11.5 / 2, 11.5 / 2)
    print("")

    # fig = plt.figure()
    # fig.canvas.mpl_connect('close_event', exit(0))

    time_step = 0.1

    for time in np.arange(0, 20, time_step):
        x_val = []
        y_val = []
        color_val = []
        for holder in ustanovka.holders:
            x_val.append(holder.center_3d[0])
            y_val.append(holder.center_3d[1])
            color_val.append("blue")
            for point in holder.points:
                v_p, coord_intersections = double_integr_trap(
                    cond_enabled=True,
                    x_0=point.coord[0],
                    y_0=point.coord[1],
                    z_0=point.coord[2],
                    y_left_border_target=mishen.y_left_border_target,
                    y_right_border_target=mishen.y_right_border_target,
                    z_lower_border_target=mishen.z_lower_border_target,
                    z_higher_border_target=mishen.z_higher_border_target,
                    l=mishen.x,
                    ksi=point.current_angle,
                )

                for coord_intersection in coord_intersections:
                    x_val.append(coord_intersection[0])
                    y_val.append(coord_intersection[1])
                    if coord_intersection[3] == 1:
                        color_val.append("green")
                    else:
                        color_val.append("red")

                x_val.append(point.coord[0])
                y_val.append(point.coord[1])
                color_val.append("lime")

        ustanovka.move_dt(time_step)

        plt.xlim(-abs(ustanovka.rad) - 5, mishen.x + 5)
        plt.ylim(-15, 15)

        # plt.axline((mishen.x, mishen.y_left_border_target), (mishen.x, mishen.y_right_border_target))

        plt.scatter(x_val, y_val, color=color_val)
        plt.draw()
        plt.pause(time_step)
        plt.clf()


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    one_dot__with_visualization()
    # calc_plain_z_axis_multiple_points()
