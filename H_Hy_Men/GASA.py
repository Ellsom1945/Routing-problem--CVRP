# 改进遗传:四种交叉方式—改进退火
from H_Hy_Men.SA import *
import math
import random
import numpy as np
from H_Hy_Men import VRPLibReader


# 三交叉算子
def GASA_threecross(popva, poppath, n):
    probability = ((1 / popva) / ((1 / popva).sum())).cumsum()
    father_pop = np.zeros((3, n)).astype(int)
    k = []
    for i in range(3):
        t = probability.copy()
        t -= np.random.rand()
        j = list(t > 0).index(True)
        while j in k:
            t = probability.copy()
            t -= np.random.rand()
            j = list(t > 0).index(True)
        k.append(j)
        father_pop[i] = poppath[j].copy()
    return father_pop


# 右轮变换
def GASA_right_rotation(i, path, n):
    j = list(path).index(i)
    temppath = np.zeros(n).astype(int)
    temppath[:n - j] = path[j:]
    temppath[n - j:] = path[:j]
    return temppath


# 左轮变换
def GASA_left_rotation(i, path, n):
    j = list(path).index(i)
    temppath = np.zeros(n).astype(int)
    temppath[:n - j - 1] = path[j + 1:]
    temppath[n - j - 1:] = path[:j + 1]
    return temppath


# 产生子代1
def son1(fpop, n, distmat):
    new1 = [0] * n
    q = random.randint(1, n)
    new1[0] = q
    unv = list(set(range(1, n + 1)))
    unv.remove(q)
    for i in range(1, n):
        for k in range(3):
            fpop[k] = GASA_right_rotation(q, fpop[k], n)
        b = 0
        for k in range(3):
            if (fpop[k][1] in unv) == False:
                continue
            if distmat[fpop[k][0]][fpop[k][1]] < distmat[fpop[b][0]][fpop[b][1]] or (fpop[b][1] in unv) == False:
                b = k
        if (fpop[b][1] in unv) == False:
            q = random.choice(unv)
        else:
            q = fpop[b][1]
        unv.remove(q)
        new1[i] = q
    return new1


# 产生子代2
def son2(fpop, t, n, distmat):
    new2 = [0] * n
    q = t
    new2[0] = q
    unv = list(set(range(1, n + 1)))
    unv.remove(q)
    for i in range(1, n):
        for k in range(3):
            fpop[k] = GASA_left_rotation(q, fpop[k], n)
        b = 0
        for k in range(3):
            if (fpop[k][-2] in unv) == False:
                continue
            if distmat[fpop[k][-1]][fpop[k][-2]] < distmat[fpop[b][-1]][fpop[b][-2]] or (fpop[b][-2] in unv) == False:
                b = k
        if (fpop[b][-2] in unv) == False:
            q = random.choice(unv)
        else:
            q = fpop[b][-2]
        unv.remove(q)
        new2[i] = q
    return new2


# 交叉函数,顺序交叉
def GASA_cross1(ans1, ans2, n):
    new1 = [0] * n
    new2 = [0] * n
    x = random.randint(0, n - 1)
    y = random.randint(0, n - 1)
    if x < y:  # 子代1
        new1[x:y + 1] = ans1[x:y + 1].copy()
    else:
        new1[y:x + 1] = ans1[y:x + 1].copy()
    j = 0
    for i in range(n):
        if (new1[i] != 0):
            continue
        else:
            while (ans2[j] in new1):
                j += 1
            new1[i] = ans2[j]
            j += 1
    x = random.randint(0, n - 1)
    y = random.randint(0, n - 1)
    if x < y:  # 子代2
        new2[x:y + 1] = ans2[x:y + 1]
    else:
        new2[y:x + 1] = ans2[y:x + 1]
    i = 0
    j = 0
    for i in range(n):
        if (new2[i] != 0):
            continue
        else:
            while (ans1[j] in new2):
                j += 1
            new2[i] = ans1[j]
            j += 1
    return np.array(new1), np.array(new2)


