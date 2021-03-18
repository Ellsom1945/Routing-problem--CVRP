import numpy as np
import math
import random
import re

coordinates1 = np.array([[200.0, 30.0], [180.0, 70.0], [250.0, 200.0]])  # 需求地坐标

coordinates2 = np.array([[100.0, 30.0], [70.0, 50.0], [30.0, 100.0]])  # 供应地坐标
coordinates1goods = []
coordinates2goods = []

truck_coordinates = [[4292, 4798, 1]]  # 无人机的【x坐标，y坐标，载货量】


def data2():
    for i in range(len(coordinates1)):
        coordinates1goods[i] = 1  # 首先生成两个个禁忌表，用遗传求出tsp
    for i in range(len(coordinates2)):
        coordinates2goods[i] = 1


def data():
    for i in range(len(coordinates1)):
        coordinates1goods.append(1)  # 首先生成两个个禁忌表，用遗传求出tsp
    for i in range(len(coordinates2)):
        coordinates2goods.append(1)


data()

alllujing = []  # 记录所有路径
car_size = 200  # 种群数量
c_rate = 0.7  # "交叉率"


class Truck:
    def __init__(self, x, y, volume):
        self.x = x
        self.y = y  # 起点设置为（0，0）
        self.lat_x = 0
        self.lat_y = 0
        self.goto = 0
        self.drivedistance = 0.0
        self.involume = 0
        self.lastinvolume = 0
        self.volume = volume
        self.goal = "供应地"
        self.goods = 0
        self.buff = " "
        self.lastdrive = 0
        self.current_capacity = 0

        self.last_drivedistance = 0
        self.drawpath = [[x, y]]  # 基因走过的坐标
        self.lujing = []  # 基因当前路径（代号形式）
        self.last_lujing = []
        self.best_lujing = []


def lenth(x1, y1, x2, y2):
    return math.sqrt((int(x1) - int(x2)) ** 2 + (int(y1) - int(y2)) ** 2)  # 用于计算路径表


def paixudistmat(distmat):  # 返回一个最近坐标表
    p = []
    a = sorted(distmat.items(), key=lambda x: x[1])
    for i in range(len(a)):
        p.append(a[i])
    return p


def checklist1(checknum):  # 最近供应地坐标
    list = []
    num = []
    for i in range(len(coordinates2)):
        list.append(lenth(coordinates1[checknum][0], coordinates1[checknum][1], coordinates2[i][0], coordinates2[i][1]))
    for i in range(len(coordinates2)):
        num.append(i)
    k = dict(zip(num, list))
    op = paixudistmat(k)
    return op


totallist1 = []
for i in range(len(coordinates1)):
    totallist1.append(checklist1(i))
print(totallist1)


def checklist2(checknum):  # 最近需求地坐标
    list = []
    num = []
    for i in range(len(coordinates1)):
        list.append(lenth(coordinates2[checknum][0], coordinates2[checknum][1], coordinates1[i][0], coordinates1[i][1]))
    for i in range(len(coordinates1)):
        num.append(i)
    k = dict(zip(num, list))
    op = paixudistmat(k)
    return op


totallist2 = []
for i in range(len(coordinates2)):
    totallist2.append(checklist2(i))


def jisuan(num):
    list = []
    for i in range(len(coordinates2)):
        list.append(lenth(car[num].x, car[num].y, coordinates2[i][0], coordinates2[i][1]))  # 到达最近的供应地
    s = 0
    min = list[0]
    for i in range(len(coordinates2)):
        if list[i] < min:
            s = i
            min = list[i]
    return (s, min)  # 返回一个最小距离的下标和距离


car = []
for i in range(len(truck_coordinates)):
    car.append(Truck(truck_coordinates[i][0], truck_coordinates[i][1], truck_coordinates[i][2]))


