import datetime
import math
import matplotlib.pyplot as plt
from H_Hy_Men import VRPLibReader

start_time = datetime.datetime.now()


# 供需地封装成site类
class Site:
    def __init__(self, x, y, ifo, goods):
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
for i in range(len(VRPLibReader.site)):
    if i==0:
        sites.append(Site(VRPLibReader.site[i][0], VRPLibReader.site[i][1], "sup", VRPLibReader.things[i]))
    else:
        sites.append(Site(VRPLibReader.site[i][0], VRPLibReader.site[i][1], "req", VRPLibReader.things[i]))

# 获取长度
def length(x1, y1, x2, y2):
    return math.sqrt((int(x1) - int(x2)) ** 2 + (int(y1) - int(y2)) ** 2)  # 用于计算路径表


# 需求货物计数器
req_count = 0
for i in VRPLibReader.things:
    req_count += i
# 供应货物计数器
sup_count = 100000000000



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
            if k == 0:
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

    # 无人机前往下一个地点
    def next_site(self):
        def updadte(goto, uav):
            global req_count
            global sup_count
            if goto == "closest":
                for poi in uav.at.map:
                    if poi[1].need + poi[1].store != 0:
                        if poi[1].description == "req":
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
                        elif poi[1].description == "sup":
                            uav.covered_dis += length(uav.x, uav.y, poi[1].x, poi[1].y)
                            uav.draw_path.append([uav.x, uav.y])
                            uav.at = poi[1]
                            uav.x = poi[1].x
                            uav.y = poi[1].y
                            if poi[1].store >= uav.volume - uav.capacity:
                                poi[1].store -= (uav.volume - uav.capacity)
                                sup_count -= (uav.volume - uav.capacity)
                                uav.capacity = uav.volume
                            else:
                                uav.capacity += poi[1].store
                                sup_count -= poi[1].store
                                poi[1].store = 0
                            break
            elif goto == "sup":
                for poi in uav.at.map:
                    if poi[1].description == "sup" and poi[1].store != 0:
                        uav.covered_dis += length(uav.x, uav.y, poi[1].x, poi[1].y)
                        uav.draw_path.append([uav.x, uav.y])
                        uav.at = poi[1]
                        uav.x = poi[1].x
                        uav.y = poi[1].y
                        if poi[1].store >= (uav.volume - uav.capacity):
                            poi[1].store -= (uav.volume - uav.capacity)
                            sup_count -= (uav.volume - uav.capacity)
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
            if self.volume == self.capacity:
                updadte("req", self)
            else:
                updadte("closest", self)
        elif self.at.description == "req":
            if self.capacity == 0:
                updadte("sup", self)
            else:
                updadte("closest", self)


# 初始化每个site类内置的记录距离的地图
for i in sites:
    for si in sites:
        if i is si:
            continue
        i.map.append([length(i.x, i.y, si.x, si.y), si])
    i.map = sorted(i.map, key=lambda x: x[0])# 无人机初始化
UAVs = []
UAVs.append(UAV(VRPLibReader.site[0][0], VRPLibReader.site[0][1], VRPLibReader.capacity, 0))
for i in UAVs:
    i.draw_path.append([i.x,i.y])
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
        sup_count -= i.volume
    else:
        i.capacity += i.at.store
        sup_count -= i.at.store
        i.at.store = 0
    print(i)
a=1
while True:
    if sup_count == 0:
        break
    if req_count < 1:
        break
    for i in UAVs:
        i.next_site()
    print(req_count)
    a=a+1

end_time = datetime.datetime.now()
print()
print('算法时间:', end_time - start_time)
time_list = []
for i in UAVs:
    time_list.append(i.covered_dis)
    i.draw_picture()
# 输出代价
print(sum(time_list))