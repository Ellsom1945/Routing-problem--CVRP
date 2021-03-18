import math
import datetime
from old.greedyAlg3Data import coordinates2, coordinates1, coordinates2goods, coordinates1goods, truck_coordinates

start_time = datetime.datetime.now()


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
        self.goods = 0
        self.buff = "待命"
        self.lujing = []
        self.drawpath = [[x, y]]
        self.lastdrive = 0

    def __str__(self):
        return '坐标: [{},{}],{}：{}总共走了{}距离 已经装运{}  汽车容量为{}/{}'. \
            format(self.x, self.y, self.buff, self.goto, self.drivedistance, self.goods, self.involume, self.volume)


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


# print(totallist1)

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


# print(totallist2)

def checklist3(checknum):  # 需求地到需求地坐标
    list = []
    num = []
    for i in range(len(coordinates1)):
        list.append(lenth(coordinates1[checknum][0], coordinates1[checknum][1], coordinates1[i][0], coordinates1[i][1]))
    for i in range(len(coordinates1)):
        num.append(i)
    k = dict(zip(num, list))
    op = paixudistmat(k)
    return op


totallist3 = []
for i in range(len(coordinates1)):
    totallist3.append(checklist3(i))


# print(totallist3)

def checklist4(checknum):  # 供应地到供应地坐标
    list = []
    num = []
    for i in range(len(coordinates2)):
        list.append(lenth(coordinates2[checknum][0], coordinates2[checknum][1], coordinates2[i][0], coordinates2[i][1]))
    for i in range(len(coordinates2)):
        num.append(i)
    k = dict(zip(num, list))
    op = paixudistmat(k)
    return op


totallist4 = []
for i in range(len(coordinates2)):
    totallist4.append(checklist4(i))


# print(totallist4)

def jisuan(num):
    list = []
    for i in range(len(coordinates2)):
        # print(car[num].x,car[num].y, coordinates2[i][0],coordinates2[i][1])
        list.append(lenth(car[num].x, car[num].y, coordinates2[i][0], coordinates2[i][1]))  # 到达最近的供应地
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
    car.append(Truck(truck_coordinates[i][0], truck_coordinates[i][1], truck_coordinates[i][2]))

for i in range(len(truck_coordinates)):  # 给卡车初始化
    car[i].goto = jisuan(i)[0]
    car[i].drivedistance = jisuan(i)[1]
    car[i].x = coordinates2[car[i].goto][0]
    car[i].y = coordinates2[car[i].goto][1]
    car[i].drawpath.append([car[i].x, car[i].y])
    if (car[i].volume >= coordinates2goods[car[i].goto]):
        car[i].involume = coordinates2goods[car[i].goto]
        coordinates2goods[car[i].goto] = 0
    else:
        car[i].involume = car[i].volume
        coordinates2goods[car[i].goto] -= car[i].volume
    car[i].buff = "到达供应地"
    car[i].lujing.append(str(car[i].buff) + str(car[i].goto))


# print(totallist4)

