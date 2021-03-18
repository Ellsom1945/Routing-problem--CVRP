import numpy as np
import re

n = 0
j = 0
i = 0
capacity = 0
site = []
things = []
f = open("../data/A/A-n53-k7.vrp", 'r')
lines = []
line = f.readline().strip('\n')
carnum = int(re.findall('\d+', f.name)[1])
while line:
    lines.append(line)
    line = f.readline().strip('\n')
    if line.__contains__("DIMENSION"):
        n = int(line.lstrip('DIMENSION : '))
    site = np.zeros((n, 2))
    things = np.zeros(n)
    if line.__contains__("CAPACITY"):
        capacity = int(line.lstrip('CAPACITY : '))
    site = np.zeros((n, 2))
    if line.__contains__("NODE_COORD_SECTION"):
        line = f.readline().strip('\n')
        while not line.__contains__("DEMAND_SECTION"):
            a, site[j][0], site[j][1] = line.strip().split(" ")
            j = int(a)
            line = f.readline().strip('\n')
    if line.__contains__("DEMAND_SECTION"):
        line = f.readline().strip('\n')
        while not line.__contains__("DEPOT_SECTION"):
            a, things[i] = line.strip().split(" ")
            i = int(a)
            line = f.readline().strip('\n')
    if line.__contains__("DEPOT_SECTION"):
        break


def getdistmat(coordinates):
    num1 = coordinates.shape[0]  # 矩阵的行数
    distmat = np.zeros((num1, num1))  # 构造全零矩阵
    for i in range(0, num1):
        for j in range(0, num1):  # 利用数组求二范式计算距离
            distmat[i][j] = round(pow((pow((coordinates[i][0] - coordinates[j][0]), 2) + \
                                       pow((coordinates[i][1] - coordinates[j][1]), 2)), 0.5))
    return distmat


distmat = getdistmat(site)
