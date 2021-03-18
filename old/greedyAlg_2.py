import math
import numpy as np
import matplotlib.pyplot as plt
import random
import datetime

start_time = datetime.datetime.now()

'''这个程序可以计算出货车承重为1的多辆货车的最短路径，输入需求点和供应点坐标，以及对应的货物量，就能求出最短路径'''

coordinates1 = np.array([[3979, 4854], [2965, 901], [1844, 1979], [2385, 537], [2156, 2169], [2582, 4561], [2920, 4481], [2746, 1749], [1116, 364], [736, 2568], [1611, 1313], [3674, 4814], [3556, 3696], [1673, 465], [1304, 510], [365, 3962], [2485, 2505], [967, 2414], [4771, 1303], [683, 564], [3876, 2460], [3319, 4193], [3449, 2322], [457, 3422], [2702, 3892], [1778, 3699], [2251, 2849], [2384, 1894], [917, 3749], [878, 835], [1841, 1616], [2538, 1560], [2582, 3891], [817, 1786], [3040, 2736], [1498, 706], [4851, 4512], [2139, 4515], [89, 1686], [4962, 4457], [1275, 5], [1836, 665], [988, 701], [965, 547], [3143, 3909], [1081, 3319], [640, 2566], [1694, 938], [4702, 1536], [2826, 4625]])      #需求地坐标
coordinates1goods=np.array([5, 2, 5, 2, 10, 2, 6, 8, 1, 8, 8, 3, 9, 5, 7, 2, 8, 2, 2, 8, 9, 2, 10, 10, 4, 8, 8, 8, 6, 9, 2, 1, 3, 4, 5, 6, 3, 9, 7, 10, 10, 8, 6, 6, 4, 9, 8, 9, 9, 6])

coordinates2 = np.array([[3322, 58], [3987, 2398], [3144, 417], [1273, 3380], [2792, 526], [2759, 3258], [2390, 4410], [3368, 2957], [841, 4658], [4674, 3347], [2749, 2452], [2237, 3424], [3086, 1432], [2160, 2810], [4622, 766], [3330, 4004], [4150, 3170], [3429, 4197], [1991, 2780], [1656, 383], [974, 207], [4907, 1616], [1377, 823], [3214, 4037], [4159, 3570], [2296, 14], [3110, 1510], [2577, 2966], [4255, 2547], [2637, 1885], [1406, 4309], [2450, 3962], [4295, 1183], [4369, 2409], [939, 967], [3699, 2823], [1711, 2909], [1462, 3568], [793, 4057], [4240, 1848], [4410, 2969], [1803, 3053], [1141, 328], [225, 4181], [674, 4990], [3913, 328], [2708, 3970], [3199, 188], [3273, 526], [1531, 1774]])   #供应地坐标
coordinates2goods=np.array([7, 3, 5, 10, 10, 8, 4, 1, 7, 4, 2, 8, 10, 1, 8, 3, 1, 5, 6, 4, 5, 10, 6, 3, 10, 9, 10, 1, 6, 5, 10, 10, 1, 4, 5, 1, 1, 10, 6, 8, 1, 7, 10, 6, 6, 9, 5, 2, 7, 3])        #供应地物资

truck_coordinates=[[4292, 4798], [2403, 1155], [852, 4540], [411, 4568], [4389, 1851]]


class Truck:
    def __init__(self,x,y):
        self.x = x
        self.y = y     #起点设置为（0，0）
        self.lat_x=0
        self.lat_y=0
        self.goto=0
        self.drivedistance=0.0
        self.goal="供应地"
        self.goods=0
        self.buff="待命"
        self.lujing=[]
        self.drawpath=[[x,y]]
        self.lastdrive=0
        self.current_capacity = 0  # 当前运载的货量

    def __str__(self):
        return '坐标: [{},{}],{}：{}当前运载的货量: {} 总共走了{}距离 正在前往{} 已经装运{}'. \
            format(self.x, self.y,self.buff,self.goto,self.current_capacity,self.drivedistance,self.goal,self.goods)

def lenth(x1, y1, x2, y2):
    return math.sqrt((int(x1) - int(x2)) ** 2 + (int(y1) - int(y2)) ** 2)           #用于计算路径表

def paixudistmat(distmat):                #返回一个最近坐标表
    p=[]
    #print(distmat[n].items())
    a = sorted(distmat.items(), key=lambda x: x[1])
    #print(a)
    for i in range(len(a)):
        p.append(a[i])
    return p

def checklist1(checknum):                       #最近供应地坐标
    list=[]
    num=[]
    for i in range(len(coordinates2)):
        list.append(lenth(coordinates1[checknum][0], coordinates1[checknum][1], coordinates2[i][0], coordinates2[i][1]))
    for i in range(len(coordinates2)):
        num.append(i)
    k = dict(zip(num, list))
    op = paixudistmat(k)
    return op

totallist1=[]
for i in range(len(coordinates1)):
    totallist1.append(checklist1(i))

def checklist2(checknum):                   #最近需求地坐标
    list=[]
    num=[]
    for i in range(len(coordinates1)):
        list.append(lenth(coordinates2[checknum][0], coordinates2[checknum][1], coordinates1[i][0], coordinates1[i][1]))
    for i in range(len(coordinates1)):
        num.append(i)
    k=dict(zip(num,list))
    op=paixudistmat(k)
    return  op

totallist2=[]
for i in range(len(coordinates2)):
    totallist2.append(checklist2(i))