def select(checknum, totallist1, totallist2, totallist3, totallist4,
           carnumber):  # 根据输入的车辆号码，从而得出该车的所在地点，返回它的下一步目标和目标的下标
    def maxselect(listone):
        max = listone[0][1]
        s = listone[0][0]
        for i in range(len(listone)):
            if (listone[i][1] > max):
                max = listone[i][1]
                s = listone[i][0]
        return (s, max)  # 返回（效率最高的下标，效率）

    coordinatesArrivable_one = []  # 同类型地点效率表
    coordinatesArrivable_twe = []  # 不同类型地点效率表
    if (car[carnumber].buff == "到达需求地"):
        for i in range(1, len(totallist3[checknum])):  # 计算当前需求地到需求地的效率
            if (coordinates1goods[totallist3[checknum][i][0]] <= car[
                carnumber].involume):  # 如果需求地物资小于等于车载的物资，效率=需求地物资/距离
                coordinatesArrivable_one.append((totallist3[checknum][i][0],
                                                 coordinates1goods[totallist3[checknum][i][0]] /
                                                 totallist3[checknum][i][1]))
                # print(totallist3[checknum][i][0])
                # print(coordinates1goods[totallist3[checknum][i][0]])
            else:
                coordinatesArrivable_one.append((totallist3[checknum][i][0],
                                                 car[carnumber].involume / totallist3[checknum][i][
                                                     1]))  # checknum:需求地标号，i:遍历 【1】：距离

        for i in range(len(totallist1[checknum])):  # 计算需求地到供应地的效率
            if (coordinates2goods[totallist1[checknum][i][0]] <= (car[carnumber].volume - car[carnumber].involume)):
                coordinatesArrivable_twe.append((totallist1[checknum][i][0],
                                                 coordinates2goods[totallist1[checknum][i][0]] /
                                                 totallist1[checknum][i][1]))
            else:
                coordinatesArrivable_twe.append((totallist1[checknum][i][0],
                                                 (car[carnumber].volume - car[carnumber].involume) /
                                                 totallist1[checknum][i][1]))

        # print("需求到需求的效率",coordinatesArrivable_one)
        # print("需求到供应的效率",coordinatesArrivable_twe)
        t1 = maxselect(coordinatesArrivable_one)
        t2 = maxselect(coordinatesArrivable_twe)
        if (t1[1] > t2[1]):
            return ("需求地到需求地", t1[0])
        else:
            return ("需求地到供应地", t2[0])

    if (car[carnumber].buff == "到达供应地"):
        for i in range(1, len(totallist4)):  # 计算当前供应地到供应地的效率
            if (coordinates2goods[totallist4[checknum][i][0]] <= (
                    car[carnumber].volume - car[carnumber].involume)):  # 如果供应地物资小于车辆剩余装货量，效率=供应地物资/距离
                coordinatesArrivable_one.append((totallist4[checknum][i][0],
                                                 coordinates2goods[totallist4[checknum][i][0]] /
                                                 totallist4[checknum][i][1]))  # checknum 为供应地标号
            else:
                coordinatesArrivable_one.append((totallist4[checknum][i][0],
                                                 (car[carnumber].volume - car[carnumber].involume) /
                                                 totallist4[checknum][i][1]))

        for i in range(len(totallist2)):  # 计算供应地到需求地的效率
            if (coordinates1goods[totallist2[checknum][i][0]] <= car[
                carnumber].involume):  # 如果需求地物资小于车辆装载的货物，效率=需求地物资/距离
                coordinatesArrivable_twe.append((totallist2[checknum][i][0],
                                                 coordinates1goods[totallist2[checknum][i][0]] /
                                                 totallist2[checknum][i][1]))
            else:
                # print(coordinates1goods[totallist2[checknum][i][0]])
                # print(totallist2[checknum][i][1])
                coordinatesArrivable_twe.append(
                    (totallist2[checknum][i][0], car[carnumber].involume / totallist2[checknum][i][1]))
        # print("供应到供应的效率",coordinatesArrivable_one)
        # print("供应到需求的效率",coordinatesArrivable_twe)
        t1 = maxselect(coordinatesArrivable_one)
        t2 = maxselect(coordinatesArrivable_twe)
        if (t1[1] > t2[1]):
            return ("供应地到供应地", t1[0])
        else:
            return ("供应地到需求地", t2[0])


