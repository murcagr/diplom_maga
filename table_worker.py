import csv
import os
import re
from fractions import Fraction
import matplotlib.pyplot as plt
import numpy as np
from scipy.interpolate import interp1d
from scipy.interpolate import make_interp_spline

path = "/home/remini/learning/diplom_synced_0_test_all"
res = []
for filename in os.listdir(path):
    if re.match("table_ob*", filename):
        with open(os.path.join(path, filename), 'r') as f:
            print(filename)
            reader = csv.reader(f, delimiter=',', quotechar=',',
                        quoting=csv.QUOTE_MINIMAL)
            d_arr = []
            sootn = 0
            sootn_math = 0
            for row in reader:
                print(row)
                if re.match("omega*",row[0]):
                    omega_b = row[0].rsplit("=")[1]
                    omega_o = row[1].rsplit("=")[1]
                    sootn = f"{omega_b}/{omega_o}"
                    sootn_math = float(omega_b)/float(omega_o)
                    continue
                if re.match("angle*",row[0]):
                    continue
                else:
                    d_arr.append(float(row[1]))
            maxx = max(d_arr)
            minn = min(d_arr)
            koeff = (maxx - minn) / maxx
            print(koeff)
            print(sootn)
            res.append([sootn_math, koeff, sootn])

res.sort(key=lambda x: x[0])

print(res)

x = []
y = []
x_tick = np.array([])

for elem in res:
    if Fraction(elem[0]).limit_denominator() not in x_tick:
        x_tick = np.append(x_tick,Fraction(elem[0]).limit_denominator())
        x.append(elem[0])
        y.append(elem[1])


# f = interp1d(x, y, kind='quadratic')
# xnew = np.linspace(min(x), max(x), num=len(x)*8, endpoint=True)
X_Y_Spline = make_interp_spline(x, y)

# Returns evenly spaced numbers
# over a specified interval.
X_ = np.linspace(max(x), max(y), len(x)*8)
Y_ = X_Y_Spline(X_)

# plt.plot(np.arange(0, len(xnew), 1), f(xnew))
# plt.xticks(np.arange(0, len(xnew), step), np.unique(x_tick))
# plt.plot(np.arange(0, len(np.unique(x_tick)), 1), )
# plt.xticks(np.arange(0, len(np.unique(x_tick)), 1), np.unique(x_tick))
plt.plot(X_, Y_)
plt.scatter(x, y)
plt.xticks(np.unique(x_tick), np.unique(x_tick), rotation=45)
plt.xlabel("Отношение скорости барабана к скорости образца")
plt.ylabel("Неоднородность по окружности")
plt.savefig(f'{path}/res.png', dpi=1000)
plt.show()