def cross(parent1, parent2):  # parent1是要交换的基因    函数填（当前基因，之前基因）
    if np.random.rand() > c_rate:
        return parent1
    index1 = np.random.randint(0, len(parent1))
    index2 = np.random.randint(index1, len(parent1))
    tempcar1 = parent1[index1:index2]
    tempcar2 = parent2[index1:index2]  # parent2 給 parant1交叉的基因片段
    if (tempcar1 == tempcar2):
        return parent1
    difference1 = list(set(tempcar1) - set(tempcar2))  # 差集，在tempGen1中但不在tempGen2中的元素
    difference2 = list(set(tempcar2) - set(tempcar1))  # 差集，在tempcar2中但不在tempcar1中的元素
    if (len(difference1) == 0):
        return parent1

    else:
        k = 0
        for i in range(len(tempcar2)):
            parent1[index1 + i] = tempcar2[i]
        for i in range(0, index1):
            for j in range(len(difference2)):
                if (parent1[i] == difference2[j]):
                    if (k < len(difference1) - 1):
                        parent1[i] = difference1[k]
                        k = k + 1
        for i in range(index2, len(parent1) - 1):
            for j in range(len(difference2)):
                if (parent1[i] == difference2[j]):
                    if (k < len(difference1) - 1):
                        parent1[i] = difference1[k]
                        k = k + 1
        return parent1


def select(checknum, totallist1, totallist2, carnumber):
    sum = 0
    coordinatesArrivable_one = []  # 更新后的禁忌表（供应地）
    coordinatesArrivable_twe = []  # 禁忌表（需求地）
    coordinatesArrivable_one_gailv = []  # (供应地概率表)
    coordinatesArrivable_twe_gailv = []  # （需求地概率表）

    if (car[carnumber].buff == "到达需求地"):
        for i in range(len(totallist1[checknum])):
            coordinatesArrivable_one.append(totallist1[checknum][i])  # 更新禁忌表
        for i in range(len(coordinatesArrivable_one)):
            if (coordinates2goods[coordinatesArrivable_one[i][0]] > 0):
                sum += 1 / coordinatesArrivable_one[i][1]
        for i in range(len(coordinatesArrivable_one)):
            if (coordinates2goods[i] == 0):
                coordinatesArrivable_one_gailv.append(0)
            else:
                coordinatesArrivable_one_gailv.append((1 / coordinatesArrivable_one[i][1]) / sum)
        r_ = 0
        ran = random.random()
        for i in range(len(coordinatesArrivable_one_gailv)):
            r_ += coordinatesArrivable_one_gailv[i]
            if ran < r_:
                coordinates2goods[i] = 0
                break
        return coordinatesArrivable_one[i]

    if (car[carnumber].buff == "到达供应地"):
        for i in range(len(totallist2[checknum])):
            coordinatesArrivable_twe.append(totallist2[checknum][i])  # 更新禁忌表
        for i in range(len(coordinatesArrivable_twe)):
            if (coordinates1goods[coordinatesArrivable_twe[i][0]] > 0):
                sum += 1 / coordinatesArrivable_twe[i][1]
        for i in range(len(coordinatesArrivable_twe)):
            if (coordinates1goods[i] == 0):
                coordinatesArrivable_twe_gailv.append(0)
            else:
                coordinatesArrivable_twe_gailv.append((1 / coordinatesArrivable_twe[i][1]) / sum)
        r_ = 0
        ran = random.random()
        for i in range(len(coordinatesArrivable_twe_gailv)):
            r_ += coordinatesArrivable_twe_gailv[i]
            if ran < r_:
                coordinates1goods[i] = 0
                break
        return coordinatesArrivable_twe[i]


def sousuodistance(listone):  # 输入的是一组路径   返回路径长度
    def soushuo(text, listone, i):
        distance = 0
        op = int(re.findall("\d+", listone[i])[0])
        op2 = int(re.findall("\d+", listone[i + 1])[0])
        if (text == "到达供应地"):
            listtwo = checklist2(op)
            for j in range(len(listtwo)):
                if (op2 == listtwo[j][0]):  # 利用正则表达式比较地点
                    distance = listtwo[j][1]
            return distance

        if (text == "到达需求地"):
            listtwo = checklist1(op)
            for j in range(len(listtwo)):
                if op2 == listtwo[j][0]:  # 利用正则表达式比较地点
                    distance = listtwo[j][1]
            return distance

    distance = 0
    for i in range(len(listone) - 1):
        if listone[i][0:5] == '到达供应地':
            distance += soushuo("到达供应地", listone, i)

        if listone[i][0:5] == '到达需求地':
            distance += soushuo("到达需求地", listone, i)
    return distance


