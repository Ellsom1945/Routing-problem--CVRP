import datetime
import math
import random

import matplotlib.pyplot as plt

from H_Hy_Men import VRPLibReader

start_time = datetime.datetime.now()


# 供需地封装成site类
class Site:
    def __init__(self, x, y, ifo, goods, ):
        self.x = x
        self.y = y
        self.store = 0
        self.need = 0
        self.map = []
        self.description = ifo
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
        sites.append(Site(VRPLibReader.site[i][0], VRPLibReader.site[i][1], "sup", 100000000000))
    else:
        sites.append(Site(VRPLibReader.site[i][0], VRPLibReader.site[i][1], "req", VRPLibReader.things[i]))
    distmap.append([VRPLibReader.site[i][0], VRPLibReader.site[i][1]])


# 获取长度
def length(x1, y1, x2, y2):
    return math.sqrt((int(x1) - int(x2)) ** 2 + (int(y1) - int(y2)) ** 2)  # 用于计算路径表


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

    def __str__(self):
        return '坐标: [{},{}]当前运载的货量: {} 总共走了{}距离 '.format(self.x, self.y, self.capacity, self.covered_dis)

    # 无人机前往下一个地点
    def next_site(self):
        def updadte(goto, uav):
            global req_count
            global sup_count
            if goto == "closest":
                for poi in uav.at.map:
                    if poi[1].need + poi[1].store != 0:
                        if poi[1].description == "req":
                            if poi[1].need > uav.capacity:
                                pass
                            else:
                                uav.covered_dis += length(uav.x, uav.y, poi[1].x, poi[1].y)
                                uav.draw_path.append([uav.x, uav.y])
                                uav.at = poi[1]
                                uav.x = poi[1].x
                                uav.y = poi[1].y
                                uav.capacity -= poi[1].need
                                req_count -= poi[1].need
                                poi[1].need = 0
                                break
                        elif poi[1].description == "sup":
                            uav.covered_dis += length(uav.x, uav.y, poi[1].x, poi[1].y)
                            uav.draw_path.append([uav.x, uav.y])
                            uav.at = poi[1]
                            uav.x = poi[1].x
                            uav.y = poi[1].y
                            if poi[1].store >= uav.volume - uav.capacity:
                                poi[1].store -= (uav.volume - uav.capacity)
                                uav.capacity = uav.volume
                            else:
                                uav.capacity += poi[1].store
                                sup_count -= poi[1].store
                                poi[1].store = 0
                            break
            elif goto == "req":
                for poi in uav.at.map:
                    if poi[1].description == "req" and poi[1].need != 0:
                        uav.covered_dis += length(uav.x, uav.y, poi[1].x, poi[1].y)
                        uav.draw_path.append([uav.x, uav.y])
                        uav.at = poi[1]
                        uav.x = poi[1].x
                        uav.y = poi[1].y
                        if poi[1].need >= uav.capacity:
                            poi[1].need -= uav.capacity
                            req_count -= uav.capacity
                            uav.capacity = 0
                        else:
                            uav.capacity -= poi[1].need
                            req_count -= poi[1].need
                            poi[1].need = 0
                        break

        # 包含了所有特殊情况
        if self.at.description == "sup":
            updadte("req", self)
        elif self.at.description == "req":
            updadte("closest", self)


# 初始化每个site类内置的记录距离的地图
for i in sites:
    for si in sites:
        if i is si:
            continue
        i.map.append([length(i.x, i.y, si.x, si.y), si])
    i.map = sorted(i.map, key=lambda x: x[0])  # 无人机初始化
UAVs = []
UAVs.append(UAV(VRPLibReader.site[0][0], VRPLibReader.site[0][1], VRPLibReader.capacity, 0))
for i in UAVs:
    i.draw_path.append([i.x, i.y])
for i in UAVs:
    li = []
    for si in sites:
        if si.description == "sup":
            li.append([length(i.x, i.y, si.x, si.y), si])
    i.at = min(li, key=lambda x: x[0])[1]
    i.covered_dis += length(i.x, i.y, i.at.x, i.at.y)
    i.draw_path.append([i.x, i.y])
    i.x = i.at.x
    i.y = i.at.y
    if i.at.store >= i.volume:
        i.at.store -= i.volume
        i.capacity = i.volume
    else:
        i.capacity += i.at.store
        i.at.store = 0

a = 1
while True:
    if req_count < 1:
        break
    for i in UAVs:
        i.next_site()
end_time = datetime.datetime.now()
time_list = []
UAVs[0].draw_path.append([i.x, i.y])


class Customer:

    def __init__(self, num, demand):
        self.num = num
        self.demand = demand
        self.is_visited = False


class temp:
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


num = []
temps = []
for i in UAVs:
    time_list.append(i.covered_dis)
    for j in i.draw_path:
        a = distmap.index([j[0], j[1]])
        num.append(a)
time_list.append(VRPLibReader.distmat[distmap.index(UAVs[0].draw_path[-1])][0])

while num[0] == 0:
    del num[0]
tem = []
temps = []
for i in num:
    if (i != 0):
        tem.append(i)
    else:
        a = []
        for j in tem:
            a.append(j)
        temps.append(a)
        tem.clear()
temps.append(tem)
for i in temps:
    i.append(0)
    i.insert(0, 0)
print(temps,456)
uavs = []
for i in range(VRPLibReader.n):
    uavs.append(temp(VRPLibReader.capacity))
for i in range(len(temps)):
    for j in temps[i]:
        aaa = Customer(j, VRPLibReader.things[j])
        uavs[i].transport(aaa)
total_cost = sum(time_list)
num.append(0)
num.insert(0, 0)
print(num)


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


draw_path(temps, VRPLibReader.site)
print("greedy cost:", total_cost)
print('算法时间:', end_time - start_time)
