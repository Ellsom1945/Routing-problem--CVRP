# 前提:一个供应地（供应量无限），每个需求地有且仅去一次
# 设置车辆载重量以及车辆的最大行驶距离
# 影响算法效率的因素：信息素重要程度因子，启发函数重要程度因子，信息素的挥发速度
# 迭代总数,蚂蚁个数，信息素常数
import datetime
import numpy as np
from numpy import random
import random
import math
import Greedy
from H_Hy_Men import TABU, VRPLibReader


def random_pick(some_list, probabilities):
    x = random.uniform(0, 1)
    cumulative_probability = 0.0
    for item, item_probability in zip(some_list, probabilities):
        cumulative_probability += item_probability
        if x < cumulative_probability:
            break
    return item


# 代价函数
def value(a):
    s = 0
    for i in range(len(a) - 1):
        s += VRPLibReader.distmat[a[i]][a[i + 1]]
    return s


# 蚁群算法
def aco_1(distmat, things, weight, a):
    numant = 20  # 蚂蚁个数
    numplace = a + 1  # 需求地个数加上起点
    alpha = 1  # 信息素重要程度因子
    beta = 2  # 启发函数重要程度因子
    rho = 0.2  # 信息素的挥发速度
    iter = 0  # 迭代初始
    itermax = 100  # 迭代总数
    # 启发矩阵 diag将对角元素设为1e10 表示从i到j的期望值
    etatable = 1.0 / (distmat + np.diag([1e10] * numplace))
    # 信息素矩阵
    pheromonetable = np.ones((numplace, numplace))  # 构造全一矩阵
    visitingfreq = np.ones((numplace, numplace)).astype(int)
    antipheromonetable = np.ones((numplace, numplace))
    lengthbest = np.zeros(itermax)  # 各代及其之前的最佳路径长度
    pathbest = Greedy.num
    lengthbest[0] = Greedy.total_cost
    t0 = 1 / lengthbest[0] * (a + 1)  # 信息素常数
    # lengthbest[0] = TABU.tabu_solver()[0]
    pathbest = TABU.tabu_solver()[2]
    pics = []
    for s in range(len(pathbest) - 1):
        pheromonetable[pathbest[s]][pathbest[s + 1]] = pheromonetable[pathbest[s]][
                                                           pathbest[s + 1]] * (1+math.log(a,10)*0.03)
    start_time = datetime.datetime.now()
    while iter < itermax:
        thta = iter // 10 + 5
        pic = np.zeros((numplace, numplace)).astype(int)
        r0 = 0.6 + iter / (iter + itermax * 4)
        tabutable = []
        lengthtable = np.zeros(numant)
        antload = np.zeros(numant)
        # 将蚂蚁随机放置在第一个需求点
        for i in range(numant):
            listunvisited = list(range(1, numplace))
            probtrans = np.zeros(len(listunvisited))
            for k in range(len(listunvisited)):
                probtrans[k] = \
                    np.power(pheromonetable[0][listunvisited[k]], alpha) \
                    * np.power(etatable[0][listunvisited[k]], beta) * antipheromonetable[0][
                        listunvisited[k]]
            cumsumprobtrans = (probtrans / sum(probtrans))
            if np.random.rand() > r0:
                k = random_pick(listunvisited, cumsumprobtrans)
            else:
                k = listunvisited[np.argmax(probtrans)]
            tabutable.insert(i, [k])
            listunvisited.remove(k)
            antload[i] = things[k]
            pic[0][k] += 1
            pheromonetable[0][k] = (1 - rho) * pheromonetable[0][k] + rho * t0
            visiting = k
            lengthtable[i] += distmat[0][visiting]
            while len(listunvisited) != 0:  # 逐个选择下一个地点
                wl = np.ones(len(listunvisited))
                for j in range(len(wl)):
                    if antload[i] + things[listunvisited[j]] > weight:
                        wl[j] = 0
                probtrans = np.zeros(len(listunvisited))
                # 求出本只蚂蚁的转移到各个地点的概率数列
                for k in range(len(listunvisited)):  # O(n^2)
                    probtrans[k] = \
                        pheromonetable[visiting][listunvisited[k]] \
                        * np.power(etatable[visiting][listunvisited[k]], beta) * antipheromonetable[visiting][
                            listunvisited[k]] * wl[k]
                if np.all(probtrans) == 0 or len(probtrans) == 0:
                    tabutable[i].append(0)
                    antload[i] = 0
                    lengthtable[i] += distmat[0][visiting]
                    visiting = 0
                else:
                    cumsumprobtrans = (probtrans / sum(probtrans))
                    if (np.random.rand() > r0):
                        k = random_pick(listunvisited, cumsumprobtrans)
                    else:
                        k = listunvisited[np.argmax(probtrans)]
                    tabutable[i].append(k)
                    listunvisited.remove(k)
                    antload[i] += things[k]
                    lengthtable[i] += distmat[k][visiting]
                    pic[visiting][k] += 1
                    pheromonetable[visiting][k] = (1 - rho) * pheromonetable[visiting][k] + rho * t0
                    pheromonetable[k][visiting] = (1 - rho) * pheromonetable[k][visiting] + rho * t0
                    visiting = k
            lengthtable[i] += distmat[0][visiting]
        # 2-opt局部优化
        MAXCOUNT = 100
        tem = []
        temps = []
        for z in tabutable[np.argmin(lengthtable)]:
            if z != 0:
                tem.append(z)
            else:
                a = []
                for j in tem:
                    a.append(j)
                temps.append(a)
                tem.clear()
        temps.append(tem)
        for z in temps:
            z.insert(0, 0)
        newtabu = []
        for i in temps:
            city = []
            for z in i:
                city.append(VRPLibReader.site[z])
            cities = np.array(city)

            def calDist(xindex, yindex):
                return (np.sum(np.power(cities[xindex] - cities[yindex], 2))) ** 0.5

            def calPathDist(indexList):
                sum = 0.0
                for i in range(1, len(indexList)):
                    sum += calDist(indexList[i], indexList[i - 1])
                return sum

            # path1长度比path2短则返回true
            def pathCompare(path1, path2):
                if calPathDist(path1) <= calPathDist(path2):
                    return True
                return False

            def generateRandomPath(bestPath):
                a = np.random.randint(len(bestPath))
                while True:
                    b = np.random.randint(len(bestPath))
                    if np.abs(a - b) > 1:
                        break
                if a > b:
                    return b, a, bestPath[b:a + 1]
                else:
                    return a, b, bestPath[a:b + 1]

            def reversePath(path):
                rePath = path.copy()
                rePath[1:-1] = rePath[-2:0:-1]
                return rePath

            def updateBestPath(bestPath):
                count = 0
                while count < MAXCOUNT and len(bestPath) > 3:
                    start, end, path = generateRandomPath(bestPath)
                    rePath = reversePath(path)

                    if pathCompare(path, rePath):
                        count += 1
                        continue

                    else:
                        count = 0
                        bestPath[start:end + 1] = rePath
                return bestPath

            def opt2():
                # 随便选择一条可行路径
                bestPath = np.arange(0, len(cities))
                bestPath = np.append(bestPath, 0)
                bestPath = updateBestPath(bestPath)
                return bestPath

            ttt = opt2().tolist()
            aaa = []
            for j in range(1, len(ttt)):
                aaa.append(i[ttt[j]])
            bbb = aaa * 2
            a = 0
            while bbb[a] != 0:
                a += 1
            newtabu.append(0)

            a += 1
            while bbb[a] != 0:
                newtabu.append(bbb[a])
                a += 1
                if a == len(bbb):
                    break
        newtabu.append(0)
        newlen = value(newtabu)
        # 选出最佳路径
        if iter == 0:
            if lengthbest[iter] > newlen:
                lengthbest[iter] = newlen
                pathbest = newtabu
        else:
            if newlen >= lengthbest[iter - 1]:
                lengthbest[iter] = lengthbest[iter - 1]
            else:
                lengthbest[iter] = newlen
                pathbest = newtabu
        # 更新信息素
        if iter > 1:
            changepheromonetable = rho * (lengthbest[iter - 1] - newlen) / lengthbest[iter - 1]
            for s in range(len(pathbest) - 1):
                pheromonetable[pathbest[s]][pathbest[s + 1]] = pheromonetable[pathbest[s]][
                                                                   pathbest[s + 1]] * (1 - rho) + changepheromonetable
                visitingfreq[pathbest[s]][pathbest[s + 1]] += 1
        # 更新负信息素
        antipheromonetable = thta / visitingfreq
        print(lengthbest[iter])
        pics.append(pic)
        iter += 1
    end_time = datetime.datetime.now()
    print('算法时间:', end_time - start_time)
    print(pathbest, lengthbest[-1])
    return pics


pics = aco_1(VRPLibReader.distmat, VRPLibReader.things, VRPLibReader.capacity, VRPLibReader.n - 1)
# for i in pics:
#     plt.matshow(i)
# plt.show()
