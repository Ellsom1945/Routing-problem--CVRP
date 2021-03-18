import random
import numpy as np
import math
import turtle as tl

global n, m, u1, u2

coordinates1 = np.array([[200.0, 30.0], [180.0, 70.0], [250.0, 200.0]])  # 需求地坐标
coordinates1goods = np.array([[3], [2], [1]])  # 需求地物资

coordinates2 = np.array([[100.0, 30.0], [70.0, 50.0], [30.0, 100.0]])  # 供应地坐标
coordinates2goods = np.array([[6], [5], [4]])  # 供应地物资

truck_coordinates = [(150, 70), (120, 150)]  # 无人机的【x坐标，y坐标】
dic1 = {0: 0, 1: 0, 2: 0, 3: 1, 4: 1, 5: 2, 6: 0, 7: 0, 8: 1, 9: 1, 10: 2, 11: 2}


def getdistmat(coordinates, coordinates2):
    num1 = coordinates.shape[0]  # 矩阵的行数
    num2 = coordinates2.shape[0]
    distmat = np.zeros((num1, num2))  # 构造全零矩阵
    for i in range(0, num1):
        for j in range(0, num2):  # 利用数组求二范式计算距离
            distmat[i][j] = np.linalg.norm(coordinates[i] - coordinates2[j])
    return distmat


distmat = getdistmat(coordinates2, coordinates1)

n = 50


def init():  # 初始化函数
    global gbest
    for i in range(n):
        spco[i] = 0
        rand(road[i])
        cop(pbestway[i], road[i], m)  # 将局部最优设为初始化的随机解
        pbest[i] = get_value(road[i])
        if (pbest[i] < gbest):
            gbest = pbest[i]
            cop(gbestway, pbestway[i], m)
    return gbest, pbestway, road, spco


e = 0
y = 0


def draw(t):
    i = 0
    tl.setup(700, 700)
    tl.speed(0)
    # 坐标轴
    tl.color("black")
    for z in range(6):
        tl.write("{}".format(z * 50))
        tl.fd(50)
    tl.home()
    tl.left(90)
    for z in range(6):
        tl.write("{}".format(z * 50))
        tl.fd(50)
    tl.right(90)
    # 需求点
    tl.color("blue")
    for h in range(3):
        tl.up()
        tl.goto(coordinates1[h][0], coordinates1[h][1])
        tl.down()
        tl.dot(10)
        tl.write("需求地{}".format(h))
    # 供应点
    tl.color("green")
    for h in range(3):
        tl.up()
        tl.goto(coordinates2[h][0], coordinates2[h][1])
        tl.down()
        tl.dot(10)
        tl.write("供应地{}".format(h))
    # 路线
    tl.color("purple")
    tl.speed(1)
    tl.up()
    tl.goto(truck_coordinates[0][0], truck_coordinates[0][1])
    tl.dot(10)
    tl.down()
    tl.goto(coordinates2[dic1[t[i]]][0], coordinates2[dic1[t[i]]][1])
    i = i + 1
    for j in range(5):
        tl.goto(coordinates1[dic1[t[i]]][0], coordinates1[dic1[t[i]]][1])
        i = i + 1
        if (dic1[t[i]] == 1 or dic1[t[i]] == 2):
            e = dic1[t[i]]
            tl.color("green")
            tl.up()
            tl.goto(truck_coordinates[1][0], truck_coordinates[1][1])
            tl.dot(10)
            tl.down()
            tl.goto(coordinates2[dic1[t[i]]][0], coordinates2[dic1[t[i]]][1])
            y = i - 1
            i = i + 1
            continue
        tl.goto(coordinates2[dic1[t[i]]][0], coordinates2[dic1[t[i]]][1])
        i = i + 1
    tl.goto(coordinates1[dic1[t[i]]][0], coordinates1[dic1[t[i]]][1])


def get_value(t):  # 计算粒子的函数适应值
    ans = 0.0
    a = [0] * m
    for j in range(0, m):
        a[j] = t[j]
    for i in range(1, m, 2):  # 两点距离公式
        ans += distmat[dic1[a[i - 1]]][dic1[a[i]]]
    for i in range(1, 10, 2):
        ans += distmat[dic1[a[i + 1]]][dic1[a[i]]]
    return ans


