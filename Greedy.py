import datetime
import math
import random

import matplotlib.pyplot as plt

from H_Hy_Men import VRPLibReader

start_time = datetime.datetime.now()


def value(a):
    s = 0
    for i in range(len(a) - 1):
        s += VRPLibReader.distmat[a[i]][a[i + 1]]
    return s


# 获取长度
def length(x1, y1, x2, y2):
    return math.sqrt((int(x1) - int(x2)) ** 2 + (int(y1) - int(y2)) ** 2)  # 用于计算路径表

class Site:
    def __init__(self, x, y, ifo, goods, num):
        self.num = num
        self.x = x
        self.y = y
        self.store = 0
        self.need = 0
        self.map = []
        self.map2 = []
        self.description = ifo
        self.to_point = length(self.x, self.y, VRPLibReader.site[0][0], VRPLibReader.site[0][1])
        if ifo == "req":
            self.need = goods
        elif ifo == "sup":
            self.store = goods

    def __str__(self):
        return '[{},{}]+{}+{}+{}'.format(self.x, self.y, self.description, self.store, self.need)


# sites里面储存了所有的供需地
sites = []
distmap = []
for i in range(len(VRPLibReader.site)):
    if i == 0:
        sites.append(Site(VRPLibReader.site[i][0], VRPLibReader.site[i][1], "sup", 100000000000, i))
    else:
        sites.append(Site(VRPLibReader.site[i][0], VRPLibReader.site[i][1], "req", VRPLibReader.things[i], i))
    distmap.append([VRPLibReader.site[i][0], VRPLibReader.site[i][1]])

# 需求货物计数器
req_count = 0
for i in VRPLibReader.things:
    req_count += i



# 无人机类
class UAV:
    def __init__(self, x, y, volume, num):
        self.x = x
        self.y = y
        self.volume = volume
        self.covered_dis = 0
        self.draw_path = []
        self.capacity = volume
        self.at = sites[0]
        self.number = num
        self.end = None

    def __str__(self):
        return '坐标: [{},{}]当前运载的货量: {} 总共走了{}距离 '.format(self.x, self.y, self.capacity, self.covered_dis)

    # 无人机前往下一个地点
    def next_site(self):
        global req_count
        global sup_count
        if self.capacity > self.volume / 2 :
            for poi in self.at.map:
                if poi[1].need != 0:
                    if poi[1].description == "req":
                        if poi[1].need <= self.capacity:
                            self.covered_dis += length(self.x, self.y, poi[1].x, poi[1].y)
                            self.draw_path.append(poi[1].num)
                            self.at = poi[1]
                            self.x = poi[1].x
                            self.y = poi[1].y
                            self.capacity -= poi[1].need
                            req_count -= poi[1].need
                            poi[1].need = 0
                            break
        else:
            if self.end is None:
                self.end = self.at
            for poi in self.end.map2:
                if poi[1].need != 0:
                    if poi[1].description == "req":
                        if poi[1].need <= self.capacity:
                            self.covered_dis += length(self.x, self.y, poi[1].x, poi[1].y)
                            self.draw_path.append(poi[1].num)
                            self.at = poi[1]
                            self.x = poi[1].x
                            self.y = poi[1].y
                            self.capacity -= poi[1].need
                            req_count -= poi[1].need
                            poi[1].need = 0

for i in sites:
    for si in sites[1:]:
        if i is si:
            continue
        i.map.append([length(i.x, i.y, si.x, si.y), si])
    i.map = sorted(i.map, key=lambda x: x[0])
for i in sites[1:]:
    for si in sites[1:]:
        if i is si:
            continue
        i.map2.append([length(i.x, i.y, si.x, si.y), si])
    i.map2 = sorted(i.map2, key=lambda x: x[0] ** 2 + x[1].to_point)
UAVs = []
for i in range(VRPLibReader.carnum):
    UAVs.append(UAV(VRPLibReader.site[0][0], VRPLibReader.site[0][1], VRPLibReader.capacity, 0))
for i in UAVs:
    i.draw_path.append(0)
while True:
    print(req_count)
    if req_count < 1:
        break
    for i in UAVs:
        i.next_site()
for i in UAVs:
    i.draw_path.append(0)
end_time = datetime.datetime.now()

allpath = []
for i in UAVs:
    allpath.append(i.draw_path)
way = [0]
for i in allpath:
    for j in i[1:len(i) - 1]:
        way.append(j)
    way.append(0)


def draw_path(path, sites):
    color = ['r', 'k', 'y', 'c', 'b', 'g', 'm', 'dodgerblue', 'gold', 'peru', 'darkolivegreen', 'indigo', 'lime',
             'deeppink']
    plt.xlim(0, 100)
    plt.ylim(0, 100)
    for i in path:
        c = random.choice(color)
        for j in range(0, len(i) - 1):
            plt.plot((sites[i[j]][0], sites[i[j + 1]][0]), (sites[i[j]][1], sites[i[j + 1]][1]), c, marker='.')
    plt.show()


total_cost = value(way)
print(way)
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
            if len(a)>0:
                temps.append(a)
            tem.clear()
    for i in temps:
        i.append(0)
        i.insert(0, 0)
    return temps
