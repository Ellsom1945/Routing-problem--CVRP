# 加入OR-OPT算法
import random
import VRPLibReader
from oropt import *
import datetime


class Customer:

    def __init__(self, num, demand):
        self.num = num
        self.demand = demand
        self.is_visited = False


class UAV:

    def __init__(self, cap):
        self.cap = cap
        self.load = 0
        self.routes = []
        self.current_location = 0

    def check_if_fit(self, demand):
        return self.load + demand <= self.cap

    def transport(self, cus):
        self.routes.append(cus.num)
        self.load += cus.demand
        self.current_location = cus.num


def value(a):
    s = 0
    for i in range(len(a) - 1):
        s += VRPLibReader.distmat[a[i]][a[i + 1]]
    return s


# 邻近算法求初始解
def sa_init(distmat, n, weight, things):
    w = weight
    uvisited = list(range(1, n + 1))
    visit = []
    k = 0
    while len(visit) != n:
        j = 0
        r = np.argsort(distmat[k])
        while r[j] == 0 or r[j] in visit:
            j += 1
        w -= things[r[j]]
        if w < 0:
            k = 0
            w = weight
        else:
            k = r[j]
            visit.append(r[j])
            uvisited.remove(r[j])
    return np.array(visit)


# 随机解生成函数
def rand(array_1, num_place):
    array_1 = np.random.permutation(range(1, num_place + 1))
    return array_1


# 初始化函数
def init(tabu, f, distmat, weight, things, n, num_place, position, pbestpath, pbest):
    position[0] = sa_init(distmat, num_place, weight, things)
    tabu.append(list(position[0]))
    pbestpath[0] = position[0].copy()  # 将局部最优设为初始化的随机解
    pbest[0] = get_value(distmat, position[0], weight, things)
    f[0] = pbest[0]
    for i in range(1, n):
        position[i] = rand(position[i], num_place)
        vi = get_value(distmat, position[i], weight, things)
        position[i] = oropt(list(position[i]), num_place, distmat, weight, things, vi)
        tabu.append(list(position[i]))
        pbestpath[i] = position[i].copy()  # 将局部最优设为初始化的随机解
        pbest[i] = get_value(distmat, position[i], weight, things)
        f[i] = pbest[i]


def minus(ans_1, ans_2, p, C, sub):  # 求解1减去解2的交换序结果,将其保存在sub列表中,p为交换概率
    h = 0
    b = ans_2.copy()
    for i in range(len(ans_1)):
        if ans_1[i] == b[i]:
            continue
        h = b.index(ans_1[i])
        if random.random() < ((p + C[b[i - 1]][b[h]]) / 2):
            sub.append([i, h])
        b[i], b[h] = b[h], b[i]


def add(ans, change):  # 解加上长度为length的交换序change
    x = 0
    y = 0
    length = len(change)
    for i in range(length):
        x = change[i][0]
        y = change[i][1]
        ans[x], ans[y] = ans[y], ans[x]
    change = []
    return change


# 更新个体最优
def update_pbest(i, ans, distmat, weight, things, pbestpath, pbest):
    va = get_value(distmat, ans, weight, things)  # 计算适应值
    if (va < pbest[i]):
        pbest[i] = va
        pbestpath[i] = ans.copy()


# 更新群体最优
def update_gbest(array2, gbest, gbestpath, pbestpath, pbest):
    for j in range(array2.shape[0]):
        if (pbest[j] < gbest):
            gbest = pbest[j]
            gbestpath = pbestpath[j].copy()
    return gbest, gbestpath


# 轮盘赌策略选择群体最优
def gambling_selection(array3, gbest):
    probability = ((1 / array3) / ((1 / array3).sum())).cumsum()
    probability -= np.random.rand()
    k = array3[list(probability >= 0).index(True)]
    gbest = k
    return gbest


