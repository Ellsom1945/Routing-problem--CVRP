# 改进遗传:四种交叉方式—改进退火
import random
import numpy as np
import math


# 初始化
def init(N, n, pop):
    for i in range(N):
        pop[i] = np.random.permutation(range(1, n + 1))


# 适应度函数
def va(distmat, list1, maxlength, weight, things):
    s = 0
    w = weight
    ml = maxlength
    tlist = list(list1)
    tlist.insert(0, 0)
    for i in range(0, len(tlist) - 1):
        w = w - things[tlist[i + 1]]
        ml = ml - distmat[tlist[i]][tlist[i + 1]]
        if (w < 0 or ml - distmat[tlist[i + 1]][0] < 0):  # 已超过最大运输距离或货物不足，返回
            s += distmat[tlist[i]][0] + distmat[0][tlist[i + 1]]
            w = weight - things[tlist[i + 1]]
            ml = maxlength - distmat[0][tlist[i + 1]]
        else:
            # 计算到K城市的距离
            s += distmat[tlist[i]][tlist[i + 1]]
    s += distmat[tlist[-1]][0]
    return s


# 计算适应值
def value(pop, popvalue, distmat, maxlength, weight, things):
    for i in range(len(pop)):
        popvalue[i] = va(distmat, list(pop[i]), maxlength, weight, things)


# 更新种群最优解
def update_pop(pop, popvalue, bpop, bvalue):
    for i in range(len(popvalue)):
        if popvalue[i] < bvalue:
            bpop = pop[i].copy()
            bvalue = popvalue[i]
            bol = True
    return bpop, bvalue


# 三交叉算子
def threecross(popva, poppath, n):
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
def right_rotation(i, path, n):
    j = list(path).index(i)
    temppath = np.zeros(n).astype(int)
    temppath[:n - j] = path[j:]
    temppath[n - j:] = path[:j]
    return temppath


# 左轮变换
def left_rotation(i, path, n):
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
            fpop[k] = right_rotation(q, fpop[k], n)
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
            fpop[k] = left_rotation(q, fpop[k], n)
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
def cross1(ans1, ans2, n):
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
def cross2(ans1, ans2, n):
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
def cross3(ans1, ans2, n):
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


def cross(pop_value, pop_path, n1, distmat, N):
    a = random.randint(0, N - 1)
    b = random.randint(0, N - 1)
    while a == b:
        a = random.randint(0, N - 1)
    z = random.randint(0, 3)
    if (z == 0):
        ff = np.zeros((2, n1)).astype(int)
        ff[0] = pop_path[a].copy()
        ff[1] = pop_path[b].copy()
        t1, t2 = cross1(pop_path[a], pop_path[b], n1)
        return t1, t2, ff
    elif (z == 1):
        ff = np.zeros((2, n1)).astype(int)
        ff[0] = pop_path[a].copy()
        ff[1] = pop_path[b].copy()
        t1, t2 = cross2(pop_path[a], pop_path[b], n1)
        return t1, t2, ff
    elif (z == 2):
        ff = np.zeros((2, n1)).astype(int)
        ff[0] = pop_path[a].copy()
        ff[1] = pop_path[b].copy()
        t1, t2 = cross3(pop_path[a], pop_path[b], n1)
        return t1, t2, ff
    else:
        ff = threecross(pop_value, pop_path, n1)
        t1 = son1(ff, n1, distmat)
        t2 = son2(ff, t1[0], n1, distmat)
        return t1, t2, ff


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
def sa_choice(fpop, s1, s2, distmat, maxlength, weight, things, T):
    f1 = va(distmat, list(fpop[0]), maxlength, weight, things)
    f2 = va(distmat, list(fpop[1]), maxlength, weight, things)
    v1 = va(distmat, list(s1), maxlength, weight, things)
    v2 = va(distmat, list(s2), maxlength, weight, things)
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


# 产生新解——逆序
def ch1(tpath):
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
def ch2(tpath):
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
def ch3(tpath):
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
def ch4(tpath):
    x = random.randint(0, len(tpath) - 1)
    y = random.randint(0, len(tpath) - 1)
    while x == y:
        x = random.randint(0, len(tpath) - 1)
    tpath[x], tpath[y] = tpath[y], tpath[x]
    return tpath


