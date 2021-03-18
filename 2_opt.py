import datetime
import math
import matplotlib.pyplot as plt
import numpy as np
import cmath
import operator
from H_Hy_Men import VRPLibReader

start_time = datetime.datetime.now()


# 供需地封装成site类
class Site:
    def __init__(self, x, y, ifo, goods):
        self.map = []
        self.x = x
        self.y = y
        self.store = 0
        self.need = 0
        self.description = ifo
        self.angle = 0
        if ifo == "req":
            self.need = goods
        elif ifo == "sup":
            self.store = goods

    def __str__(self):
        return '[{},{}]+{}+{}+{}+{}'.format(self.x, self.y, self.description, self.store, self.need, self.angle)


# sites里面储存了所有的供需地
sites = []
for i in range(len(VRPLibReader.site)):
    if i==0:
        sites.append(Site(VRPLibReader.site[i][0], VRPLibReader.site[i][1], "sup", VRPLibReader.things[i]))
    else:
        sites.append(Site(VRPLibReader.site[i][0], VRPLibReader.site[i][1], "req", VRPLibReader.things[i]))


# 获取长度
def length(x1, y1, x2, y2):
    return math.sqrt((int(x1) - int(x2)) ** 2 + (int(y1) - int(y2)) ** 2)  # 用于计算路径表


# 初始化每个site类内置的记录距离的地图和用来分组的极坐标系
for i in sites:
    i.angle = cmath.polar(complex(i.x - VRPLibReader.site[0][0], i.y - VRPLibReader.site[0][1]))[1]
# 分组操作
sites2 = []
for i in sites:
    if i.store == 0:
        sites2.append(i)
cmpfunc = operator.attrgetter('angle')
sites2.sort(key=cmpfunc)
zone = []
count = 0
group = []
temp = 0
while len(sites2) > 0:
    temp = sites2.pop()
    if count + temp.need > VRPLibReader.capacity:
        ttt = group.copy()
        zone.append(ttt)
        group.clear()
        count = 0
        sites2.append(temp)
    else:
        count += temp.need
        group.append(temp)
        if (len(sites2) == 0):
            zone.append(group)


# 无人机类
class UAV:
    def __init__(self, x, y, volume, num):
        self.x = x
        self.y = y
        self.volume = volume
        self.covered_dis = 0
        self.draw_path = []
        self.capacity = 0
        self.at = Site(0, 0, 0, 0)
        self.number = num

    def __str__(self):
        return '坐标: [{},{}]当前运载的货量: {} 总共走了{}距离 '.format(self.x, self.y, self.capacity, self.covered_dis)

    # 画图操作
    def draw_picture(self):
        color = ['b', 'g', 'r', 'c']
        for k in range(len(VRPLibReader.site)):
            if k==0:
                plt.plot(VRPLibReader.site[k][0], VRPLibReader.site[k][1], 'r', marker='o')  # 红色 需求点坐标为o
            else:
                plt.plot(VRPLibReader.site[k][0], VRPLibReader.site[k][1], 'b', marker='>')  # 蓝色 供应点坐标为>
        for k in range(len(self.draw_path) - 1):
            plt.plot((self.draw_path[k][0], self.draw_path[k + 1][0]),
                     (self.draw_path[k][1], self.draw_path[k + 1][1]),
                     color[self.number % 4])
        plt.title('car: ' + str(self.number), fontsize=30)
        plt.show()
        plt.close()


# 无人机初始化
UAVs = []
UAVs.append(UAV(VRPLibReader.site[0][0], VRPLibReader.site[0][1], VRPLibReader.capacity, 0))
for i in UAVs:
    i.draw_path.append([i.x,i.y])

# A*启发式函数模块：
def isbest(i, bestpath, p):
    for k in bestpath[1:p + 1]:
        if i == k:
            return 1
    return 0

print(zone)
MAXCOUNT = 500
c = 0
for z in zone:
    # 数据在这里输入，依次键入每个城市的坐标
    z.insert(0, Site(VRPLibReader.site[0][0], VRPLibReader.site[0][0], "sup", 10000))
    city = []
    for i in z:
        city.append([i.x,i.y])
    cities=np.array(city)

    #2-opt模块
    # 1 随机选择一条路线（比方说是A->B->C->D->E->F->G），假设是最短路线min；
    # 2 随机选择在路线s中不相连两个节点，将两个节点之间的路径翻转过来获得新路径，比方我们随机选中了B节点和E节点，则新路径为A->(E->D->C->B)->F->G，()
    # 3 部分为被翻转的路径;
    # 4 如果新路径比min路径短，则设新路径为最短路径min，将计数器count置为0，返回步骤2，否则将计数器count加1，当count大于等于maxCount时，算法结束，此时min即为最短路径，否则返回步骤2;

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
        while count < MAXCOUNT:
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
    bestpath=opt2().tolist()
    for i in bestpath:
        UAVs[c].draw_path.append([z[i].x, z[i].y])
    c = (c + 1) % len(UAVs)
end_time = datetime.datetime.now()
print()
print('算法时间:', end_time - start_time)
for i in UAVs:
    for j in range(1, len(i.draw_path)):
        i.covered_dis += length(i.draw_path[j - 1][0], i.draw_path[j - 1][1], i.draw_path[j][0], i.draw_path[j][0])
time_list = []
for i in UAVs:
    time_list.append(i.covered_dis)
    i.draw_picture()
print(sum(time_list))
