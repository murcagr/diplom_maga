import integr
import math

def V_p(V_m, x_0, y_0, z_0, l):
    return 1 / math.pi * V_m * integr.double_integr_trap(x_0=x_0, y_0=y_0, z_0=z_0, l=l)


# https://stackoverflow.com/questions/57065080/draw-perpendicular-line-of-fixed-length-at-a-point-of-another-line
# def is_point_in_view(left_border_coord, right_border_coord, circle_center, point):
#     k1, b1 = get_perpendicular(left_border_coord, circle_center)
#     k2, b2 = get_perpendicular(right_border_coord, circle_center)

# def get_perpendicular(border_coord, circle_center):
#     ab = LineString([border_coord, circle_center])
#     cd_length = 10
#     left = ab.parallel_offset(cd_length / 2, 'left')
#     right = ab.parallel_offset(cd_length / 2, 'right')
#     c = left.boundary[1]
#     d = right.boundary[0]  # note the different orientation for right offset
#     cd = LineString([c, d])
#     k, b = get_line_equation_by_two_coords(c, d)
#     return k, b

# # https://stackoverflow.com/questions/21565994/method-to-return-the-equation-of-a-straight-line-given-two-points
# def get_line_equation_by_two_coords(a, b):
#     points = [a, b]
#     x_coords, y_coords = zip(*points)
#     A = vstack([x_coords, ones(len(x_coords))]).T
#     m, c = lstsq(A, y_coords)[0]
#     return m, c


# Количество атомов материала мишени в единицу времени с определенного участка мишени
# def v_t(r_1):
#     return Y_t * (j_i) / eps

# def j_i(r_1):
#     return j_t(r_1) / (1 + gamma_t)

# def j_t(r_1):
#     f_integr = integrate.quad(lambda r_1: f(r_1), 0, np.inf)
#     return (I_t / (math.pi * (R_max + R_min) + 2 * L)) * (f(r_1) / f_integr[0])

# def f(r_1):
#     sigma = (R_max - R_min) / 6
#     sigma_1 = (R_med - R_min) / 3
#     sigma_2 = (R_max - R_med) / 3

#     left_side = 1 / (math.sqrt(2 * math.pi) * sigma)

#     if (math.fabs(r_1) <= R_med):
#         return left_side * math.exp(-((r_1 - R_med)**2) / (2 * (sigma_1**2)))
#     else:
#         return left_side * math.exp(-((r_1 - R_med)**2) / (2 * (sigma_2**2)))


# def ips_t(r_1):
#     return Y_t * j_t(r_1) * A_t / (N_a * eps * ro_t * (1 + gamma_t))

# def t_dep(gamma_max, V_s):
#     return 2 * gamma_max / V_s

# def w(x_2):
#     return integrate.quad(lambda t: V(x_2, t * V_s), -t_dep / 2, t_dep / 2)

# def W(x_2, z_k):
#     return w(x_2) * z_k

# def V(x_2, y_2):
#     return V_1(x_2, y_2) + V_2(x_2, y_2) + V_3(x_2, y_2) + V_4(x_2, y_2)


# def V_1(x2, y2):
#     l = 5 # расстояние от точки распыления
#     return 1 / math.pi * integrate.dblquad(lambda r_1, teta: (r_1 * ips_t(r_1) * math.cos(TODO1) * (math.cos(TODO2)**n)) / (l**2), R_min, R_max, lambda teta: -math.pi / 2, lambda teta: math.pi / 2)

# def V_3(x2, y2):
#     l = 5 # расстояние от точки распыления
#     return 1 / math.pi * integrate.dblquad(lambda x_1, y_1: (ips_t(x_1) * math.cos(x_1, y_1) * (math.cos(x_1, y_1)**n)) / (l**2), R_min, R_max, lambda y_1: - L / 2, lambda y_1: L / 2)