def check(text,checknum,totallist1,totallist2):
    if(text=="查找最近的供应地"):
        s=0
        min=totallist1[checknum][0]
        for i in range(len(coordinates2)):
            if coordinates2goods[totallist1[checknum][i][0]]>0:
                s = totallist1[checknum][i][0]
                min = totallist1[checknum][i][1]
                return(s,min)

    if(text=="查找最近的需求地"):
        s=0
        min=totallist2[checknum][0]
        for i in range(len(coordinates1)):
            if coordinates1goods[totallist2[checknum][i][0]]>0:
                s=totallist2[checknum][i][0]
                min=totallist2[checknum][i][1]
                return (s,min)

#print(check("查找最近的需求地",0,totallist1,totallist2)) #      第一个参数是（查找） 第二个参数是 当前点序号  之后参数固定

def jisuan(num):
    list=[]
    for i in range(len(coordinates2)):
        #print(car[num].x,car[num].y, coordinates2[i][0],coordinates2[i][1])
        list.append(lenth(car[num].x,car[num].y, coordinates2[i][0],coordinates2[i][1]))
    #print(list)
    s=0
    min=list[0]
    for i in range(len(coordinates2)):
        if list[i]<min:
            s=i
            min=list[i]
    return (s,min)                          #返回一个最小距离的下标和距离

car=[]
for i in range(len(truck_coordinates)):
    car.append(Truck(truck_coordinates[i][0],truck_coordinates[i][1]))

for i in range(len(truck_coordinates)):                  #给卡车初始化
    car[i].goto=jisuan(i)[0]
    car[i].drivedistance=jisuan(i)[1]
    car[i].x=coordinates2[car[i].goto][0]
    car[i].y = coordinates2[car[i].goto][1]
    car[i].drawpath.append([car[i].x,car[i].y])
    car[i].goal="需求地"
    car[i].current_capacity=1
    car[i].buff="到达供应地"
    car[i].lujing.append(str(car[i].buff)+str(car[i].goto))
    print(car[i])

def transport():
    def yusong2():
        op = check("查找最近的供应地", car[i].goto,totallist1,totallist2)
        car[i].lat_x = car[i].x
        car[i].lat_y = car[i].y
        car[i].x = coordinates2[op[0]][0]
        car[i].y = coordinates2[op[0]][1]
        #print(car[i].x,car[i].y)
        car[i].goto = op[0]
        car[i].buff = "到达供应地"
        car[i].goal = "需求地"
        car[i].lujing.append(str(car[i].buff) + str(car[i].goto))
        car[i].drawpath.append([car[i].x,car[i].y])                 #添加卡车走过的坐标
        car[i].drivedistance += op[1]
        car[i].lastdrive=op[1]
        coordinates2goods[op[0]] -= 1
        car[i].goods += 1
        #print(car[i])

    def yusong1():
        op = check("查找最近的需求地", car[i].goto,totallist1,totallist2)
        car[i].lat_x = car[i].x
        car[i].lat_y = car[i].y
        car[i].x = coordinates1[op[0]][0]
        car[i].y = coordinates1[op[0]][1]
        car[i].goto = op[0]
        car[i].buff = "到达需求地"
        car[i].goal = "供应地"
        car[i].lujing.append(str(car[i].buff) + str(car[i].goto))
        car[i].drawpath.append([car[i].x,car[i].y])
        car[i].drivedistance += op[1]
        car[i].lastdrive=op[1]
        coordinates1goods[op[0]] -= 1
        #print(car[i])

    while(True):
        if(max(coordinates1goods))==0:
            return 0
        elif(max(coordinates2goods)==0):
            return 0

        for i in range(len(truck_coordinates)):          #开始送货
            if(car[i].goal=="需求地"):
                if (max(coordinates1goods) == 0):
                    return 0
                elif (max(coordinates2goods) == 0):
                    return 0
                yusong1()
                yusong2()

def drawpicture(p):
    color = ['b', 'g', 'r', 'c']
    for i in range(len(coordinates1)):
        plt.plot(coordinates1[i][0],coordinates1[i][1],'r',marker='o')   #红色 需求点坐标为o
    for i in range(len(coordinates2)):
        plt.plot(coordinates2[i][0],coordinates2[i][1],'b',marker='>')    #蓝色 供应点坐标为>
    for i in range(len(truck_coordinates)):
        plt.plot(truck_coordinates[i][0],truck_coordinates[i][1],'black',marker='1')   #黑色 汽车初始位置
    for j in range (len(car[p].drawpath)-1):
        plt.plot((car[p].drawpath[j][0], car[p].drawpath[j + 1][0]), (car[p].drawpath[j][1], car[p].drawpath[j + 1][1]), color[p%4])
    plt.title('car: '+str(p),fontsize=30)
    #plt.title(r'$hello\ world$', fontsize=30)
    plt.show()
    plt.close()

transport()
end_time = datetime.datetime.now()
for i in range(len(truck_coordinates)):
    if(car[i].buff=="到达供应地"):
        car[i].x=car[i].lat_x
        car[i].y=car[i].lat_y
        car[i].drivedistance-=car[i].lastdrive
        car[i].lujing.pop()
        car[i].drawpath.pop()

for i in range(len(truck_coordinates)):                  #2是汽车数量，可以统计汽车输入的个数，将其换为变量
    print("卡车："+str(i))
    print(car[i])
    print(car[i].lujing)
    print("卡车的路径坐标表:",car[i].drawpath)
    print('\n')

mintime=[]
for i in range(len(truck_coordinates)):
    mintime.append(car[i].drivedistance)
print("需要最短时间为：",max(mintime))

for p in range(len(truck_coordinates)):
    drawpicture(p)

#print("需求地物资",coordinates1goods)
#print("供应地物资",coordinates2goods)
print()
print('算法时间:', end_time - start_time)

'''判断结束的条件是，需求地或者供应地有一方物资全为0'''