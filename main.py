import logging
import numpy as np
import matplotlib.pyplot as plt
import math
import time
import tkinter as tk
import sys

from integr import double_integr_trap, double_integr_trap_multithread, midpoint_double_multithread
from model import Drum_with_podlozkda, Mishen

# https://www.reddit.com/r/Unity2D/comments/34qm8v/how_to_move_an_object_in_a_circular_pattern/


def one_dot__with_visualization(thread_count=4, minutes=1, omega_b=1, omega_o=2, ksi=0):
    ustanovka = Drum_with_podlozkda(0, 0, 0, 10, omega_b, 1, omega_o)
    ustanovka.make_custom_holder(0, ksi)
    mishen = Mishen(30, -25.5 / 2, 25.5 / 2, -11.5 / 2, 11.5 / 2)
    end_time = minutes * 60
    v_m = 1

    thickness = 0

    time_step = 0.15

    fig, (ax1, ax2) = plt.subplots(2)

    for ttime in np.arange(0, end_time + time_step, time_step):
        x_val = []
        y_val = []
        color_val = []
        y_val2 = []
        z_val2 = []
        color_val2 = []
        for holder in ustanovka.holders:
            x_val.append(holder.center_3d[0])
            y_val.append(holder.center_3d[1])
            color_val.append("blue")
            for point in holder.points:
                v_p, coord_intersections = v_m * double_integr_trap(
                    cond_enabled=True,
                    x_0=point.coord[0],
                    y_0=point.coord[1],
                    z_0=point.coord[2],
                    h1=0.1,
                    h2=0.1,
                    y_left_border_target=mishen.y_left_border_target,
                    y_right_border_target=mishen.y_right_border_target,
                    z_lower_border_target=mishen.z_lower_border_target,
                    z_higher_border_target=mishen.z_higher_border_target,
                    l=mishen.x,
                    ksi=point.current_angle,
                )

                thickness += v_p * time_step

                green_intersections_xs_top = []
                green_intersections_ys_top = []
                red_intersections_xs_top = []
                red_intersections_ys_top = []
                for coord_intersection in coord_intersections:
                    # x_val.append(coord_intersection[0])
                    # y_val.append(coord_intersection[1])
                    y_val2.append(coord_intersection[1])
                    z_val2.append(coord_intersection[2])
                    if coord_intersection[3] == 1:
                        green_intersections_xs_top.append(coord_intersection[0])
                        green_intersections_ys_top.append(coord_intersection[1])
                        # color_val.append("green")
                        color_val2.append("green")
                    else:
                        red_intersections_xs_top.append(coord_intersection[0])
                        red_intersections_ys_top.append(coord_intersection[1])
                        # color_val.append("red")
                        color_val2.append("red")

                x_val.extend(red_intersections_xs_top)
                y_val.extend(red_intersections_ys_top)
                color_val += ["red"] * len(red_intersections_xs_top)
                x_val.extend(green_intersections_xs_top)
                y_val.extend(green_intersections_ys_top)
                color_val += ["green"] * len(green_intersections_xs_top)

                x_val.append(point.coord[0])
                y_val.append(point.coord[1])
                color_val.append("lime")
            print(f't={ttime} psi={math.degrees(point.current_angle):.5f} v_p={v_p:.5f}  d= {thickness:.5f}')

        ustanovka.move_dt(time_step)

        ax1.set_xlim(-abs(ustanovka.rad) - 5, mishen.x + 5)
        ax1.set_ylim(-15, 15)
        ax1.scatter(x_val, y_val, color=color_val)

        # для мишени
        ax2.set_xlim(-20, 20)
        ax2.set_ylim(-20, 20)
        ax2.scatter(y_val2, z_val2, color=color_val2)

        # plt.axline((mishen.x, mishen.y_left_border_target), (mishen.x, mishen.y_right_border_target))
        # plt.draw()

        fig.canvas.draw()
        fig.canvas.flush_events()
        plt.pause(time_step)
        ax1.cla()
        ax2.cla()

    print(f'Вычисленная толщина пленки: {thickness}')


