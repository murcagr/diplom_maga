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

def read_file(path, name):
    d_arr = []
    for filename in os.listdir(path):
        if re.match(name, filename):
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
                        d_arr.append([float(row[1]), float(row[2]), int(row[5])])
    return d_arr



d_arr_one = read_file(path, "table_tochn_time_one_thread.csv*")
d_arr_multi = read_file(path, "table_tochn_time.csv*")

print(d_arr_one)
d_arr_one.sort(key=lambda x: x[2])
print(d_arr_multi)
d_arr_multi.sort(key=lambda x: x[2])

x = []
y = []
x_multi = []
y_multi = []
c1 = []
x_tick = np.array([])

for elem in d_arr_one:
    x.append(elem[2])
    y.append(elem[1])
    c1.append("green")

for elem in d_arr_multi:
    x_multi.append(elem[2])
    y_multi.append(elem[1])
    c1.append("green")

# f = interp1d(x, y, kind='quadratic')
# xnew = np.linspace(min(x), max(x), num=len(x)*8, endpoint=True)
# X_Y_Spline = make_interp_spline(x, y)

# # Returns evenly spaced numbers
# # over a specified interval.
# X_ = np.linspace(max(x), max(y), len(x) * 8)
# Y_ = X_Y_Spline(X_)

# # plt.plot(np.arange(0, len(xnew), 1), f(xnew))
# # plt.xticks(np.arange(0, len(xnew), step), np.unique(x_tick))
# # plt.plot(np.arange(0, len(np.unique(x_tick)), 1), )
# # plt.xticks(np.arange(0, len(np.unique(x_tick)), 1), np.unique(x_tick))
# plt.plot(X_, Y_)
plt.plot(x, y, "-", c="black", label="Однопоточный метод")
plt.plot(x_multi, y_multi, "--", c="gray", label="Многопоточный метод")
plt.legend(loc='upper left')

plt.xscale('log', base=2)
plt.yscale('log', base=10)
# plt.xticks(np.unique(x_tick), np.unique(x_tick), rotation=45)
plt.xlabel("Количество точек")
plt.ylabel("Время (сек)")
plt.grid()
plt.savefig(f'{path}/res_time_parrall.png', dpi=1000)
plt.show()