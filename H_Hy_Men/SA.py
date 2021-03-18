import math
import random
import numpy as np
from numpy import random
from H_Hy_Men import VRPLibReader
import copy


def value_function(distmat, list1, weight, things):
    s = 0
    w = weight
    tlist = list(list1).copy()
    tlist.insert(0, 0)
    for i in range(0, len(tlist) - 1):
        w = w - things[tlist[i + 1]]
        if (w < 0):  # 已超过最大运输距离或货物不足，返回
            s += distmat[tlist[i]][0] + distmat[0][tlist[i + 1]]
            w = weight - things[tlist[i + 1]]
        else:
            # 计算到K城市的距离
            s += distmat[tlist[i]][tlist[i + 1]]
    s += distmat[tlist[-1]][0]
    return s


class SA(object):
    def __init__(self, Tmax=50, Tmin=1e-2, t=0.9, L=50):
        self.T = Tmax
        self.T_end = Tmin
        self.t = t
        self.L = L

    def SA_solver(self, spath, ju=1):
        path = copy.deepcopy(spath)
        distmat = copy.deepcopy(VRPLibReader.distmat)
        things = copy.deepcopy(VRPLibReader.things)
        weight = copy.deepcopy(VRPLibReader.capacity)
        if ju == 1:
            for i in path:
                del i[0]
                del i[-1]
            path = [x for j in path for x in list(j)]
        temp1 = list(path).copy()
        temp3 = temp1.copy()
        tpath = temp1.copy()  # 最佳路径
        tbest = value_function(distmat, tpath, weight, things)  # 最佳总长度
        th = 0
        while self.T > self.T_end:
            self.T *= self.t
            z = self.L
            while z > 0:
                z -= 1
                temp2 = list(temp1)
                temp2 = changepath(temp2)  # 扰动解
                t1 = value_function(distmat, temp1, weight, things)
                t2 = value_function(distmat, temp2, weight, things)
                if (t1 > t2):
                    temp1 = list(temp2)
                    if (t2 < tbest):
                        tpath = temp2.copy()
                        tbest = t2
                    continue
                p = math.exp((t1 - t2) / self.T)
                if (random.random() < p):
                    temp1 = list(temp2)
            if (temp3 == temp1):
                th += 1
            else:
                th = 0
                temp3 = temp1.copy()
            if th == 5:
                break
        if ju == 1:
            finalpath = []
            w = 0  # 计算载货量
            i = 0
            j = len(tpath)
            tt = [0]
            while (i < j):
                if (w + things[tpath[i]] > weight):
                    tt.append(0)
                    finalpath.append(tt)
                    tt = [0]
                    w = things[tpath[i]]
                    tt.append(tpath[i])
                else:
                    w = w + things[tpath[i]]
                    tt.append(tpath[i])
                i += 1
            if tt != [] or tt != [0]:
                tt.append(0)
                finalpath.append(tt)
            return finalpath, tbest
        else:
            return tpath, tbest


# 随机解生成函数
def rand(array_1, num_place):
    array_1 = np.random.permutation(range(1, num_place + 1))
    return array_1


# 产生新解——逆序
def by_chpa1(tpath):
    x = random.randint(0, len(tpath) - 1)
    y = random.randint(0, len(tpath) - 1)
    while x == y:
        x = random.randint(0, len(tpath) - 1)
    if x < y:
        while x != y and x < y:
            tpath[x], tpath[y] = tpath[y], tpath[x]
            x += 1
            y -= 1
    else:
        while x != y and y < x:
            tpath[x], tpath[y] = tpath[y], tpath[x]
            y += 1
            x -= 1
    return tpath


# 产生新解——三变化
def by_chpa2(tpath):
    path = []
    x = random.randint(0, len(tpath) - 2)
    y = random.randint(0, len(tpath) - 2)
    while x == y:
        x = random.randint(0, len(tpath) - 2)
    if x < y:
        z = random.randint(y + 1, len(tpath) - 1)
        path[0:x] = tpath[0:x]
        path.append(tpath[z])
        path[x + 1:y + 2] = tpath[x:y + 1]
        path[y + 2:z + 1] = tpath[y + 1:z]
        if z + 1 <= len(tpath) - 1:
            path[z + 1:] = tpath[z + 1:]
    else:
        z = random.randint(y + 1, len(tpath) - 1)
        path[0:y] = tpath[0:y]
        path.append(tpath[z])
        path[y + 1:x + 2] = tpath[y:x + 1]
        path[x + 2:z + 1] = tpath[x + 1:z]
        if z + 1 <= len(tpath) - 1:
            path[z + 1:] = tpath[z + 1:]
    return path


# 产生新解——移位
def by_chpa3(tpath):
    path = []
    x = random.randint(0, len(tpath) - 2)
    y = random.randint(0, len(tpath) - 2)
    while x == y:
        x = random.randint(0, len(tpath) - 2)
    if x < y:
        z = random.randint(1, len(tpath) - 1 - y)
        j = len(tpath) - 1
        for i in range(z):
            path.append(tpath[j])
            j -= 1
        path[z:] = tpath[:len(tpath) - z]
    else:
        z = random.randint(1, len(tpath) - 1 - x)
        j = len(tpath) - 1
        for i in range(z):
            path.append(tpath[j])
            j -= 1
        path[z:] = tpath[:len(tpath) - z]
    return path


# 产生新解——交换
def by_chpa4(tpath):
    x = random.randint(0, len(tpath) - 1)
    y = random.randint(0, len(tpath) - 1)
    while x == y:
        x = random.randint(0, len(tpath) - 1)
    tpath[x], tpath[y] = tpath[y], tpath[x]
    return tpath


# 产生新解
def changepath(tpath):
    i = random.randint(1, 5)
    if i == 1:
        return by_chpa1(tpath)
    elif i == 2:
        return by_chpa2(tpath)
    elif i == 3:
        return by_chpa3(tpath)
    elif i == 4:
        return by_chpa4(tpath)
    else:
        return rand(tpath, len(list(tpath)))