# 产生新解——逆序
def ch1(tpath):
    x = random.randint(0, len(tpath) - 1)
    y = random.randint(0, len(tpath) - 1)
    while x == y:
        x = random.randint(0, len(tpath) - 1)
    if x < y:
        while x != y and x < y:
            tpath[x], tpath[y] = tpath[y], tpath[x]
            x += 1
            y -= 1
    else:
        while x != y and y < x:
            tpath[x], tpath[y] = tpath[y], tpath[x]
            y += 1
            x -= 1
    return tpath


# 产生新解——三变化
def ch2(tpath):
    path = []
    x = random.randint(0, len(tpath) - 2)
    y = random.randint(0, len(tpath) - 2)
    while x == y:
        x = random.randint(0, len(tpath) - 2)
    if x < y:
        z = random.randint(y + 1, len(tpath) - 1)
        path[0:x] = tpath[0:x]
        path.append(tpath[z])
        path[x + 1:y + 2] = tpath[x:y + 1]
        path[y + 2:z + 1] = tpath[y + 1:z]
        if z + 1 <= len(tpath) - 1:
            path[z + 1:] = tpath[z + 1:]
    else:
        z = random.randint(y + 1, len(tpath) - 1)
        path[0:y] = tpath[0:y]
        path.append(tpath[z])
        path[y + 1:x + 2] = tpath[y:x + 1]
        path[x + 2:z + 1] = tpath[x + 1:z]
        if z + 1 <= len(tpath) - 1:
            path[z + 1:] = tpath[z + 1:]
    return path


# 产生新解——移位
def ch3(tpath):
    path = []
    x = random.randint(0, len(tpath) - 2)
    y = random.randint(0, len(tpath) - 2)
    while x == y:
        x = random.randint(0, len(tpath) - 2)
    if x < y:
        z = random.randint(1, len(tpath) - 1 - y)
        j = len(tpath) - 1
        for i in range(z):
            path.append(tpath[j])
            j -= 1
        path[z:] = tpath[:len(tpath) - z]
    else:
        z = random.randint(1, len(tpath) - 1 - x)
        j = len(tpath) - 1
        for i in range(z):
            path.append(tpath[j])
            j -= 1
        path[z:] = tpath[:len(tpath) - z]
    return path


# 产生新解——交换
def ch4(tpath):
    x = random.randint(0, len(tpath) - 1)
    y = random.randint(0, len(tpath) - 1)
    while x == y:
        x = random.randint(0, len(tpath) - 1)
    tpath[x], tpath[y] = tpath[y], tpath[x]
    return tpath


# 产生新解
def change(tpath):
    i = random.randint(1, 5)
    if i == 1:
        return ch1(tpath)
    elif i == 2:
        return ch2(tpath)
    elif i == 3:
        return ch3(tpath)
    elif i == 4:
        return ch4(tpath)
    else:
        return rand(tpath, len(list(tpath)))


# 计算优秀系数
def calculate_C(C, distmat):
    l = distmat.shape[0]
    C1 = np.zeros((l, l))
    for i in range(l):
        for j in range(l):
            C1[i][j] = (distmat.max() - distmat[i][j]) / distmat.sum()
    for i in range(l):
        for j in range(l):
            C[i][j] = C1[i][j] / C1.max()


# 禁忌表
def search_tabu(tabu, array5):
    if (list(array5) in tabu):
        return True
    else:
        return False


