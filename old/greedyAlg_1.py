import math
import numpy as np
import matplotlib.pyplot as plt
import random
import datetime

start_time = datetime.datetime.now()
'''这个程序可以计算出货车承重为1的多辆货车的最短路径，输入需求点和供应点坐标，以及对应的货物量，就能求出最短路径'''


def add(text, n):  # 添加数组
    a = []
    if (text == "添加坐标"):
        for i in range(n):
            a.append([int(random.random() * 5000), int(random.random() * 5000)])
    if (text == "添加物资"):
        for i in range(n):  # 随机出来的物资可能需求大于供应
            a.append(int(random.random() * 10) + 1)
    return a


coordinates1 = np.array([[200.0, 30.0], [180.0, 70.0], [250.0, 200.0]])  # 需求地坐标
coordinates1goods = np.array([[3.0], [2.0], [1.0]])

coordinates2 = np.array([[100.0, 30.0], [70.0, 50.0], [30.0, 100.0]])  # 供应地坐标
coordinates2goods = np.array([[6.0], [5.0], [4.0]])  # 供应地物资

truck_coordinates = [(150, 70), (120, 150)]  # 无人机的【x坐标，y坐标】


class Truck:
    def __init__(self, x, y):
        self.x = x
        self.y = y  # 起点设置为（0，0）
        self.lat_x = 0
        self.lat_y = 0
        self.goto = 0
        self.drivedistance = 0.0
        self.goal = "供应地"
        self.goods = 0
        self.buff = "待命"
        self.lujing = []
        self.drawpath = [[x, y]]
        self.lastdrive = 0
        self.current_capacity = 0  # 当前运载的货量

    def __str__(self):
        return '坐标: [{},{}],{}：{}当前运载的货量: {} 总共走了{}距离 正在前往{} 已经装运{}'. \
            format(self.x, self.y, self.buff, self.goto, self.current_capacity, self.drivedistance, self.goal,
                   self.goods)


def lenth(x1, y1, x2, y2):
    return math.sqrt((int(x1) - int(x2)) ** 2 + (int(y1) - int(y2)) ** 2)  # 用于计算路径表


def paixudistmat(distmat):  # 返回一个最近坐标表
    p = []
    # print(distmat[n].items())
    a = sorted(distmat.items(), key=lambda x: x[1])
    # print(a)
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


def check(text, checknum, totallist1, totallist2):
    if text == "查找最近的供应地":
        s = 0
        min = totallist1[checknum][0]
        for i in range(len(coordinates2)):
            if coordinates2goods[totallist1[checknum][i][0]] > 0:
                s = totallist1[checknum][i][0]
                min = totallist1[checknum][i][1]
                return (s, min)

    if text == "查找最近的需求地":
        s = 0
        min = totallist2[checknum][0]
        for i in range(len(coordinates1)):
            if coordinates1goods[totallist2[checknum][i][0]] > 0:
                s = totallist2[checknum][i][0]
                min = totallist2[checknum][i][1]
                return (s, min)


# print(check("查找最近的需求地",0,totallist1,totallist2)) #      第一个参数是（查找） 第二个参数是 当前点序号  之后参数固定

def jisuan(num):
    list = []
    for i in range(len(coordinates2)):
        # print(car[num].x,car[num].y, coordinates2[i][0],coordinates2[i][1])
        list.append(lenth(car[num].x, car[num].y, coordinates2[i][0], coordinates2[i][1]))
    # print(list)
    s = 0
    min = list[0]
    for i in range(len(coordinates2)):
        if list[i] < min:
            s = i
            min = list[i]
    return (s, min)  # 返回一个最小距离的下标和距离


car = []
for i in range(len(truck_coordinates)):
    car.append(Truck(truck_coordinates[i][0], truck_coordinates[i][1]))

for i in range(len(truck_coordinates)):  # 给卡车初始化
    car[i].goto = jisuan(i)[0]
    car[i].drivedistance = jisuan(i)[1]
    car[i].x = coordinates2[car[i].goto][0]
    car[i].y = coordinates2[car[i].goto][1]
    car[i].drawpath.append([car[i].x, car[i].y])
    car[i].goal = "需求地"
    car[i].current_capacity = 1
    car[i].buff = "到达供应地"
    car[i].lujing.append(str(car[i].buff) + str(car[i].goto))
    print(car[i])