def transport():
    def yusong1():  # 更新到达供应地情况
        op = select(car[i].goto, totallist1, totallist2, i)

        if (car[i].buff == "到达需求地"):
            car[i].buff = "到达供应地"
            car[i].goal = "需求地"
            car[i].goto = op[0]
            car[i].lat_x = car[i].x
            car[i].lat_y = car[i].y
            car[i].x = coordinates2[op[0]][0]
            car[i].y = coordinates2[op[0]][1]
            car[i].lujing.append(str(car[i].buff) + str(car[i].goto))
            car[i].drawpath.append([car[i].x, car[i].y])
            car[i].drivedistance += op[1]

    def yusong2():
        op = select(car[i].goto, totallist1, totallist2, i)
        if (car[i].buff == "到达供应地"):
            car[i].buff = "到达需求地"
            car[i].goal = "供应地"
            car[i].goto = op[0]
            car[i].lat_x = car[i].x
            car[i].lat_y = car[i].y
            car[i].x = coordinates1[op[0]][0]
            car[i].y = coordinates1[op[0]][1]
            car[i].lujing.append(str(car[i].buff) + str(car[i].goto))
            car[i].drawpath.append([car[i].x, car[i].y])
            car[i].drivedistance += op[1]
            car[i].lastdrive = op[1]

    while True:
        if (max(coordinates2goods)) == 0:
            return 0
        for i in range(len(truck_coordinates)):  # 开始送货
            yusong1()
            yusong2()
            if (max(coordinates2goods)) == 0:
                return 0


for i in range(len(truck_coordinates)):  # 2是汽车数量，可以统计汽车输入的个数，将其换为变量
    print("卡车：" + str(i))
    print(car[i].lujing)
    print("卡车的路径坐标表:", car[i].drawpath)
    print('\n')

alltime = []
allmintime = []
for up in range(car_size):
    car = []
    for i in range(len(truck_coordinates)):
        car.append(Truck(truck_coordinates[i][0], truck_coordinates[i][1], truck_coordinates[i][2]))

    for i in range(len(truck_coordinates)):  # 初始化参数
        car[i].goto = jisuan(i)[0]
        car[i].drivedistance = jisuan(i)[1]
        car[i].x = coordinates2[car[i].goto][0]
        car[i].y = coordinates2[car[i].goto][1]
        car[i].drawpath.append([car[i].x, car[i].y])
        car[i].goal = "需求地"
        car[i].current_capacity = 1
        car[i].buff = "到达供应地"
        car[i].lujing.append(str(car[i].buff) + str(car[i].goto))

    transport()
    if (max(coordinates1goods) > 0):
        up = up - 1
    else:
        for i in range(len(truck_coordinates)):  # 2是基因数量，可以统计基因输入的个数，将其换为变量
            print("基因：" + str(i))
            print(car[i].lujing)
            print("基因的路径坐标表:", car[i].drawpath)
            print('\n')
        mintime = []
        for i in range(len(truck_coordinates)):
            alllujing.append(car[i].lujing)
            mintime.append(car[i].drivedistance)
            if (up > 1):
                car[i].last_drivedistance = car
        if (max(coordinates1goods) > 0):
            up = up - 1
        allmintime.append(max(mintime))

        op = len(allmintime)
        if (op > 1):
            if (allmintime[op - 2] > allmintime[op - 1]):
                new_lujing = cross(alllujing[op - 2], alllujing[op - 1])
                print("新的路径", new_lujing)
                new_mintime = sousuodistance((new_lujing))
                if (new_mintime < allmintime[op - 1]):
                    alllujing[op - 2] = new_mintime
    data2()
    gene_coordinates = [[4292, 4798, 1]]

the_bestdistance = min(allmintime)
the_bestluing = alllujing[int(np.argmin(allmintime))]
the_bestgene = np.argmin(allmintime)
print("该基因是：", the_bestluing)
print("该次路径为：", the_bestgene)
l1 = alllujing[int(np.argmin(allmintime))]  # 去除重复的地点
lst = []
for el in l1:
    if lst.count(el) < 1:
        lst.append(el)

print(lst)
print(len(lst))


class Truck2:
    def __init__(self, x, y, volume):
        self.init = 0  # 起始出发点
        self.drivedistance = 0.0  # 行驶距离
        self.goods = 0
        self.lujing = []
        self.last_lujing = []
        self.drawpath = [[x, y]]
        self.volume = volume
        self.involume = 0  # 当前运载的货量

    def __str__(self):
        return '出发点{} 总共走了{}距离 已经装运{}'. \
            format(self.init, self.drivedistance, self.goods)