def cop(a, b, le):  # 把b数组的值赋值a数组
    for i in range(le):
        a[i] = b[i]


def rand(g):  # 随机解生成函数
    j = 0
    vis = [0] * 12
    b = [6, 7, 8, 9, 10, 11]
    random.shuffle(b)
    for i in range(6):
        vis[i] = 0;
    on = 0
    while on < 6:
        te = on
        if (vis[te] == 0):
            vis[te] = 1
            g[on] = te
            on += 1
    for i in range(0, 11, 2):
        g.insert(i, random.randint(6, 11))


def normal(g):
    j = 0
    vis = [0] * 12
    b = [6, 7, 8, 9, 10, 11]
    random.shuffle(b)
    for i in range(6):
        vis[i] = 0;
    on = 0
    while on < 6:
        te = on
        if (vis[te] == 0):
            vis[te] = 1
            g[on] = te
            on += 1
    for i in range(0, 11, 2):
        g.insert(i, b[j])
        j = j + 1


def find(g, ob):  # 在数组g中寻找，值为ob的下标，并返回下标
    for i in range(m):
        if (g[i] == ob):
            return i


def cat(a, c, u):  # 求解a减去解b的交换序结果  将其保存在ss序列 u为保留概率
    global co
    co = 0
    b = [0] * m
    for i in range(m):
        b[i] = c[i]
    ob = 0
    for i in range(m):
        if (a[i] == b[i]):
            continue
        ob = find(b, a[i])
        if ob == None:
            ob = 0
            continue
        if (random.random() < u):
            ss[co] = (i, ob)
            co += 1
        b[i], b[ob] = b[ob], b[i]


def add(g, sv, le):  # 解g加上长度为le的交换序sv
    a = 0
    b = 0
    for i in range(le):
        a = sv[i][0]
        b = sv[i][1]
        g[a], g[b] = g[b], g[a]


def update(i, r):  # 更新i个体的函数适应值
    global gbest
    te = get_value(r)  # 计算适应值
    if (te < pbest[i]):  # 个体最优更新
        pbest[i] = te
        cop(pbestway[i], r, m)
    if (te < gbest):  # 全局最优更新
        gbest = te
        cop(gbestway, r, m)


def slove():  # 执行函数
    global co, gbest, u1, u2
    t1 = [0] * 6
    t2 = [0] * 6
    rand(t1)
    rand(t2)
    u1 = 0.6  # 个体最优交换子保留概率
    u2 = 0.7  # 全局最优交换子保留概率
    for i in range(n):
        for k in range(m):  # 构造两个解t1，t2求基本交换序
            add(t1, speed[i], spco[i])
            cat(pbestway[i], road[i], u1)  # 与个体最优解相减
            add(t1, ss, co)
            cat(gbestway, road[i], u2)  # 与全局最优解相减
            add(t1, ss, co)
            cat(t1, t2, 1)  # 求出基本交换序
            for j in range(co):
                speed[i][j][0] = ss[j][0]
                speed[i][j][1] = ss[j][1]  # 更新个体速度;
                spco[i] = co
                add(road[i], speed[i], spco[i])  # 将速度作用到当前位置
                update(i, road[i])  # 更新函数适应值


m = 12
gbest = 100000
gbestway = [0.0] * m
pbestway = [[0] * (m) for i in range(n)]
pbest = [0.0] * n
road = [[0] * (6) for i in range(n)]

ss = [[0, 0]] * 100
global co
speed = [[[0, 0]] * (300) for i in range(n)]
spco = [0.0] * n
init()  # 数据初始化
for i in range(50):  # 控制迭代次数
    slove()  # 达到最优解提前退出
    print(i)
gbest += np.linalg.norm(truck_coordinates[0] - coordinates2[dic1[gbestway[0]]])
if e == 1 or e == 2:
    gbest += np.linalg.norm(truck_coordinates[1] - coordinates2[e])
    gbest -= np.linalg.norm(coordinates2[e] - coordinates2[y])
draw(gbestway)  # 画图描绘路线
print(gbest)