def transport():
    def yusong2():
        op = check("查找最近的供应地", car[i].goto, totallist1, totallist2)
        car[i].lat_x = car[i].x
        car[i].lat_y = car[i].y
        car[i].x = coordinates2[op[0]][0]
        car[i].y = coordinates2[op[0]][1]
        # print(car[i].x,car[i].y)
        car[i].goto = op[0]
        car[i].buff = "到达供应地"
        car[i].goal = "需求地"
        car[i].lujing.append(str(car[i].buff) + str(car[i].goto))
        car[i].drawpath.append([car[i].x, car[i].y])  # 添加卡车走过的坐标
        car[i].drivedistance += op[1]
        car[i].lastdrive = op[1]
        coordinates2goods[op[0]] -= 1
        car[i].goods += 1
        # print(car[i])

    def yusong1():
        op = check("查找最近的需求地", car[i].goto, totallist1, totallist2)
        car[i].lat_x = car[i].x
        car[i].lat_y = car[i].y
        car[i].x = coordinates1[op[0]][0]
        car[i].y = coordinates1[op[0]][1]
        car[i].goto = op[0]
        car[i].buff = "到达需求地"
        car[i].goal = "供应地"
        car[i].lujing.append(str(car[i].buff) + str(car[i].goto))
        car[i].drawpath.append([car[i].x, car[i].y])
        car[i].drivedistance += op[1]
        car[i].lastdrive = op[1]
        coordinates1goods[op[0]] -= 1
        # print(car[i])

    while (True):
        if (max(coordinates1goods)) == 0:
            return 0
        elif (max(coordinates2goods) == 0):
            return 0

        for i in range(len(truck_coordinates)):  # 开始送货
            if (car[i].goal == "需求地"):
                if (max(coordinates1goods) == 0):
                    return 0
                elif (max(coordinates2goods) == 0):
                    return 0
                yusong1()
                yusong2()


def drawpicture(p):
    color = ['b', 'g', 'r', 'c']
    for i in range(len(coordinates1)):
        plt.plot(coordinates1[i][0], coordinates1[i][1], 'r', marker='o')  # 红色 需求点坐标为o
    for i in range(len(coordinates2)):
        plt.plot(coordinates2[i][0], coordinates2[i][1], 'b', marker='>')  # 蓝色 供应点坐标为>
    for i in range(len(truck_coordinates)):
        plt.plot(truck_coordinates[i][0], truck_coordinates[i][1], 'black', marker='1')  # 黑色 汽车初始位置
    for j in range(len(car[p].drawpath) - 1):
        plt.plot((car[p].drawpath[j][0], car[p].drawpath[j + 1][0]), (car[p].drawpath[j][1], car[p].drawpath[j + 1][1]),
                 color[p % 4])
    plt.title('car: ' + str(p), fontsize=30)
    plt.show()
    plt.close()


transport()
end_time = datetime.datetime.now()
for i in range(len(truck_coordinates)):
    if (car[i].buff == "到达供应地"):
        car[i].x = car[i].lat_x
        car[i].y = car[i].lat_y
        car[i].drivedistance -= car[i].lastdrive
        car[i].lujing.pop()
        car[i].drawpath.pop()

for i in range(len(truck_coordinates)):  # 2是汽车数量，可以统计汽车输入的个数，将其换为变量
    print("卡车：" + str(i))
    print(car[i])
    print(car[i].lujing)
    print("卡车的路径坐标表:", car[i].drawpath)
    print('\n')

mintime = []
for i in range(len(truck_coordinates)):
    mintime.append(car[i].drivedistance)
print("需要最短时间为：", max(mintime))

for p in range(len(truck_coordinates)):  # 供应点与需求点太多，画图没有意义
    drawpicture(p)
print()
print('算法时间:', end_time - start_time)

'''判断结束的条件是，需求地或者供应地有一方物资全为0'''