# 部分映射交叉
def GASA_cross2(ans1, ans2, n):
    new1 = [0] * n
    new2 = [0] * n
    new1 = list(ans1)
    new2 = list(ans2)
    x = random.randint(0, n - 1)
    y = random.randint(0, n - 1)
    while x == y:
        x = random.randint(0, n - 1)
    l1 = []
    l2 = []
    if x < y:  # 子代1
        new1[x:y + 1] = ans2[x:y + 1]
        new2[x:y + 1] = ans1[x:y + 1]
        for i in range(x, y + 1):
            if (ans1[i] in ans2[x:y + 1]):
                continue
            l1.append(ans1[i])
        for i in range(x, y + 1):
            if (ans2[i] in ans1[x:y + 1]):
                continue
            l2.append(ans2[i])
        d1 = dict(zip(l1, l2))
        d2 = dict(zip(l2, l1))
        for i in range(n):
            if i >= x and i <= y:
                continue
            if d2.__contains__(new1[i]) == True:
                new1[i] = d2[new1[i]]
            if d1.__contains__(new2[i]) == True:
                new2[i] = d1[new2[i]]
    else:
        new1[y:x + 1] = ans2[y:x + 1]
        new2[y:x + 1] = ans1[y:x + 1]
        for i in range(y, x + 1):
            if (ans1[i] in ans2[y:x + 1]):
                continue
            l1.append(ans1[i])
        for i in range(y, x + 1):
            if (ans2[i] in ans1[y:x + 1]):
                continue
            l2.append(ans2[i])
        d1 = dict(zip(l1, l2))
        d2 = dict(zip(l2, l1))
        for i in range(n):
            if i >= y and i <= x:
                continue
            if d2.__contains__(new1[i]) == True:
                new1[i] = d2[new1[i]]
            if d1.__contains__(new2[i]) == True:
                new2[i] = d1[new2[i]]
    return np.array(new1), np.array(new2)


