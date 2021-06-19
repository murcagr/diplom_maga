import csv
import os
import re
from fractions import Fraction
import matplotlib.pyplot as plt
import numpy as np
from scipy.interpolate import interp1d
from scipy.interpolate import make_interp_spline

# def find_min_or_max(list, n):
#     max_i = []
#     for i in range(len(list)):
#         curr_max_i = 0
#         if i not in max_i:
#             if list[i] > list[curr_max_i]:


path = "/home/remini/learning/diplom_diff_k"
res = []
for filename in os.listdir(path):
    if re.match("table_nera*", filename):
        filename_s = filename.split("_")
        # print(filename_s[1][2:])
        k = float(filename_s[5].split(".csv")[0][1:])
        with open(os.path.join(path, filename), 'r') as f:
            print(filename)
            reader = csv.reader(f, delimiter=',', quotechar=',', quoting=csv.QUOTE_MINIMAL)
            d_arr = []
            for row in reader:
                print(row)
                if re.match("omega*", row[0]):
                    continue
                else:
                    d_arr.append(float(row[10]))
            maxx = max(d_arr)
            minn = min(d_arr)
            koeff = (maxx - minn) / maxx
            res.append([koeff, k])

res.sort(key=lambda x: x[0])

print(res)

x = []
y = []
# x_tick = np.array([])

for elem in res:
    #if Fraction(elem[0]).limit_denominator() not in x_tick:
        # x_tick = np.append(x_tick, Fraction(elem[0]).limit_denominator())

    x.append(elem[1])
    y.append(elem[0])


# f = interp1d(x, y, kind='quadratic')
# xnew = np.linspace(min(x), max(x), num=len(x)*8, endpoint=True)
X_Y_Spline = make_interp_spline(x, y)

# Returns evenly spaced numbers
# over a specified interval.
X_ = np.linspace(min(x), max(x), len(x) * 6)
Y_ = X_Y_Spline(X_)

# max and min

print("Maximals")
maxes_i = sorted(range(len(y)), key=lambda i: y[i])[-10:]
print(maxes_i)
for elem in maxes_i:
    print(x[elem], y[elem])

print("Minimals")
min_i = sorted(range(len(y)), key=lambda i: y[i])[:10]
print(min_i)
for elem in min_i:
    print(x[elem], y[elem])


# plt.plot(np.arange(0, len(xnew), 1), f(xnew))
# plt.xticks(np.arange(0, len(xnew), step), np.unique(x_tick))
# plt.plot(np.arange(0, len(np.unique(x_tick)), 1), )
# plt.xticks(np.arange(0, len(np.unique(x_tick)), 1), np.unique(x_tick))
plt.plot(x, y, c="black")
plt.grid(True)
# plt.scatter(x, y)
# plt.xticks(np.unique(x_tick), np.unique(x_tick), rotation=45)
plt.xlabel("Степень затенения")
plt.ylabel("Неоднородность по поверхности образца")
plt.savefig(f'{path}/res.png', dpi=1000)
plt.show()
