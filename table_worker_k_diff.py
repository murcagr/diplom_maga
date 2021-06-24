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
res11 = []
for filename in os.listdir(path):
    if re.match("table_nera*", filename):
        filename_s = filename.split("_")
        # print(filename_s[1][2:])
        if not(int(filename_s[2][2:]) == 1 and int(filename_s[3][2:]) == 1):
            continue
        k = float(filename_s[5].split(".csv")[0][1:])
        if k >= 0.055253796026246194:
            continue
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
            res11.append([koeff, k])

res12 = []
for filename in os.listdir(path):
    if re.match("table_nera*", filename):
        filename_s = filename.split("_")
        # print(filename_s[1][2:])
        if not(int(filename_s[2][2:]) == 1 and int(filename_s[3][2:]) == 2):
            continue
        k = float(filename_s[5].split(".csv")[0][1:])
        if k >= 0.055253796026246194:
            continue
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
            res12.append([koeff, k])

res1523 = []
for filename in os.listdir(path):
    if re.match("table_nera*", filename):
        filename_s = filename.split("_")
        # print(filename_s[1][2:])
        if not(int(filename_s[2][2:]) == 15 and int(filename_s[3][2:]) == 23):
            continue
        k = float(filename_s[5].split(".csv")[0][1:])
        if k >= 0.055253796026246194:
            continue
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
            res1523.append([koeff, k])


res11.sort(key=lambda x: x[0])
res12.sort(key=lambda x: x[0])
res1523.sort(key=lambda x: x[0])


# print(res)

x = []
y = []

x2 = []
y2 = []

x3 = []
y3 = []
# x_tick = np.array([])

for elem in res11:
    #if Fraction(elem[0]).limit_denominator() not in x_tick:
        # x_tick = np.append(x_tick, Fraction(elem[0]).limit_denominator())
    x.append(elem[1])
    y.append(elem[0])

for elem in res12:
    #if Fraction(elem[0]).limit_denominator() not in x_tick:
        # x_tick = np.append(x_tick, Fraction(elem[0]).limit_denominator())
    x2.append(elem[1])
    y2.append(elem[0])

for elem in res1523:
    #if Fraction(elem[0]).limit_denominator() not in x_tick:
        # x_tick = np.append(x_tick, Fraction(elem[0]).limit_denominator())
    x3.append(elem[1])
    y3.append(elem[0])


# f = interp1d(x, y, kind='quadratic')
# xnew = np.linspace(min(x), max(x), num=len(x)*8, endpoint=True)
X_Y_Spline = make_interp_spline(x, y)

# Returns evenly spaced numbers
# over a specified interval.
X_ = np.linspace(min(x), max(x), len(x) * 6)
Y_ = X_Y_Spline(X_)

# max and min

print("Maximals")
maxes_i = sorted(range(len(y3)), key=lambda i: y3[i])[-10:]
print(maxes_i)
for elem in maxes_i:
    print(x3[elem], y3[elem])

print("Minimals")
min_i = sorted(range(len(y3)), key=lambda i: y3[i])[:10]
print(min_i)
for elem in min_i:
    print(x3[elem], y3[elem])


# plt.plot(np.arange(0, len(xnew), 1), f(xnew))
# plt.xticks(np.arange(0, len(xnew), step), np.unique(x_tick))
# plt.plot(np.arange(0, len(np.unique(x_tick)), 1), )
# plt.xticks(np.arange(0, len(np.unique(x_tick)), 1), np.unique(x_tick))
plt.plot(x, y, c="black", label="1/1")
plt.plot(x2, y2, '--', c="black", label="1/2")
plt.plot(x3, y3, '-.', c="black", label="15/23")
plt.legend(loc='upper left')
# plt.yscale("log", base=10)
plt.grid(True)
# plt.scatter(x, y)
# plt.xticks(np.unique(x_tick), np.unique(x_tick), rotation=45)
# plt.set
plt.xlabel("Коэффициент рассеяния")
plt.ylabel("Неоднородность по поверхности образца")
plt.savefig(f'{path}/res1_1.png')
plt.show()
