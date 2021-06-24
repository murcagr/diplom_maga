import csv
import os
import re
from fractions import Fraction
import matplotlib.pyplot as plt
import numpy as np
from scipy.interpolate import interp1d
from scipy.interpolate import make_interp_spline

path = "/home/remini/learning/diplom"
res = []
d_arr = []
for filename in os.listdir(path):
    if re.match("table_tochn_time_one_thread.csv*", filename):
        with open(os.path.join(path, filename), 'r') as f:
            print(filename)
            reader = csv.reader(f, delimiter=',', quotechar=',',
                        quoting=csv.QUOTE_MINIMAL)
            sootn = 0
            sootn_math = 0
            for row in reader:
                print(row)
                if re.match("omega*", row[0]):
                    omega_b = row[0].rsplit("=")[1]
                    omega_o = row[1].rsplit("=")[1]
                    sootn = f"{omega_b}/{omega_o}"
                    sootn_math = float(omega_b) / float(omega_o)
                    continue
                if re.match("angle*", row[0]):
                    continue
                else:
                    d_arr.append([float(row[2]), int(row[5])])

d_arr.sort(key=lambda x: x[1])
print(d_arr)

x = []
y = []
x_tick = np.array([])

appended = []
for elem in d_arr:
    if elem[1] not in appended:
        x.append(elem[1])
        y.append(elem[0])
        appended.append(elem[1])

# xnew = np.linspace(min(x), max(x), 100)
# bspline = make_interp_spline(x, y)
# y_smoothed = bspline(xnew)
# plt.plot(xnew, y_smoothed, c="black")

X_Y_Spline = make_interp_spline(x, y)

# Returns evenly spaced numbers
# over a specified interval.
X_ = np.linspace(min(x), max(x), 100)
Y_ = X_Y_Spline(X_)

# # plt.plot(np.arange(0, len(xnew), 1), f(xnew))
# # plt.xticks(np.arange(0, len(xnew), step), np.unique(x_tick))
# # plt.plot(np.arange(0, len(np.unique(x_tick)), 1), )
# # plt.xticks(np.arange(0, len(np.unique(x_tick)), 1), np.unique(x_tick))
plt.plot(x, y, c="black")
# plt.plot(x, y)
# plt.yscale('log', base=2)
# plt.yscale('log')
plt.xscale('log', base=2)
# plt.xticks(np.unique(x_tick), np.unique(x_tick), rotation=45)
plt.xlabel("Количество точек")
plt.ylabel("Время (cек)")
plt.grid()
plt.savefig(f'{path}/res_kol_time.png', dpi=1000)
plt.show()