# 产生新解
def change(tpath):
    i = random.randint(1, 4)
    c = []
    if i == 1:
        c = ch1(tpath)
    elif i == 2:
        c = ch2(tpath)
    elif i == 3:
        c = ch3(tpath)
    else:
        c = ch4(tpath)
    return c


# 退火算法
def sa(distmat, maxlength, weight, things, T, Tmin, t, bpath, bvalue):
    L = 300  # 链长
    n = distmat.shape[0] - 1
    temp1 = list(bpath).copy()  # 初解
    temp3 = temp1.copy()
    tpath = list(bpath).copy()  # 最佳路径
    tbest = bvalue  # 最佳总长度
    th = 0
    while T > Tmin:
        z = L
        while z > 0:
            z -= 1
            temp2 = list(temp1)
            temp2 = change(temp2)  # 扰动解
            t1 = va(distmat, temp1, maxlength, weight, things)
            t2 = va(distmat, temp2, maxlength, weight, things)
            if (t1 > t2):
                temp1 = list(temp2)
                if (t2 < tbest):
                    tpath = temp2.copy()
                    tbest = t2
                continue
            p = math.exp((t1 - t2) / T)
            if (random.random() < p):
                temp1 = list(temp2)
        T *= t
        if (temp3 == temp1):
            th += 1
        else:
            th = 0
            temp3 = temp1.copy()
        if th == 5 or tbest < 821:
            break

    tpath.insert(0, 0)
    newpath = [0]
    w = 0  # 计算载货量
    h = 0  # 计算累计距离
    i = 1
    j = len(tpath)
    while (i < j):
        if (w + things[tpath[i]] > weight or h + distmat[tpath[i]][0] + distmat[tpath[i - 1]][tpath[i]] > maxlength):
            newpath.append(0)
            w = things[tpath[i]]
            h = distmat[0][tpath[i]]
        else:
            w = w + things[tpath[i]]
            h = h + distmat[tpath[i - 1]][tpath[i]]
        newpath.append(tpath[i])
        i += 1
    return newpath, tbest


def GA_SA2(distmat, things, maxlength, weight, a):
    gen = 0
    maxgen = 3000
    mutate_rate = 0.1
    Tmin = 1e-4  # 终止温度
    t = 0.98  # 降温系数
    L = 300  # 链长
    N = 50  # 种群中个体数
    n = a  # 需求地数
    pop_value = np.zeros(N)  # 种群每个个体适应值
    pop_path = np.zeros((N, n)).astype(int)  # 种群每个个体解
    bestpath = np.zeros(n).astype(int)
    bestvalue = a * 10000
    T = 500  # 初始温度
    new_pop = np.zeros((N, n)).astype(int)

    init(N, n, pop_path)
    value(pop_path, pop_value, distmat, maxlength, weight, things)
    bestpath, bestvalue = update_pop(pop_path, pop_value, bestpath, bestvalue)
    yc = 0
    judge = 1
    while gen < maxgen and judge:
        while (True):
            for i in range(0, N, 2):
                new1, new2, father_pop = cross(pop_value, pop_path, n, distmat, N)
                s_1, s_2 = sa_choice(father_pop, new1, new2, distmat, maxlength, weight, things, T)
                s_1 = mutate(n, s_1, mutate_rate)
                s_2 = mutate(n, s_2, mutate_rate)
                new_pop[i], new_pop[i + 1] = s_1.copy(), s_2.copy()
            pop_path = new_pop.copy()
            gen += 1
            T *= t
            value(pop_path, pop_value, distmat, maxlength, weight, things)
            if np.min(pop_value) >= bestvalue:
                yc += 1
            else:
                yc = 0
                bestvalue = np.min(pop_value)
                bestpath = pop_path[list(pop_value).index(bestvalue)].copy()
            if yc == 5 or T < Tmin or gen > maxgen:
                judge = 0
                break
            else:
                continue
    newpath, tbest = sa(distmat, maxlength, weight, things, T, Tmin, t, bestpath, bestvalue)
    return newpath, tbest
