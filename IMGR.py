import VRPLibReader
import datetime
import math
import matplotlib.pyplot as plt
import numpy as np
import TABU

distmat = VRPLibReader.distmat
dimension = VRPLibReader.n
depot = VRPLibReader.site[0]
sites = VRPLibReader.site
cap = VRPLibReader.capacity
visited = np.zeros((dimension, dimension))
flag = np.zeros((dimension, dimension))
supply = VRPLibReader.things
finished = np.zeros(dimension)
finished[0] = 1


def value(a, distmat):
    s = 0
    for i in range(len(a) - 1):
        s += distmat[a[i]][a[i + 1]]
    return s


def find(a, b):
    for i in range(a.shape[0]):
        if np.sum(a[i, :] == b) == b.size:
            return i


def createKDTree(dataSet, depth):
    n = np.shape(dataSet)[0]
    treeNode = {}
    if n == 0:
        return None
    else:
        n, m = np.shape(dataSet)
        split_axis = depth % m
        depth += 1
        treeNode['split'] = split_axis
        dataSet = np.array(sorted(dataSet, key=lambda a: a[split_axis]))
        num = n // 2
        treeNode['median'] = dataSet[num]
        treeNode['left'] = createKDTree(dataSet[:num], depth)
        treeNode['right'] = createKDTree(dataSet[num + 1:], depth)
        # treeNode['number'] = int(np.where((VRPLibReader.site == dataSet[num]).all(1))[0])
        treeNode['number'] = find(VRPLibReader.site, dataSet[num])
        return treeNode


def searchTree(tree, i):
    data = sites[i]
    k = len(data)
    if tree is None:
        return [0] * k, float('inf'), 0
    split_axis = tree['split']
    median_point = tree['median']
    num = tree['number']
    if data[split_axis] <= median_point[split_axis]:
        nearestPoint, nearestDistance, nearestnum = searchTree(tree['left'], i)
    else:
        nearestPoint, nearestDistance, nearestnum = searchTree(tree['right'], i)
    nowDistance = np.linalg.norm(data - median_point)
    if nearestDistance > nowDistance > 0 and flag[i][num] == 0 and flag[num][i] == 0 and finished[num] == 0:
        nearestnum = num
        nearestDistance = nowDistance
        nearestPoint = median_point.copy()
    splitDistance = abs(data[split_axis] - median_point[split_axis])
    if splitDistance > nearestDistance > 0:
        return nearestPoint, nearestDistance, nearestnum
    else:
        if data[split_axis] <= median_point[split_axis]:
            nextTree = tree['right']
        else:
            nextTree = tree['left']
        nearPoint, nearDistance, nearnum = searchTree(nextTree, i)
        if nearestDistance > nearDistance > 0 and flag[i][nearnum] == 0 and flag[nearnum][i] == 0 and finished[
            num] == 0:
            nearestnum = nearnum
            nearestDistance = nearDistance
            nearestPoint = nearPoint.copy()
        return nearestPoint, nearestDistance, nearestnum


class ZHeap:
    def __init__(self, item=[]):
        # 初始化。item为数组
        self.items = item
        self.heapsize = len(self.items)

    def LEFT(self, i):
        return 2 * i + 1

    def RIGHT(self, i):
        return 2 * i + 2

    def PARENT(self, i):
        return (i - 1) / 2

    def MIN_HEAPIFY(self, i):
        # 最小堆化：使以i为根的子树成为最小堆
        l = self.LEFT(i)
        r = self.RIGHT(i)
        if l < self.heapsize and self.items[l][2] < self.items[i][2]:
            smallest = l
        else:
            smallest = i

        if r < self.heapsize and self.items[r][2] < self.items[smallest][2]:
            smallest = r

        if smallest != i:
            self.items[i], self.items[smallest] = self.items[smallest], self.items[i]
            self.MIN_HEAPIFY(smallest)

    def INSERT(self, val):
        # 插入一个值val，并且调整使满足堆结构
        self.items.append(val)
        idx = len(self.items) - 1
        parIdx = int(self.PARENT(idx))
        while parIdx >= 0:
            if self.items[parIdx][2] > self.items[idx][2]:
                self.items[parIdx], self.items[idx] = self.items[idx], self.items[parIdx]
                idx = parIdx
                parIdx = int(self.PARENT(parIdx))
            else:
                break
        self.heapsize += 1

    def DELETE(self, i):
        last = len(self.items) - 1
        if last < 0:
            return None
        self.items[i], self.items[last] = self.items[last], self.items[i]
        val = self.items.pop()
        self.heapsize -= 1
        self.MIN_HEAPIFY(i)
        return val

    def BUILD_MIN_HEAP(self):
        # 建立最小堆, O(nlog(n))
        i = self.PARENT(len(self.items) - 1)
        while i >= 0:
            self.MIN_HEAPIFY(i)
            i -= 1

    def SHOW(self):
        print(self.items)


class ZPriorityQ(ZHeap):
    def __init__(self, item=[]):
        ZHeap.__init__(self, item)

    def insert(self, val):
        ZHeap.INSERT(self, val)

    def delete(self, i):
        val = ZHeap.DELETE(self, i)
        return val