def check(checknum, totallist1, totallist2, totallist3, totallist4, volume,
          carnumber):  # 输入当前位置，车辆的号码，车辆当前运载量，返回目标点下标和距离
    def gengxingongying(s):
        if coordinates2goods[s] >= car[carnumber].volume - volume:  # 供应物资》车载空的物资时，供应物资减去车载物资，车载物资变满
            coordinates2goods[s] -= car[carnumber].volume - volume
            # print(car[carnumber].volume-volume)
            # print("需求地物资为",coordinates2goods[s])
            car[carnumber].lastinvolume = car[carnumber].involume
            car[carnumber].involume = car[carnumber].volume

        else:  # 供应物资《车载物资时，车载物资加上供应物资，供应物资为0
            car[carnumber].lastinvolume = car[carnumber].involume
            car[carnumber].involume += coordinates2goods[s]
            coordinates2goods[s] = 0
            # print("供应地物资为", coordinates2goods[s])

    def gengxinxuqiu(s):
        flag = 0
        if coordinates1goods[s] >= volume:  # 需求的物资>车载物资时，需求物资减去车载物资，车载物资为0
            coordinates1goods[s] -= volume
            car[carnumber].goods += volume
            car[carnumber].lastinvolume = car[carnumber].involume
            car[carnumber].involume = 0
            return flag
        else:  # 需求的物资《车载物资时，车载物资减去需求物资，需求物资为0
            if (coordinates1goods[s] == 0):
                flag = 1
                return flag
            else:
                car[carnumber].goods += coordinates1goods[s]
                car[carnumber].lastinvolume = car[carnumber].involume
                car[carnumber].involume -= coordinates1goods[s]
                coordinates1goods[s] = 0
            return flag

    op = select(car[carnumber].goto, totallist1, totallist2, totallist3, totallist4, carnumber)
    s = op[1]
    min = "bug"
    if (op[0] == "需求地到需求地"):
        for i in range(len(totallist3[checknum])):
            if totallist3[checknum][i][0] == s:
                # print("车子所在地",checknum)
                min = totallist3[checknum][i][1]
                # print(min)
        if (gengxinxuqiu(s) == 1):
            op0 = " "
        else:
            op0 = "需求地"
        op0 = "需求地"
        return (s, min, op0)

    if (op[0] == "需求地到供应地"):
        for i in range(len(totallist1[checknum])):
            if totallist1[checknum][i][0] == s:
                min = totallist1[checknum][i][1]
        gengxingongying(s)
        op0 = "供应地"
        return (s, min, op0)

    if (op[0] == "供应地到供应地"):
        for i in range(len(totallist4[checknum])):
            if totallist4[checknum][i][0] == s:
                min = totallist4[checknum][i][1]
        gengxingongying(s)
        op0 = "供应地"
        return (s, min, op0)

    if (op[0] == "供应地到需求地"):
        for i in range(len(totallist2[checknum])):
            if totallist2[checknum][i][0] == s:
                min = totallist2[checknum][i][1]
        gengxinxuqiu(s)
        op0 = "需求地"
        return (s, min, op0)


# print(select(car[0].goto,totallist1,totallist2,totallist3,totallist4,0))
# print(check(car[1].goto,totallist1,totallist2,totallist3,totallist4,car[1].involume,1))
for i in range(len(truck_coordinates)):
    print(car[i])


def transport():
    def yusong():
        op = check(car[i].goto, totallist1, totallist2, totallist3, totallist4, car[i].involume, i)
        if (op[2] == " "):
            pass
        else:
            car[i].lat_x = car[i].x
            car[i].lat_y = car[i].y
            if (str(op[2]) == "需求地"):
                car[i].x = coordinates1[op[0]][0]
                car[i].y = coordinates1[op[0]][1]
            else:
                car[i].x = coordinates2[op[0]][0]
                car[i].y = coordinates2[op[0]][1]
            # print(car[i].x,car[i].y)
            car[i].goto = op[0]
            car[i].buff = "到达" + str(op[2])
            car[i].lujing.append(str(car[i].buff) + str(car[i].goto))
            car[i].drawpath.append([car[i].x, car[i].y])  # 添加卡车走过的坐标
            car[i].drivedistance += op[1]
            car[i].lastdrive = op[1]

    while (True):
        if (max(coordinates1goods)) == 0:
            return 0
        elif (max(coordinates2goods) == 0):
            return 0

        for i in range(len(truck_coordinates)):  # 开始送货
            if (max(coordinates1goods) == 0):
                return 0
            elif (max(coordinates2goods) == 0):
                return 0
            yusong()


transport()
end_time = datetime.datetime.now()
for i in range(len(truck_coordinates)):
    if (car[i].buff == "到达供应地"):
        car[i].x = car[i].lat_x
        car[i].y = car[i].lat_y
        car[i].drivedistance -= car[i].lastdrive
        car[i].lujing.pop()
        car[i].involume = car[i].lastinvolume
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
print("该次路径需要最短时间为：", max(mintime))

print("需求地物资", coordinates1goods)
print("供应地物资", coordinates2goods)
print()
print('算法时间:', end_time - start_time)