# 执行函数
def pso_4(distmat, things, weight, a):
    iter = 0  # 迭代初始
    itermax = 500  # 迭代总数
    n = 30  # 粒子数
    r1 = 0.6
    r2 = 0.7
    w = 0.9  # 惯性权重
    pr = 0.5
    num_place = a

    tabu = []  # 禁忌表
    C = np.zeros((a + 1, a + 1))  # 记录优秀系数
    calculate_C(C, distmat)
    f = np.zeros(n).astype(float)  # 记录粒子的适应度
    pbestpath = np.zeros((n, num_place)).astype(int)  # gbestpath记录个体最优解
    pbest = [0] * n  # pbest记录个体最优适应值
    position = np.zeros((n, num_place)).astype(int)  # 记录每个粒子当前位置
    speed = [0] * n  # 每个粒子的速度，即交换
    # 数据初始化
    init(tabu, f, distmat, weight, things, n, num_place, position, pbestpath, pbest)
    gbest = pbest[0]  # gbest记录全局最优适应值
    gbestpath = position[0].copy()  # gbestpayh记录全局最优解
    while iter < itermax:
        iter += 1
        sub = []  # 暂存减法结果
        pr = pr * (1 - iter / itermax / (itermax / 10))
        w = 0.4 * (0.9 / 0.4) ** (1 / (1 + 10 * iter / itermax))
        r1 = 4 * r1 * (1 - r1)
        r2 = 1 - r1
        for i in range(n):
            if random.random() > pr:
                gbest, gbestpath = update_gbest(position, gbest, gbestpath, pbestpath, pbest)
            else:
                # 轮盘赌选择全局最优解，优于平均代价值作为候选解
                taver = f.copy()
                taver[taver > (taver.sum() / n)] = -1
                o = list(taver)
                while -1 in o:
                    o.remove(-1)
                gbest = gambling_selection(np.array(o), gbest)
                gbestpath = position[np.where(f == gbest)[0][0]]
            gbest, gbestpath = update_gbest(position, gbest, gbestpath, pbestpath, pbest)
            temp1 = position[i].copy()
            temp2 = position[i].copy()
            minus(list(pbestpath[i]), list(temp1), r1, C, sub)  # 与个体最优解相减
            minus(gbestpath, list(temp1), r2, C, sub)  # 与全局最优解相减
            sub = add(temp1, sub)  # 惯性权重保留
            minus(list(temp1), list(temp2), w, C, sub)  # 求出交换序
            speed[i] = sub.copy()  # 更新个体速度
            sub = add(position[i], list(speed[i]))
            # position[i]=part(distmat,things,weight,position[i])
            while search_tabu(tabu, position[i]):
                position[i] = change(position[i])
            tabu.append(list(position[i]))
            update_pbest(i, list(position[i]), distmat, weight, things, pbestpath, pbest)
            f[i] = get_value(distmat, list(position[i]), weight, things)
        if (gbest < 785):
            print(iter)
            break
    tpath = list(gbestpath)
    tpath.insert(0, 0)
    newpath = [0]
    w = 0  # 计算载货量
    i = 1
    j = len(tpath)
    while (i < j):
        if (w + things[tpath[i]] > weight):
            newpath.append(0)
            w = things[tpath[i]]
        else:
            w = w + things[tpath[i]]
        newpath.append(tpath[i])
        i += 1
    return newpath, gbest

#
# start_time = datetime.datetime.now()
# ans = pso_4(VRPLibReader.distmat, VRPLibReader.things, VRPLibReader.capacity, VRPLibReader.n - 1)
# end_time = datetime.datetime.now()
# print("pso_time", end_time - start_time)
# num = ans[0]
# total_cost = ans[1]
# while num[0] == 0:
#     del num[0]
# while num[len(num) - 1] == 0:
#     del num[len(num) - 1]
# t1 = []
# temp_arr = []
# for i in num:
#     if i != 0:
#         t1.append(i)
#     else:
#         a = []
#         for j in t1:
#             a.append(j)
#         temp_arr.append(a)
#         t1.clear()
# temp_arr.append(t1)
# for i in temp_arr:
#     i.append(0)
#     i.insert(0, 0)
# uavs = []
# for i in range(len(temp_arr)):
#     uavs.append(UAV(VRPLibReader.capacity))
# for i in range(len(temp_arr)):
#     for j in temp_arr[i]:
#         aaa = Customer(j, VRPLibReader.things[j])
#         uavs[i].transport(aaa)
# tabu_solver(uavs,total_cost)