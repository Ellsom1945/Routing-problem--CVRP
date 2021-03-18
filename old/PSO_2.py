import random
import numpy as np
import math
import turtle as tl

global n, m, u1, u2

coordinates1 = np.array([[3979, 4854], [2965, 901], [1844, 1979], [2385, 537], \
                         [2156, 2169], [2582, 4561], [2920, 4481], [2746, 1749], [1116, 364], [736, 2568], \
                         [1611, 1313], [3674, 4814], [3556, 3696], [1673, 465], [1304, 510], [365, 3962], \
                         [2485, 2505], [967, 2414], [4771, 1303], [683, 564], [3876, 2460], [3319, 4193], \
                         [3449, 2322], [457, 3422], [2702, 3892], [1778, 3699], [2251, 2849], [2384, 1894], \
                         [917, 3749], [878, 835], [1841, 1616], [2538, 1560], [2582, 3891], [817, 1786], \
                         [3040, 2736], [1498, 706], [4851, 4512], [2139, 4515], [89, 1686], [4962, 4457], \
                         [1275, 5], [1836, 665], [988, 701], [965, 547], [3143, 3909], [1081, 3319], \
                         [640, 2566], [1694, 938], [4702, 1536], [2826, 4625]])  # 需求地坐标
coordinates1goods = [5, 2, 5, 2, 10, 2, 6, 8, 1, 8, 8, 3, 9, 5, 7, 2, 8, 2, 2 \
    , 8, 9, 2, 10, 10, 4, 8, 8, 8, 6, 9, 2, 1, 3, 4, 5, 6, 3, \
                     9, 7, 10, 10, 8, 6, 6, 4, 9, 8, 9, 9, 6]

coordinates2 = np.array([[3322, 58], [3987, 2398], [3144, 417], [1273, 3380], [2792, 526], [2759, 3258], [2390, 4410], [3368, 2957], [841, 4658], [4674, 3347], [2749, 2452], [2237, 3424],
                         [3086, 1432], [2160, 2810], [4622, 766], [3330, 4004], [4150, 3170], [3429, 4197], [1991, 2780], [1656, 383], [974, 207],
                         [4907, 1616], [1377, 823], [3214, 4037], [4159, 3570], [2296, 14], [3110, 1510], [2577, 2966], [4255, 2547],
                         [2637, 1885], [1406, 4309], [2450, 3962], [4295, 1183], [4369, 2409], [939, 967], [3699, 2823], [1711, 2909],
                         [1462, 3568], [793, 4057], [4240, 1848], [4410, 2969], [1803, 3053], [1141, 328], [225, 4181], [674, 4990],
                         [3913, 328], [2708, 3970], [3199, 188], [3273, 526], [1531, 1774]])  # 供应地坐标
coordinates2goods = [7, 3, 5, 10, 10, 8, 4, 1, 7, 4, 2, 8, 10, 1, 8, 3, 1, 5, 6, 4, 5, 10, 6, 3, 10, \
                     9, 10, 1, 6, 5, 10, 10, 1, 4, 5, 1, 1, 10, 6, 8, 1, 7, 10, 6, 6, 9, 5, 2, 7, 3]  # 供应地物资

m = sum(coordinates1goods) * 2
dic1 = {}  # 需求地
j = 0
keys = list(range(coordinates1.shape[0]))
values = list(range(sum(coordinates1goods)))
for i in range(coordinates1.shape[0]):
    for h in range(coordinates1goods[i]):
        dic1.setdefault(keys[i], []).append(values[j])
        j += 1

dic2 = {}  # 供应地
j = 0
keys = list(range(coordinates2.shape[0]))
values = list(range(sum(coordinates1goods), sum(coordinates1goods) * 2))
for i in range(coordinates2.shape[0]):
    j = i
    for h in range(coordinates2goods[i]):
        dic2.setdefault(keys[i], []).append(values[j])
        j += 50
        if (j > 300):
            break


def getkey(dict, values):
    f = list(dict.values())
    for i in range(len(f)):
        for j in range(len(f[i])):
            if (f[i][j] == values):
                return i


def getdistmat(coordinates, coordinates2):
    num1 = coordinates.shape[0]  # 矩阵的行数
    num2 = coordinates2.shape[0]
    distmat = np.zeros((num1, num2))  # 构造全零矩阵
    for i in range(0, num1):
        for j in range(0, num2):  # 利用数组求二范式计算距离
            distmat[i][j] = np.linalg.norm(coordinates[i] - coordinates2[j])
    return distmat


distmat = getdistmat(coordinates2, coordinates1)

n = 10


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


def get_value(t):  # 计算粒子的函数适应值
    ans = 0.0
    a = [0] * m
    for j in range(0, m):
        a[j] = t[j]
    for i in range(1, m, 2):  # 两点距离公式
        while getkey(dic2, a[i - 1]) == None:
            a[i - 1] = a[i - 1] - 50
        ans += distmat[getkey(dic2, a[i - 1])][getkey(dic1, a[i])]
    for i in range(1, m - 2, 2):
        while getkey(dic2, a[i + 1]) == None:
            a[i + 1] = a[i + 1] - 50
        ans += distmat[getkey(dic2, a[i + 1])][getkey(dic1, a[i])]
    return ans


def cop(a, b, le):  # 把b数组的值赋值a数组
    for i in range(le):
        a[i] = b[i]


def rand(g):  # 随机解生成函数
    vis = [0] * m
    for i in range(m // 2):
        vis[i] = 0;
    on = 0
    while on < (m // 2):
        te = on
        if (vis[te] == 0):
            vis[te] = 1
            g[on] = te
            on += 1
    for i in range(0, m - 1, 2):
        g.insert(i, random.randint(m // 2, m - 1))


def normal(g):
    j = 0
    vis = [0] * (m // 2)
    b = list(range(m // 2, m))
    random.shuffle(b)
    for i in range(m // 2):
        vis[i] = 0;
    on = 0
    while on < (m // 2):
        te = on
        if (vis[te] == 0):
            vis[te] = 1
            g[on] = te
            on += 1
    for i in range(0, m - 1, 2):
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
    t1 = [0] * (m // 2)
    t2 = [0] * (m // 2)
    rand(t1)
    rand(t2)
    u1 = 0.6  # 个体最优交换子保留概率
    u2 = 0.7  # 全局最优交换子保留概率
    for i in range(n):
        for k in range(10):  # 构造两个解t1，t2求基本交换序
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
            print(k)


gbest = 100000000000
gbestway = [0.0] * m
pbestway = [[0] * (m) for i in range(n)]
pbest = [0.0] * n
road = [[0] * (m // 2) for i in range(n)]

ss = [[0, 0]] * 600
global co
speed = [[[0, 0]] * (600) for i in range(n)]
spco = [0.0] * n
init()  # 数据初始化
for i in range(1):  # 控制迭代次数
    slove()  # 达到最优解提前退出
    print(i)

print(gbest)