# 部分位置交叉
def GASA_cross3(ans1, ans2, n):
    new1 = [0] * n
    new2 = [0] * n
    l1 = list(range(0, n))
    random.shuffle(l1)
    for i in range(n // 2):
        new1[l1[i]] = ans1[l1[i]]
    j = 0
    for i in range(n):
        if (new1[i] != 0):
            continue
        else:
            while (ans2[j] in new1):
                j += 1
            new1[i] = ans2[j]
            j += 1
    l1 = list(range(0, n))  # 子代2
    random.shuffle(l1)
    for i in range(n // 2):
        new2[l1[i]] = ans2[l1[i]]
    j = 0
    for i in range(n):
        if (new2[i] != 0):
            continue
        else:
            while (ans1[j] in new2):
                j += 1
            new2[i] = ans1[j]
            j += 1
    return np.array(new1), np.array(new2)


def GASA_cross(pop_value, pop_path, n1, distmat, N):
    a = random.randint(0, N - 1)
    b = random.randint(0, N - 1)
    while a == b:
        a = random.randint(0, N - 1)
    z = random.randint(0, 3)
    if (z == 0):
        ff = np.zeros((2, n1)).astype(int)
        ff[0] = pop_path[a].copy()
        ff[1] = pop_path[b].copy()
        t1, t2 = GASA_cross1(pop_path[a], pop_path[b], n1)
        return t1, t2, ff
    elif (z == 1):
        ff = np.zeros((2, n1)).astype(int)
        ff[0] = pop_path[a].copy()
        ff[1] = pop_path[b].copy()
        t1, t2 = GASA_cross2(pop_path[a], pop_path[b], n1)
        return t1, t2, ff
    elif (z == 2):
        ff = np.zeros((2, n1)).astype(int)
        ff[0] = pop_path[a].copy()
        ff[1] = pop_path[b].copy()
        t1, t2 = GASA_cross3(pop_path[a], pop_path[b], n1)
        return t1, t2, ff
    else:
        ff = GASA_threecross(pop_value, pop_path, n1)
        t1 = son1(ff, n1, distmat)
        t2 = son2(ff, t1[0], n1, distmat)
        return t1, t2, ff


# 初始化
def GASA_init(N, n, pop):
    for i in range(N):
        pop[i] = np.random.permutation(range(1, n + 1))


# 计算种群适应值
def GASA_value(pop, popvalue, distmat, weight, things):
    for i in range(len(pop)):
        popvalue[i] = value_function(distmat, list(pop[i]), weight, things)


# 更新种群最优解
def GASA_update_pop(pop, popvalue, bpop, bvalue):
    for i in range(len(popvalue)):
        if popvalue[i] < bvalue:
            bpop = pop[i].copy()
            bvalue = popvalue[i]
            bol = True
    return bpop, bvalue


# 变异函数，随机变换一个位置
def mutate(n, path, mutate_rate):
    temp = path.copy()
    rate = random.random()
    if (rate < mutate_rate):
        x = random.randint(0, n - 1)
        y = random.randint(0, n - 1)
        while x == y:
            x = random.randint(0, n - 1)
        temp[x], temp[y] = temp[y], temp[x]
    return temp


# 退火选择
def GASA_SA_choice(fpop, s1, s2, distmat, weight, things, T):
    f1 = value_function(distmat, list(fpop[0]), weight, things)
    f2 = value_function(distmat, list(fpop[1]), weight, things)
    v1 = value_function(distmat, list(s1), weight, things)
    v2 = value_function(distmat, list(s2), weight, things)
    if v1 <= f1:
        tp1 = s1.copy()
    elif (random.random() < math.exp((f1 - v1) / T)):
        tp1 = s1.copy()
    else:
        tp1 = fpop[0].copy()
    if v2 <= f2:
        tp2 = s2.copy()
    elif (random.random() < math.exp((f2 - v2) / T)):
        tp2 = s2.copy()
    else:
        tp2 = fpop[1].copy()
    return tp1, tp2


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


class GASA(object):
    def __init__(self, Tmax=50, Tmin=1e-2, t=0.9, L=50, \
                 maxgen=50, mutate_rate=0.1, N=50):
        self.T = Tmax
        self.T_end = Tmin
        self.t = t
        self.L = L
        self.maxgen = maxgen
        self.mutate_rate = mutate_rate
        self.N = N  # 种群中个体数

    def GASA_solver(self, spath):
        path = copy.deepcopy(spath)
        distmat = copy.deepcopy(VRPLibReader.distmat)
        things = copy.deepcopy(VRPLibReader.things)
        weight = copy.deepcopy(VRPLibReader.capacity)
        gen = 0
        n = distmat.shape[0] - 1  # 需求地数
        pop_value = np.zeros(self.N)  # 种群每个个体适应值
        pop_path = np.zeros((self.N, n)).astype(int)  # 种群每个个体解
        for i in path:
            del i[0]
            del i[-1]
        path = [x for j in path for x in list(j)]
        bestpath = path.copy()
        bestvalue = value_function(distmat, bestpath, weight, things)
        new_pop = np.zeros((self.N, n)).astype(int)

        GASA_init(self.N, n, pop_path)
        GASA_value(pop_path, pop_value, distmat, weight, things)
        bestpath, bestvalue = GASA_update_pop(pop_path, pop_value, bestpath, bestvalue)
        yc = 0
        judge = 1
        while gen < self.maxgen and judge:
            while (True):
                for i in range(0, self.N, 2):
                    new1, new2, father_pop = GASA_cross(pop_value, pop_path, n, distmat, self.N)
                    s_1, s_2 = GASA_SA_choice(father_pop, new1, new2, distmat, weight, things, self.T)
                    s_1 = mutate(n, s_1, self.mutate_rate)
                    s_2 = mutate(n, s_2, self.mutate_rate)
                    new_pop[i], new_pop[i + 1] = s_1.copy(), s_2.copy()
                pop_path = new_pop.copy()
                gen += 1
                self.T *= self.t
                GASA_value(pop_path, pop_value, distmat, weight, things)
                if np.min(pop_value) >= bestvalue:
                    yc += 1
                else:
                    yc = 0
                    bestvalue = np.min(pop_value)
                    bestpath = pop_path[list(pop_value).index(bestvalue)].copy()
                if yc == 5 or self.T < self.T_end or gen > self.maxgen:
                    judge = 0
                    break
                else:
                    continue
        sa = SA(self.T, self.T_end, self.t, self.L)
        fp, tbest = sa.SA_solver(bestpath, 0)
        finalpath = []
        w = 0  # 计算载货量
        i = 0
        j = len(fp)
        tt = [0]
        while (i < j):
            if (w + things[fp[i]] > weight):
                tt.append(0)
                finalpath.append(tt)
                tt = [0]
                w = things[fp[i]]
                tt.append(fp[i])
            else:
                w = w + things[fp[i]]
                tt.append(fp[i])
            i += 1
        if tt != [] or tt != [0]:
            tt.append(0)
            finalpath.append(tt)
        return finalpath, tbest