def suit(edge):
    if finished[edge[1]] == 1 or finished[edge[0]] == 1:
        return False
    if visited[edge[0]].sum() < 2 and visited[edge[1]].sum() < 2:
        if visited[edge[0]].sum() + visited[edge[1]].sum() <= 1:
            return True
    return False


start_time = datetime.datetime.now()
tree_depth = int(math.log10(dimension) - 2)
KD_Tree = createKDTree(sites[1:], tree_depth)
PAI = []
for i in range(len(distmat)):
    PAI.append(0 * distmat[0][i]*(1-supply[i]/supply.sum()))
    distmat[i][i] = float('inf')
for i in range(len(distmat)):
    for j in range(len(distmat)):
        distmat[i][j] += (PAI[i] + PAI[j])
temp = []
for i in range(1, len(distmat)):
    a = searchTree(KD_Tree, i)[2]
    flag[i][a] = flag[a][i] = 1
    temp.append([i, a, distmat[i][a]])
Min_Priority = ZPriorityQ()
for i in temp:
    Min_Priority.insert(i)
paths = []
while len(Min_Priority.items) != 0:
    weight = 0
    path = []
    i = 0
    while weight < cap:
        if i >= len(Min_Priority.items):
            break
        edge = Min_Priority.items[i]
        if edge:
            if suit(edge):
                if weight + supply[edge[0]] * (1 - visited[edge[0]].sum()) + supply[edge[1]] * (
                        1 - visited[edge[1]].sum()) <= cap:
                    if visited[edge[0]].sum() == 0:
                        weight += supply[edge[0]]
                    if visited[edge[1]].sum() == 0:
                        weight += supply[edge[1]]
                    path.append(edge[:2])
                    visited[edge[0]][edge[1]] += 1
                    visited[edge[1]][edge[0]] += 1
                    Min_Priority.delete(i)
                    if visited[edge[0]].sum() < 2 and flag[edge[0]].sum() < dimension - 2:
                        a = searchTree(KD_Tree, edge[0])[2]
                        flag[edge[0]][a] = flag[a][edge[0]] = 1
                        Min_Priority.insert([edge[0], a, distmat[edge[0]][a]])
                else:
                    i += 1
            else:
                Min_Priority.delete(i)
                if visited[edge[0]].sum() < 2 and flag[edge[0]].sum() < dimension - 2:
                    a = searchTree(KD_Tree, edge[0])[2]
                    if a == 0:
                        break
                    flag[edge[0]][a] = flag[a][edge[0]] = 1
                    Min_Priority.insert([edge[0], a, distmat[edge[0]][a]])
    for i in path:
        visited[i[0]][0] = 1
        visited[i[1]][0] = 1
        finished[i[0]] = finished[i[1]] = 1
        flag[i[0]] = 1
    if path:
        paths.append(path)
c = 0
path = []
while finished.all != 1:
    while finished[c] == 1:
        c += 1
        if c==len(finished):
            break
    if c != len(finished):
        finished[c]=1
        path.append([c, 0])
    if c == len(finished):
        paths.append(path)
        break
end_time = datetime.datetime.now()


class Customer:

    def __init__(self, num, demand):
        self.num = num
        self.demand = demand
        self.is_visited = False


class UAV:

    def __init__(self, cap):
        self.cap = cap
        self.load = 0
        self.routes = []
        self.current_location = 0

    def check_if_fit(self, demand):
        return self.load + demand <= self.cap

    def transport(self, cus):
        self.routes.append(cus)
        self.load += cus.demand
        self.current_location = cus.num


realpath = []
temp = np.zeros(dimension)
for i in paths:
    tem = [0, ]
    for j in i:
        if not temp[j[0]]:
            tem.append(j[0])
            temp[j[0]] = 1
        if not temp[j[1]]:
            temp[j[1]] = 1
            tem.append(j[1])
    realpath.extend(tem)
print(realpath)
print('算法时间:', end_time - start_time)
MAXCOUNT = 1000
tem = []
temps = []
while realpath[0] == 0:
    del realpath[0]
while realpath[len(realpath) - 1] == 0:
    del realpath[len(realpath) - 1]
for z in realpath:
    if (z != 0):
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
newlen = value(newtabu, VRPLibReader.getdistmat(VRPLibReader.site))
print("newpath", newtabu)
print("newlen", newlen)
num = newtabu
total_cost = newlen
while num[0] == 0:
    del num[0]
while num[len(num) - 1] == 0:
    del num[len(num) - 1]
t1 = []
temp_arr = []
for i in num:
    if i != 0:
        t1.append(i)
    else:
        a = []
        for j in t1:
            a.append(j)
        temp_arr.append(a)
        t1.clear()
temp_arr.append(t1)
for i in temp_arr:
    i.append(0)
    i.insert(0, 0)
uavs = []
for i in range(len(temp_arr)):
    uavs.append(UAV(VRPLibReader.capacity))
for i in range(len(temp_arr)):
    for j in temp_arr[i]:
        aaa = Customer(j, VRPLibReader.things[j])
        uavs[i].transport(aaa)
TABU.tabu_solver(uavs,total_cost)