coordinates1 = np.array([[200.0, 30.0], [180.0, 70.0], [250.0, 200.0]])  # 需求地坐标
coordinates1goods = np.array([[3.0], [2.0], [1.0]])

coordinates2 = np.array([[100.0, 30.0], [70.0, 50.0], [30.0, 100.0]])  # 供应地坐标
coordinates2goods = np.array([[6.0], [5.0], [4.0]])  # 供应地物资
truck_coordinates = [(150, 70, 1), (120, 150, 1)]
truck = []
for i in range(len(truck_coordinates)):
    truck.append(Truck2(truck_coordinates[i][0], truck_coordinates[i][1], truck_coordinates[i][2]))


def fengge():
    op = len(lst) // 2
    print(op)
    for i in range(op):
        truck[0].lujing.append(lst[i])
    for i in range(op):
        truck[1].lujing.append(lst[i + op])
    for i in range(len(truck_coordinates)):
        print("无人机", i, "路径:", truck[i].lujing)


def truck_transport(i):  # i为无人机编号            根据路径运输
    if (truck[i].lujing[0][0:5] == "到达供应地"):
        for k in range(len(truck[i].lujing) - 1):
            if (k % 2 == 0):
                op1 = int(re.findall("\d+", truck[i].lujing[k])[0])
                op2 = int(re.findall("\d+", truck[i].lujing[k + 1])[0])
            else:
                op2 = int(re.findall("\d+", truck[i].lujing[k])[0])
                op1 = int(re.findall("\d+", truck[i].lujing[k + 1])[0])
            if (coordinates2goods[op1] > 0 and coordinates1goods[op2] > 0):
                if (coordinates2goods[op1] >= coordinates1goods[op2]):
                    cha = coordinates2goods[op1] - coordinates1goods[op2]
                    for k2 in range(int(coordinates1goods[op2])):
                        truck[i].last_lujing.append(truck[i].lujing[k])
                        truck[i].last_lujing.append(truck[i].lujing[k + 1])
                    coordinates2goods[op1] = cha
                    coordinates1goods[op2] = 0

                else:
                    cha = coordinates1goods[op2] - coordinates2goods[op1]
                    for k2 in range(int(coordinates2goods[op1])):
                        truck[i].last_lujing.append(truck[i].lujing[k])
                        truck[i].last_lujing.append(truck[i].lujing[k + 1])
                    coordinates2goods[op1] = 0
                    coordinates1goods[op2] = cha
    else:
        for k in range(len(truck[i].lujing) - 1):
            if (k % 2 == 0):
                op1 = int(re.findall("\d+", truck[i].lujing[k])[0])
                op2 = int(re.findall("\d+", truck[i].lujing[k + 1])[0])
            else:
                op2 = int(re.findall("\d+", truck[i].lujing[k])[0])
                op1 = int(re.findall("\d+", truck[i].lujing[k + 1])[0])
            if (coordinates1goods[op1] > 0 and coordinates2goods[op2] > 0):
                if (coordinates1goods[op1] >= coordinates2goods[op2]):
                    cha = coordinates1goods[op1] - coordinates2goods[op2]
                    for k2 in range(int(coordinates2goods[op2])):
                        truck[i].last_lujing.append(truck[i].lujing[k + 1])
                        truck[i].last_lujing.append(truck[i].lujing[k])
                    coordinates1goods[op1] = cha
                    coordinates2goods[op2] = 0

                else:
                    cha = coordinates2goods[op2] - coordinates1goods[op1]
                    for k2 in range(int(coordinates1goods[op1])):
                        truck[i].last_lujing.append(truck[i].lujing[k + 1])
                        truck[i].last_lujing.append(truck[i].lujing[k])
                    coordinates1goods[op1] = 0
                    coordinates2goods[op2] = cha
    print(coordinates1goods)
    print(coordinates2goods)


def youhuahanshu():  # 对运输路径进行优化
    if (sousuodistance(truck[0].last_lujing) / sousuodistance(truck[1].last_lujing) >= 1.3):
        truck[0].lujing.append(truck[1].lujing[0])


truck[0].lujing = lst
truck_transport(0)
print(sousuodistance(truck[0].last_lujing))
print(truck[0].last_lujing)

lst = truck[0].last_lujing
truck[0].lujing.clear()
fengge()
print(sousuodistance(truck[0].lujing))
print(sousuodistance(truck[1].lujing))