def one_dot(
    drum_with_podlozkda=Drum_with_podlozkda(0, 0, 0, 10, 1, 1, 2).make_custom_holder(0, 0),
    mishen=Mishen(30, -25.5 / 2, 25.5 / 2, -11.5 / 2, 11.5 / 2),
    thread_count=4,
    minutes=1,
    k=0,
    nx=100,
    ny=100,
    time_step=0.15,
):
    end_time = minutes * 60

    thickness = 0
    time_step = time_step

    for ttime in np.arange(0, end_time + time_step, time_step):
        for holder in drum_with_podlozkda.holders:
            for point in holder.points:
                v_p = midpoint_double_multithread(
                    cond_enabled=True,
                    x_0=point.coord[0],
                    y_0=point.coord[1],
                    z_0=point.coord[2],
                    nx=nx,
                    ny=ny,
                    k=k,
                    thread_count=thread_count,
                    y_left_border_target=mishen.y_left_border_target,
                    y_right_border_target=mishen.y_right_border_target,
                    z_lower_border_target=mishen.z_lower_border_target,
                    z_higher_border_target=mishen.z_higher_border_target,
                    l=mishen.x,
                    ksi=point.current_angle,
                )
                # exit(0)
                # v_p = v_p * (1 / math.pi)
                thickness += v_p * time_step

        print(
            f't={ttime:.3f} psi={math.degrees(holder.current_angle):.3f} ksi={math.degrees(point.current_angle):.3f} v_p={v_p:.3f}  d= {thickness:.3f}'
        )
        # file.write(f't={ttime:.3f} psi={math.degrees(holder.current_angle):.3f} ksi={math.degrees(point.current_angle):.3f} v_p={v_p:.3f}  d={thickness:.3f}\n')
        drum_with_podlozkda.move_dt(time_step)

    print(f'd: {thickness}')
    # file.close()
    return thickness


def v_p_intrg(x, y):
    return math.cos(y) * math.sin(y)


if __name__ == "__main__":
    logging.basicConfig(stream=sys.stdout, level=logging.INFO)
    # start = time.time()
    # # midpoint_double1(v_p_intrg, 0, math.pi * 2, 0, math.pi / 2, 10000, 10000)
    # end = time.time()
    # print(end - start)
    # res = midpoint_double_multithread(v_p_intrg, 0, math.pi * 2, 100, 0, math.pi / 2, 100)
    # print(res)
    start = time.time()
    drum_with_podlozkda = Drum_with_podlozkda(0, 0, 0, 10, 1, 1, 2)
    drum_with_podlozkda.make_custom_holder(0, 0)
    mishen = Mishen(30, -25.5 / 2, 25.5 / 2, -11.5 / 2, 11.5 / 2)
    one_dot(drum_with_podlozkda=drum_with_podlozkda, mishen=mishen, nx=100, ny=100)
    end = time.time()
    print(end - start)

    # # one_dot__with_visualization()
    # start = time.time()
    # one_dot(omega_b=1, omega_o=1, minutes=1, ksi=0, k=0)
    # end = time.time()
    # print(end - start)
    # # one_dot(omega_b=1, omega_o=2, minutes=1, ksi=0, thread_count=4)
    # # one_dot__with_visualization(omega_b=1, omega_o=2, minutes=1, ksi=0)
    # issled_time_multiple()
    # issled_multiple_one_dot()
    # start = time.time()
    # one_dot(thread_count=1)
    # end = time.time()
    # res, _ = double_integr_trap_multithread(
    #     cond_enabled=False,
    #     h1=0.0001,
    #     h2=0.0001,
    #     k=0,
    #     thread_count=16,)
    # print(res)
    # print(end - start)
    # calc_plain_z_axis_multiple_points()
