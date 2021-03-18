import math
import numpy as np
import matplotlib.pyplot as plt
import random
import turtle
import re

truck_allpath = []
truck_path = []
max_number = []
'''这个程序可以计算出货车承重为1的多辆货车的最短路径，输入需求点和供应点坐标，以及对应的货物量，就能求出最短路径'''
for yp in range(10):

    c_rate = 0.7

    coordinates1 = np.array(
        [[3979, 4854], [2965, 901], [1844, 1979], [2385, 537], [2156, 2169], [2582, 4561], [2920, 4481], [2746, 1749],
         [1116, 364], [736, 2568], [1611, 1313], [3674, 4814], [3556, 3696], [1673, 465], [1304, 510], [365, 3962],
         [2485, 2505], [967, 2414], [4771, 1303], [683, 564], [3876, 2460], [3319, 4193], [3449, 2322], [457, 3422],
         [2702, 3892], [1778, 3699], [2251, 2849], [2384, 1894], [917, 3749], [878, 835], [1841, 1616], [2538, 1560],
         [2582, 3891], [817, 1786], [3040, 2736], [1498, 706], [4851, 4512], [2139, 4515], [89, 1686], [4962, 4457],
         [1275, 5], [1836, 665], [988, 701], [965, 547], [3143, 3909], [1081, 3319], [640, 2566], [1694, 938],
         [4702, 1536], [2826, 4625]])  # 需求地坐标

    coordinates2 = np.array(
        [[3322, 58], [3987, 2398], [3144, 417], [1273, 3380], [2792, 526], [2759, 3258], [2390, 4410], [3368, 2957],
         [841, 4658], [4674, 3347], [2749, 2452], [2237, 3424], [3086, 1432], [2160, 2810], [4622, 766], [3330, 4004],
         [4150, 3170], [3429, 4197], [1991, 2780], [1656, 383], [974, 207], [4907, 1616], [1377, 823], [3214, 4037],
         [4159, 3570], [2296, 14], [3110, 1510], [2577, 2966], [4255, 2547], [2637, 1885], [1406, 4309], [2450, 3962],
         [4295, 1183], [4369, 2409], [939, 967], [3699, 2823], [1711, 2909], [1462, 3568], [793, 4057], [4240, 1848],
         [4410, 2969], [1803, 3053], [1141, 328], [225, 4181], [674, 4990], [3913, 328], [2708, 3970], [3199, 188],
         [3273, 526], [1531, 1774]])  # 供应地坐标

    coordinates1goods = []
    coordinates2goods = []


    def data():
        for i in range(len(coordinates1)):
            coordinates1goods.append(1)  # 首先生成两个个禁忌表，用遗传求出tsp
        for i in range(len(coordinates2)):
            coordinates2goods.append(1)


    data()

    truck_coordinates = [[4292, 4798, 1]]


    class Truck:
        def __init__(self, x, y):
            self.x = x
            self.y = y  # 起点设置为（0，0）
            self.lat_x = 0
            self.lat_y = 0
            self.goto = 0
            self.flag = 0  # 用来计数画图次数
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
        a = sorted(distmat.items(), key=lambda x: x[1])
        for i in range(len(a)):
            p.append(a[i])
        return p


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
                    if (op2 == listtwo[j][0]):  # 利用正则表达式比较地点
                        distance = listtwo[j][1]
                return distance

        distance = 0
        for i in range(len(listone) - 1):
            if (listone[i][0:5] == "到达供应地"):
                distance += soushuo("到达供应地", listone, i)

            if (listone[i][0:5] == "到达需求地"):
                distance += soushuo("到达需求地", listone, i)
        return distance


    def checklist1(checknum):  # 最近供应地坐标
        list = []
        num = []
        for i in range(len(coordinates2)):
            list.append(
                lenth(coordinates1[checknum][0], coordinates1[checknum][1], coordinates2[i][0], coordinates2[i][1]))
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
            list.append(
                lenth(coordinates2[checknum][0], coordinates2[checknum][1], coordinates1[i][0], coordinates1[i][1]))
        for i in range(len(coordinates1)):
            num.append(i)
        k = dict(zip(num, list))
        op = paixudistmat(k)
        return op


    totallist2 = []
    for i in range(len(coordinates2)):
        totallist2.append(checklist2(i))


    def check(text, checknum, totallist1, totallist2):
        if (text == "查找最近的供应地"):
            s = 0
            min = totallist1[checknum][0]
            for i in range(len(coordinates2)):
                if coordinates2goods[totallist1[checknum][i][0]] > 0:
                    s = totallist1[checknum][i][0]
                    min = totallist1[checknum][i][1]
                    return (s, min)

        if (text == "查找最近的需求地"):
            s = 0
            min = totallist2[checknum][0]
            for i in range(len(coordinates1)):
                if coordinates1goods[totallist2[checknum][i][0]] > 0:
                    s = totallist2[checknum][i][0]
                    min = totallist2[checknum][i][1]
                    return (s, min)


    def jisuan(num):
        list = []
        for i in range(len(coordinates2)):
            list.append(lenth(car_init[num].x, car_init[num].y, coordinates2[i][0], coordinates2[i][1]))
        s = 0
        min = list[0]
        for i in range(len(coordinates2)):
            if list[i] < min:
                s = i
                min = list[i]
        return (s, min)  # 返回一个最小距离的下标和距离


    car_init = []
    for i in range(len(truck_coordinates)):
        car_init.append(Truck(truck_coordinates[i][0], truck_coordinates[i][1]))

    for i in range(len(truck_coordinates)):  # 给卡车初始化
        car_init[i].goto = jisuan(i)[0]
        coordinates2goods[car_init[i].goto] = 0
        car_init[i].drivedistance = jisuan(i)[1]
        car_init[i].x = coordinates2[car_init[i].goto][0]
        car_init[i].y = coordinates2[car_init[i].goto][1]
        car_init[i].drawpath.append([car_init[i].x, car_init[i].y])
        car_init[i].goal = "需求地"
        car_init[i].current_capacity = 1
        car_init[i].buff = "到达供应地"
        car_init[i].lujing.append(str(car_init[i].buff) + str(car_init[i].goto))
        print(car_init[i])


    def transport():
        def yusong2():
            op = check("查找最近的供应地", car_init[i].goto, totallist1, totallist2)
            car_init[i].lat_x = car_init[i].x
            car_init[i].lat_y = car_init[i].y
            car_init[i].x = coordinates2[op[0]][0]
            car_init[i].y = coordinates2[op[0]][1]
            car_init[i].goto = op[0]
            car_init[i].buff = "到达供应地"
            car_init[i].goal = "需求地"
            car_init[i].lujing.append(str(car_init[i].buff) + str(car_init[i].goto))
            car_init[i].drawpath.append([car_init[i].x, car_init[i].y])  # 添加卡车走过的坐标
            car_init[i].drivedistance += op[1]
            car_init[i].lastdrive = op[1]
            coordinates2goods[op[0]] -= 1
            car_init[i].goods += 1

        def yusong1():
            op = check("查找最近的需求地", car_init[i].goto, totallist1, totallist2)
            car_init[i].lat_x = car_init[i].x
            car_init[i].lat_y = car_init[i].y
            car_init[i].x = coordinates1[op[0]][0]
            car_init[i].y = coordinates1[op[0]][1]
            car_init[i].goto = op[0]
            car_init[i].buff = "到达需求地"
            car_init[i].goal = "供应地"
            car_init[i].lujing.append(str(car_init[i].buff) + str(car_init[i].goto))
            car_init[i].drawpath.append([car_init[i].x, car_init[i].y])
            car_init[i].drivedistance += op[1]
            car_init[i].lastdrive = op[1]
            coordinates1goods[op[0]] -= 1

        while True:
            if (max(coordinates1goods)) == 0:
                return 0
            elif max(coordinates2goods) == 0:
                return 0

            for i in range(len(truck_coordinates)):  # 开始送货
                if car_init[i].goal == "需求地":
                    if max(coordinates1goods) == 0:
                        return 0
                    elif max(coordinates2goods) == 0:
                        return 0
                    yusong1()
                    yusong2()


    def drawpicture(p):
        color = ['b', 'g', 'r', 'c']
        flt = plt.figure()
        ax = flt.add_subplot(1, 1, 1)
        ax.set_xticks([0, 50, 100, 150, 200, 250, 5000])
        ax.set_yticks([0, 50, 100, 150, 200, 250, 5000])
        for i in range(len(coordinates1)):
            plt.plot(coordinates1[i][0], coordinates1[i][1], 'r', marker='o')  # 红色 需求点坐标为o
        for i in range(len(coordinates2)):
            plt.plot(coordinates2[i][0], coordinates2[i][1], 'b', marker='>')  # 蓝色 供应点坐标为>
        for i in range(len(truck_coordinates)):
            plt.plot(truck_coordinates[i][0], truck_coordinates[i][1], 'black', marker='1')  # 黑色 汽车初始位置
        for j in range(len(car_init[p].drawpath) - 1):
            plt.plot((car_init[p].drawpath[j][0], car_init[p].drawpath[j + 1][0]),
                     (car_init[p].drawpath[j][1], car_init[p].drawpath[j + 1][1]), color[p % 4])
        plt.title('car_init: ' + str(p), fontsize=30)
        plt.show()
        plt.close()


    def drawpicture2(p):
        t = []
        colors = ["green", "blue", "red", "orange", "purple"]
        name = ["classic", "arrow", "square", "circle", "turtle", "triangle"]
        t1 = turtle.Pen()
        t1.speed(1)
        for i in range(len(coordinates1)):
            t1.penup()
            t1.goto(coordinates1[i][0], coordinates1[i][1])
            t1.write("需求地" + str(i), align="center", font=("Arial", 8))
            t1.dot(5, "blue")
        for i in range(len(coordinates2)):
            t1.goto(coordinates2[i][0], coordinates2[i][1])
            t1.write("供应地" + str(i), align="center", font=("Arial", 8))
            t1.dot(5, "green")

        for i in range(6):
            if i == 0:
                t1.penup()
                t1.goto(i * 50, 0)
            else:
                t1.pendown()
                t1.goto(i * 50, 0)
                t1.write('*', font=("Arial Rounded", 5, "normal"))
                t1.write(str(i * 50))

        t1.goto(0, 0)
        t1.pendown()

        for i in range(6):
            t1.goto(0, i * 50)
            t1.write('*', font=("Arial Rounded", 5, "normal"))
            t1.write(str(i * 50))
        t1.hideturtle()
        for i in range(p):
            t.append(turtle.Pen())
            t[i].shape()
            t[i].shape(name[i % 6])
            t[i].pencolor(colors[i % 5])
            t[i].speed(1)
        for i in range(p):
            if i == 0:
                t[i + 1].hideturtle()
            flag2 = 1
            while flag2:
                if car_init[i].flag == 0:
                    t[i].penup()
                    t[i].hideturtle()
                    t[i].goto(car_init[i].drawpath[car_init[i].flag][0], car_init[i].drawpath[car_init[i].flag][1])
                    t[i].showturtle()
                    t[i].pendown()
                    t[i].dot(5, "black")
                    car_init[i].flag += 1
                    if car_init[i].flag >= len(car_init[i].drawpath):
                        flag2 = 0

                else:
                    angle = math.degrees(math.atan(
                        (car_init[i].drawpath[car_init[i].flag][1] - car_init[i].drawpath[car_init[i].flag - 1][1]) / (
                                car_init[i].drawpath[car_init[i].flag][0] -
                                car_init[i].drawpath[car_init[i].flag - 1][0])))
                    if (((car_init[i].drawpath[car_init[i].flag][1] - car_init[i].drawpath[car_init[i].flag - 1][
                        1]) <= 0 and (
                                 car_init[i].drawpath[car_init[i].flag][0] - car_init[i].drawpath[car_init[i].flag - 1][
                             0])) < 0):
                        angle = 180 + angle
                    t[i].setheading(angle)
                    t[i].goto(car_init[i].drawpath[car_init[i].flag][0], car_init[i].drawpath[car_init[i].flag][1])
                    car_init[i].flag += 1
                    if car_init[i].flag >= len(car_init[i].drawpath):
                        flag2 = 0


    transport()
    for i in range(len(coordinates1goods)):
        if coordinates1goods[i] != 0:
            car_init[0].lujing.append("到达需求地" + str(i))
            car_init[0].x = coordinates1[i][0]
            car_init[0].y = coordinates1[i][1]
            car_init[0].goods += 1
            car_init[0].drawpath.append([car_init[0].x, car_init[0].y])
            car_init[0].drivedistance += lenth(car_init[0].x, car_init[0].y,
                                               car_init[0].drawpath[len(car_init[0].drawpath) - 2][0],
                                               car_init[0].drawpath[len(car_init[0].drawpath) - 2][1])

    for i in range(len(truck_coordinates)):  # 2是汽车数量，可以统计汽车输入的个数，将其换为变量
        print("卡车：" + str(i))
        print(car_init[i])
        print(car_init[i].lujing)
        print("卡车的路径坐标表:", car_init[i].drawpath)
        print('\n')

    mintime = []
    for i in range(len(truck_coordinates)):
        mintime.append(car_init[i].drivedistance)
    print("需要最短时间为：", max(mintime))

    coordinates1goods = []

    coordinates2goods = []

    data()

    truck_coordinates = [[4292, 4798, 1]]


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
            self.buff = "待命"
            self.lujing = []
            self.drawpath = [[x, y]]
            self.lastdrive = 0
            self.current_capacity = 0  # 当前运载的货量

        def __str__(self):
            return '坐标: [{},{}],{}：{}当前运载的货量: {} 总共走了{}距离 正在前往{} 已经装运{}  汽车容量为{}/{}'. \
                format(self.x, self.y, self.buff, self.goto, self.current_capacity, self.drivedistance, self.goal,
                       self.goods, self.involume, self.volume)


    def select(text, checknum, totallist1, totallist2):  # 轮盘赌法选择目标点
        sum = 0  # 距离越远，物资越少，去的概率越低
        coordinates1Arrivable = []
        if text == "查找下一个供应地":
            for i in range(len(totallist1[checknum])):
                sum = sum + (coordinates2goods[totallist1[checknum][i][0]] / totallist1[checknum][i][1])
            for i in range(len(totallist1[checknum])):
                coordinates1Arrivable.append((totallist1[checknum][i][0], (
                        coordinates2goods[totallist1[checknum][i][0]] / totallist1[checknum][i][
                    1]) / sum))  # 元组第一个是下标，第二个是到达的概率
            r_ = 0
            ran = random.random()
            for i in range(len(coordinates1Arrivable)):
                r_ += coordinates1Arrivable[i][1]
                if ran < r_:  break
            return coordinates1Arrivable[i][0]

        if text == "查找下一个需求地":
            for i in range(len(totallist2[checknum])):
                sum = sum + (coordinates1goods[totallist2[checknum][i][0]] / totallist2[checknum][i][1])
            for i in range(len(totallist2[checknum])):
                coordinates1Arrivable.append((totallist2[checknum][i][0], (
                        coordinates1goods[totallist2[checknum][i][0]] / totallist2[checknum][i][
                    1]) / sum))  # 元组第一个是下标，第二个是到达的概率
            r_ = 0
            ran = random.random()
            for i in range(len(coordinates1Arrivable)):
                r_ += coordinates1Arrivable[i][1]
                if ran < r_:
                    break
            return coordinates1Arrivable[i][0]


    def check(text, checknum, totallist1, totallist2, volume, carnumber):  # 根据概率进行对目标点的选择和修改（因为选择的地点物资可能会出现0）
        if text == "查找下一个供应地":
            s = 0
            min = totallist1[checknum][0]
            flag = 1
            while flag == 1:
                i = select("查找下一个供应地", checknum, totallist1, totallist2)
                if coordinates2goods[i] > 0:
                    flag = 0
            s = i
            for i in range(len(totallist1[checknum])):
                if totallist1[checknum][i][0] == s:
                    min = totallist1[checknum][i][1]
            if coordinates2goods[s] >= car[carnumber].volume - volume:  # 供应物资》车载空的物资时，供应物资减去车载物资，车载物资变满
                coordinates2goods[s] -= car[carnumber].volume - volume
                car[carnumber].lastinvolume = car[carnumber].involume
                car[carnumber].involume = car[carnumber].volume

            else:  # 供应物资《车载物资时，车载物资加上供应物资，供应物资为0
                car[carnumber].lastinvolume = car[carnumber].involume
                car[carnumber].involume += coordinates2goods[s]
                coordinates2goods[s] = 0
            return (s, min)

        if text == "查找下一个需求地":
            s = 0
            min = totallist2[checknum][0]
            flag = 1
            while flag == 1:
                i = select("查找下一个需求地", checknum, totallist1, totallist2)
                if coordinates1goods[i] > 0:
                    flag = 0
            s = i
            for i in range(len(totallist2[checknum])):
                if totallist2[checknum][i][0] == s:
                    min = totallist2[checknum][i][1]
            if coordinates1goods[s] >= volume:  # 需求的物资>车载物资时，需求物资减去车载物资，车载物资为0
                coordinates1goods[s] -= volume
                car[carnumber].lastinvolume = car[carnumber].involume
                car[carnumber].involume = 0
            else:  # 需求的物资《车载物资时，车载物资减去需求物资，需求物资为0
                car[carnumber].lastinvolume = car[carnumber].involume
                car[carnumber].involume -= coordinates1goods[s]
                coordinates1goods[s] = 0

            return (s, min)


    def jisuan(num):
        list = []
        for i in range(len(coordinates2)):
            list.append(lenth(car[num].x, car[num].y, coordinates2[i][0], coordinates2[i][1]))
        # print(list)
        s = 0
        min = list[0]
        for i in range(len(coordinates2)):
            if list[i] < min:
                s = i
                min = list[i]
        return (s, min)  # 返回一个最小距离的下标和距离


    def transport():
        def yusong2():
            op = check("查找下一个供应地", car[i].goto, totallist1, totallist2, car[i].involume, i)
            car[i].lat_x = car[i].x
            car[i].lat_y = car[i].y
            car[i].x = coordinates2[op[0]][0]
            car[i].y = coordinates2[op[0]][1]
            car[i].goto = op[0]
            car[i].buff = "到达供应地"
            car[i].goal = "需求地"
            car[i].lujing.append(str(car[i].buff) + str(car[i].goto))
            car[i].drawpath.append([car[i].x, car[i].y])  # 添加卡车走过的坐标
            car[i].drivedistance += op[1]
            car[i].lastdrive = op[1]
            car[i].goods += car[i].volume

        def yusong1():
            op = check("查找下一个需求地", car[i].goto, totallist1, totallist2, car[i].involume, i)
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

        while True:
            if (max(coordinates1goods)) == 0:
                return 0
            elif max(coordinates2goods) == 0:
                return 0

            for i in range(len(truck_coordinates)):  # 开始送货
                if car[i].goal == "需求地":
                    if max(coordinates1goods) == 0:
                        return 0
                    elif max(coordinates2goods) == 0:
                        return 0
                    yusong1()
                    yusong2()


    def cross(parent1, parent2):  # parent1是要交换的基因    函数填（当前基因，之前基因）
        if np.random.rand() > c_rate:
            return parent1
        index1 = np.random.randint(0, len(parent1))
        index2 = np.random.randint(index1, len(parent1))
        tempcar1 = parent1[index1:index2]
        tempcar2 = parent2[index1:index2]  # parent2 給 parant1交叉的基因片段
        if tempcar1 == tempcar2:
            return parent1
        difference1 = list(set(tempcar1) - set(tempcar2))  # 差集，在tempGen1中但不在tempGen2中的元素
        difference2 = list(set(tempcar2) - set(tempcar1))  # 差集，在tempcar2中但不在tempcar1中的元素
        if len(difference1) == 0:
            return parent1

        else:
            k = 0
            for i in range(len(tempcar2)):
                parent1[index1 + i] = tempcar2[i]
            for i in range(0, index1):
                for j in range(len(difference2)):
                    if parent1[i] == difference2[j]:
                        if k < len(difference1) - 1:
                            parent1[i] = difference1[k]
                            k = k + 1
            for i in range(index2, len(parent1) - 1):
                for j in range(len(difference2)):
                    if parent1[i] == difference2[j]:
                        if k < len(difference1) - 1:
                            parent1[i] = difference1[k]
                            k = k + 1
            return parent1


    def drawpicture(p):
        color = ['b', 'g', 'r', 'c']
        for i in range(len(coordinates1)):
            plt.plot(coordinates1[i][0], coordinates1[i][1], 'r', marker='o')  # 红色 需求点坐标为o
        for i in range(len(coordinates2)):
            plt.plot(coordinates2[i][0], coordinates2[i][1], 'b', marker='>')  # 蓝色 供应点坐标为>
        for i in range(len(truck_coordinates)):
            plt.plot(truck_coordinates[i][0], truck_coordinates[i][1], 'black', marker='1')  # 黑色 汽车初始位置
        for j in range(len(car[p].drawpath) - 1):
            plt.plot((car[p].drawpath[j][0], car[p].drawpath[j + 1][0]),
                     (car[p].drawpath[j][1], car[p].drawpath[j + 1][1]), color[p % 4])
        plt.title('car: ' + str(p), fontsize=30)
        plt.show()
        plt.close()


    allmintime = []
    alllujing = []
    for up in range(200):
        global car
        car = []
        for i in range(len(truck_coordinates)):
            car.append(Truck(truck_coordinates[i][0], truck_coordinates[i][1], truck_coordinates[i][2]))

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
            if max(coordinates1goods) > 0:
                up = up - 1
            allmintime.append(max(mintime))
            print("该次路径需要最短时间为：", min(allmintime))

            op = len(allmintime)
            if (op > 1):
                if allmintime[op - 2] > allmintime[op - 1]:
                    new_lujing = cross(car_init[0].drawpath, alllujing[op - 1])
                    print("新的路径", new_lujing)
                    new_mintime = sousuodistance((new_lujing))
                    if new_mintime < allmintime[op - 1]:
                        alllujing[op - 2] = new_mintime
        for i in range(len(truck_coordinates)):
            if car[i].buff == "到达供应地":
                car[i].x = car[i].lat_x
                car[i].y = car[i].lat_y
                car[i].drivedistance -= car[i].lastdrive
                car[i].lujing.pop()
                car[i].involume = car[i].lastinvolume
                car[i].drawpath.pop()

        mintime = []
        for i in range(len(truck_coordinates)):
            mintime.append(car[i].drivedistance)
        alllujing.append(car[0].lujing)
        allmintime.append(max(mintime))

        print("该次路径需要最短时间为：", min(allmintime))

        print("\n第{}次运输\n".format(up))

        coordinates1 = np.array(
            [[3979, 4854], [2965, 901], [1844, 1979], [2385, 537], [2156, 2169], [2582, 4561], [2920, 4481],
             [2746, 1749],
             [1116, 364], [736, 2568], [1611, 1313], [3674, 4814], [3556, 3696], [1673, 465], [1304, 510], [365, 3962],
             [2485, 2505], [967, 2414], [4771, 1303], [683, 564], [3876, 2460], [3319, 4193], [3449, 2322], [457, 3422],
             [2702, 3892], [1778, 3699], [2251, 2849], [2384, 1894], [917, 3749], [878, 835], [1841, 1616],
             [2538, 1560],
             [2582, 3891], [817, 1786], [3040, 2736], [1498, 706], [4851, 4512], [2139, 4515], [89, 1686], [4962, 4457],
             [1275, 5], [1836, 665], [988, 701], [965, 547], [3143, 3909], [1081, 3319], [640, 2566], [1694, 938],
             [4702, 1536], [2826, 4625]])  # 需求地坐标
        coordinates1goods = []

        coordinates2 = np.array(
            [[3322, 58], [3987, 2398], [3144, 417], [1273, 3380], [2792, 526], [2759, 3258], [2390, 4410], [3368, 2957],
             [841, 4658], [4674, 3347], [2749, 2452], [2237, 3424], [3086, 1432], [2160, 2810], [4622, 766],
             [3330, 4004],
             [4150, 3170], [3429, 4197], [1991, 2780], [1656, 383], [974, 207], [4907, 1616], [1377, 823], [3214, 4037],
             [4159, 3570], [2296, 14], [3110, 1510], [2577, 2966], [4255, 2547], [2637, 1885], [1406, 4309],
             [2450, 3962],
             [4295, 1183], [4369, 2409], [939, 967], [3699, 2823], [1711, 2909], [1462, 3568], [793, 4057],
             [4240, 1848],
             [4410, 2969], [1803, 3053], [1141, 328], [225, 4181], [674, 4990], [3913, 328], [2708, 3970], [3199, 188],
             [3273, 526], [1531, 1774]])  # 供应地坐标
        coordinates2goods = []  # 供应地物资
        data()
        truck_coordinates = [[4292, 4798, 1]]

    min_time = min(allmintime)  # 最短时间
    number = np.argmin(allmintime)  # 该次趟数

    l1 = alllujing[int(np.argmin(allmintime))]
    lst = []
    for el in l1:
        if lst.count(el) < 1:
            lst.append(el)


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


    coordinates1goods = np.array(
        [5, 2, 5, 2, 10, 2, 6, 8, 1, 8, 8, 3, 9, 5, 7, 2, 8, 2, 2, 8, 9, 2, 10, 10, 4, 8, 8, 8, 6, 9, 2, 1, 3, 4, 5, 6,
         3, 9, 7, 10, 10, 8, 6, 6, 4, 9, 8, 9, 9, 6])

    coordinates2goods = np.array(
        [7, 3, 5, 10, 10, 8, 4, 1, 7, 4, 2, 8, 10, 1, 8, 3, 1, 5, 6, 4, 5, 10, 6, 3, 10, 9, 10, 1, 6, 5, 10, 10, 1, 4,
         5, 1, 1, 10, 6, 8, 1, 7, 10, 6, 6, 9, 5, 2, 7, 3])  # 供应地物资

    truck_coordinates = [[4292, 4798, 1], [2403, 1155, 1], [852, 4540, 1], [411, 4568, 1], [4389, 1851, 1]]

    truck = []
    for i in range(len(truck_coordinates)):
        truck.append(Truck2(truck_coordinates[i][0], truck_coordinates[i][1], truck_coordinates[i][2]))


    def fengge():
        new_flag = 0
        op = len(lst) // 5
        x0 = sousuodistance(lst)
        x1 = sousuodistance(lst) // 5
        for i in range(op):
            truck[0].lujing.append(lst[i])
        while x1 - sousuodistance(truck[0].lujing) > 0.014 * x0:
            i = i + 1
            truck[0].lujing.append(lst[i])
        while sousuodistance(truck[0].lujing) - x1 > 0.014 * x0:
            i = i - 1
            truck[0].lujing.pop()
        new_flag = i

        for i in range(op):
            truck[1].lujing.append(lst[i + new_flag])
        while x1 - sousuodistance(truck[1].lujing) > 0.014 * x0:
            i = i + 1
            truck[1].lujing.append(lst[i])
        while sousuodistance(truck[1].lujing) - x1 > 0.014 * x0:
            i = i - 1
            truck[1].lujing.pop()
        new_flag = i

        for i in range(op):
            truck[2].lujing.append(lst[i + new_flag])
        while x1 - sousuodistance(truck[2].lujing) > 0.014 * x0:
            i = i + 1
            truck[2].lujing.append(lst[i])
        while sousuodistance(truck[2].lujing) - x1 > 0.014 * x1:
            i = i - 1
            truck[2].lujing.pop()
        new_flag = i

        for i in range(op):
            truck[3].lujing.append(lst[i + new_flag])
        while x1 - sousuodistance(truck[3].lujing) > 0.014 * x0:
            i = i + 1
            truck[3].lujing.append(lst[i])
        while sousuodistance(truck[3].lujing) - x1 > 0.014 * x0:
            i = i - 1
            truck[3].lujing.pop()
        new_flag = i

        for i in range(op):
            truck[4].lujing.append(lst[i + new_flag])

        for i in range(len(truck_coordinates)):
            print("无人机", i, "路径:", truck[i].lujing)
            print(sousuodistance(truck[i].lujing))


    def truck_transport(i):  # i为无人机编号            根据路径运输
        if truck[i].lujing[0][0:5] == "到达供应地":
            for k in range(len(truck[i].lujing) - 1):
                if k % 2 == 0:
                    op1 = int(re.findall("\d+", truck[i].lujing[k])[0])
                    op2 = int(re.findall("\d+", truck[i].lujing[k + 1])[0])
                else:
                    op2 = int(re.findall("\d+", truck[i].lujing[k])[0])
                    op1 = int(re.findall("\d+", truck[i].lujing[k + 1])[0])
                if coordinates2goods[op1] > 0 and coordinates1goods[op2] > 0:
                    if coordinates2goods[op1] >= coordinates1goods[op2]:
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
                if k % 2 == 0:
                    op1 = int(re.findall("\d+", truck[i].lujing[k])[0])
                    op2 = int(re.findall("\d+", truck[i].lujing[k + 1])[0])
                else:
                    op2 = int(re.findall("\d+", truck[i].lujing[k])[0])
                    op1 = int(re.findall("\d+", truck[i].lujing[k + 1])[0])
                if coordinates1goods[op1] > 0 and coordinates2goods[op2] > 0:
                    if coordinates1goods[op1] >= coordinates2goods[op2]:
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


    truck[0].lujing = lst
    truck_transport(0)

    lst = truck[0].last_lujing
    truck[0].lujing.clear()
    fengge()

    distance = []
    for i in range(len(truck_coordinates)):
        distance.append(sousuodistance(truck[i].lujing))
    max_number.append(max(distance))
print("完成运输至少需要时间：", min(max_number))
print(max_number.index(min(max_number)))
