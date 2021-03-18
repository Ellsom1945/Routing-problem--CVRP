import numpy as np
from H_Hy_Men import VRPLibReader


# 计算两点之间距离
def distance(t1, t2):
    return np.sum((t1 - t2) ** 2)


# 计算当前各个中心点中离给定点最近的一个
def classify(p, centers):
    t = [distance(p, centers[i]) for i in range(len(centers))]
    index = np.argmin(t)
    return index


# 将每个点归入到离它最近的中心点类别
def category(X, categories, centers, ts, il, spt):
    temp = list(centers).copy()
    for i in range(len(X)):
        if i in il:
            continue
        index = classify(X[i], temp)
        while ts[index] + VRPLibReader.things[i + 1] > VRPLibReader.capacity:
            del temp[index]
            if temp == []:
                return 0
            index = classify(X[i], temp)
        temp = list(centers).copy()
        ts[index] += VRPLibReader.things[i + 1]
        spt[index].insert(-1, i + 1)
        categories[index].append(X[i])  # 将pt纳入离它最近的中心点类别下
    return 1


site = list(VRPLibReader.site)
del site[0]
site = np.array(site)
M = VRPLibReader.n - 1
K = VRPLibReader.carnum
sp = []
max_iter = 5 # 序列数
def one_two(path):
    tem = []
    temps = []
    for i in path:
        if (i != 0):
            tem.append(i)
        else:
            a = []
            for j in tem:
                a.append(j)
            if len(a) > 0:
                temps.append(a)
            tem.clear()
    for i in temps:
        i.append(0)
        i.insert(0, 0)
    return temps

iter = 0
while iter < max_iter:
    categories = [[] for i in range(K)]
    # 随机选择K个中心点作为初始点
    init_indecies = np.random.randint(0, M, K)
    centers = site[init_indecies]
    spt = [[0, init_indecies[i] + 1, 0] for i in range(K)]
    ts = [[VRPLibReader.things[init_indecies[i] + 1]] for i in range(len(init_indecies))]
    ju = category(site, categories, centers, ts, init_indecies, spt)  # 计算分类
    if ju == 0:
        continue
    sp.append(spt)
    iter += 1
# sp.append([[0,58, 32, 4, 22, 45, 50, 76, 33, 72,0], [0,75, 57, 26, 35, 65, 47, 19, 20, 56, 64, 69,0], [0,34, 2, 37, 8, 68, 43, 16, 61, 78, 30,0], [0,52, 28, 79, 18, 48, 14, 71,0], [0,15, 55, 9, 54, 25, 38, 41, 46,0], [0,42, 53, 66, 67, 36, 73, 49, 70,0], [0,17, 31, 27, 59, 5, 44, 12, 62,0], [0,51, 77, 3, 39, 60, 74, 13,0], [0,23, 6, 24, 11, 63, 10,0], [0,1, 7, 21, 40, 29,0]])
sp.append(one_two([0, 1, 28, 47, 9, 17, 48, 32, 23, 0, 31, 27, 35, 18, 40, 44, 26, 29, 49, 36, 7, 50, 19, 0, 51, 8, 46, 10, 37, 0, 4, 22, 30, 2, 43, 42, 0, 39, 3, 14, 34, 52, 11, 24, 41, 0, 25, 5, 21, 13, 12, 16, 15, 0, 20, 6, 38, 33, 45, 0]))
a=1
