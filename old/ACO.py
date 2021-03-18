#50个需求地，5个供应地，以距离供应地最近为聚类条件，形成5条路径

import numpy as np
import matplotlib.pyplot as plt
from numpy import random


#需求地坐标
coordinates = np.array([[3979, 4854], [2965, 901], [1844, 1979], [2385, 537], [2156, 2169], [2582, 4561], [2920, 4481],\
                        [2746, 1749], [1116, 364], [736, 2568], [1611, 1313], [3674, 4814], [3556, 3696], [1673, 465], \
                        [1304, 510], [365, 3962], [2485, 2505], [967, 2414], [4771, 1303], [683, 564], [3876, 2460], \
                        [3319, 4193], [3449, 2322], [457, 3422], [2702, 3892], [1778, 3699], [2251, 2849], [2384, 1894],\
                        [917, 3749], [878, 835], [1841, 1616], [2538, 1560], [2582, 3891], [817, 1786], [3040, 2736], [1498, 706],\
                        [4851, 4512], [2139, 4515], [89, 1686], [4962, 4457], [1275, 5], [1836, 665], [988, 701], [965, 547], [3143, 3909],\
                        [1081, 3319], [640, 2566], [1694, 938], [4702, 1536], [2826, 4625]])

#供应地坐标
coordinates2 = np.array([[3987, 2398], [1273, 3380],[4622, 766],[974, 207], [1377, 823]])


def getdistmat1(coordinates,coordinates2):
    num = coordinates.shape[0]  #矩阵的行数
    distmat1 = np.zeros((50,5)) #构造全零矩阵
    for i in range(50):
        for j in range(0,5):#利用数组求二范式计算距离
            distmat1[i][j]  = np.linalg.norm(coordinates[i] - coordinates2[j])
    return distmat1

distmat1=getdistmat1(coordinates,coordinates2)

gather=[]
for i in range (5):
    gather.append([])
for i in range (0,50):
    gather[np.argwhere(distmat1==min(distmat1[i]))[0][1]].append(coordinates[i])

sumpath=0
for z in range(0,len(gather)):
    l=z
    a=len(gather[l])
    gather[l].append(coordinates2[l])

    def getdistmat(coordinates):
        num = len(coordinates)  #矩阵的行数
        distmat = np.zeros((num,num)) #构造全零矩阵
        for i in range(num):
            for j in range(i,num):#利用数组求二范式计算距离
                distmat[i][j] = distmat[j][i] = \
                                np.linalg.norm(coordinates[i] - coordinates[j])
        return distmat


    distmat = np.array(getdistmat(gather[l])) #距离矩阵
    numant = 2*a #蚂蚁个数
    numplace = a+1 #需求地个数
    alpha = 1       #信息素重要程度因子
    beta = 5        #启发函数重要程度因子
    rho = 0.1       #信息素的挥发速度
    Q = 1           #完成率
    iter = 0        #迭代初始
    itermax = 100    #迭代总数

    #启发矩阵 diag将对角元素设为1e10 表示从i到j的期望值
    etatable = 1.0 / (distmat+np.diag([1e10] * numplace))
    #信息素矩阵
    pheromonetable = np.ones((numplace,numplace))#构造全一矩阵
    pathtable = np.zeros((numant,numplace)).astype(int)#路径记录表
    distmat = np.array(getdistmat(gather[l]))
    lengthaver = np.zeros(itermax)#各代路径的平均长度
    lengthbest = np.zeros(itermax)#各代及其之前的最佳路径长度
    pathbest = np.zeros((itermax, numplace))#存放最佳路径地点的坐标

    while iter < itermax:
        if numant <= numplace:
            pathtable[:,0] = np.random.permutation(range(0,numplace))[:numant]
                    #随机排列一个序列
        else:   #将蚂蚁随机放置在需求点
            pathtable[:numplace,0] = np.random.permutation(range(0,numplace))[:]
            pathtable[numplace:,0] = \
                        np.random.permutation(range(0,numplace))[:numant-numplace]

        length = np.zeros(numant)#计算各个蚂蚁的路径距离

        for i in range(numant):
            visiting = pathtable[i,0] #当前所在位置
            unvisited = set(range(numplace))#未访问的地点
            unvisited.remove(visiting) #删除已经过的地点
            for j in range(1,numplace):#轮盘法选择下一个地点
                listunvisited = list(unvisited)
                probtrans = np.zeros(len(listunvisited))
                for k in range(len(listunvisited)):
                    probtrans[k] = \
                    np.power(pheromonetable[visiting][listunvisited[k]],alpha)\
                    *np.power(etatable[visiting][listunvisited[k]],beta)
                #求出本只蚂蚁的转移到各个地点的概率数列
                cumsumprobtrans = (probtrans / sum(probtrans)).cumsum()
                cumsumprobtrans -= np.random.rand()
                k = listunvisited[list(cumsumprobtrans>0).index(True)]#下一个城市
                pathtable[i,j] = k
                unvisited.remove(k)
                #计算到K城市的距离
                length[i] += distmat[visiting][k]
                visiting = k
            #一只蚂蚁总的路径
            length[i] += distmat[visiting][pathtable[i, 0]]
        #平均路径
        lengthaver[iter] = length.mean()


    #选出最佳路径
        if iter == 0:
            lengthbest[iter] = length.min()
            pathbest[iter] = pathtable[length.argmin()].copy()
        else:
            if length.min() > lengthbest[iter - 1]:
                lengthbest[iter] = lengthbest[iter - 1]
                pathbest[iter] = pathbest[iter - 1].copy()
            else:
                lengthbest[iter] = length.min()
                pathbest[iter] = pathtable[length.argmin()].copy()


    #更新信息素
        changepheromonetable = np.zeros((numplace, numplace))
        for i in range(numant):
            for j in range(numplace-1):
                changepheromonetable[pathtable[i, j]][pathtable[i, j + 1]] += \
                                Q / distmat[pathtable[i, j]][pathtable[i, j + 1]]
            changepheromonetable[pathtable[i, j + 1]][pathtable[i, 0]] += \
                                Q / distmat[pathtable[i, j + 1]][pathtable[i, 0]]
    #信息素更新公式
        pheromonetable = (1 - rho) * pheromonetable + changepheromonetable

        iter +=1
        print("this iteration end：",iter)
        if (iter - 1)%20 == 0:
            print("schedule:",iter - 1)



    #作出找到的最优路径图
    bestpath = pathbest[-1]
    for i in range(0,a):
        plt.plot(gather[l][i][0],gather[l][i][1],'r',marker=u'$\cdot$')
    plt.xlim([-100,5000])
    plt.ylim([-100,5000])
    for i in range(numplace-1):
      m, n = int(bestpath[i]), int(bestpath[i + 1])
      print ("best-path",m,n)
      plt.plot([gather[l][m][0],gather[l][n][0]],\
               [gather[l][m][1],gather[l][n][1]],'k')

    plt.plot([gather[l][int(bestpath[numplace-1])][0],gather[l][int(bestpath[0])][0]],\
               [gather[l][int(bestpath[numplace-1])][1],gather[l][int(bestpath[0])][1]],'k')

    plt.plot(gather[l][a][0],gather[l][a][1],'ob')
    sumpath+=lengthbest[a-1]

ax=plt.gca()
ax.set_title("Best Path")
ax.set_xlabel('X axis')
ax.set_ylabel('Y_axis')
plt.savefig('Best Path.png',dpi=500,bbox_inches='tight')
plt.show()
print(sumpath)




#50个需求地，50个供应地，以距离供应地最近为聚类条件，形成路径

import numpy as np
import matplotlib.pyplot as plt
from numpy import random


#需求地坐标
coordinates = np.array([[3979, 4854], [2965, 901], [1844, 1979], [2385, 537], [2156, 2169], [2582, 4561], [2920, 4481],\
                        [2746, 1749], [1116, 364], [736, 2568], [1611, 1313], [3674, 4814], [3556, 3696], [1673, 465], \
                        [1304, 510], [365, 3962], [2485, 2505], [967, 2414], [4771, 1303], [683, 564], [3876, 2460], \
                        [3319, 4193], [3449, 2322], [457, 3422], [2702, 3892], [1778, 3699], [2251, 2849], [2384, 1894],\
                        [917, 3749], [878, 835], [1841, 1616], [2538, 1560], [2582, 3891], [817, 1786], [3040, 2736], [1498, 706],\
                        [4851, 4512], [2139, 4515], [89, 1686], [4962, 4457], [1275, 5], [1836, 665], [988, 701], [965, 547], [3143, 3909],\
                        [1081, 3319], [640, 2566], [1694, 938], [4702, 1536], [2826, 4625]])

#供应地坐标
coordinates2 = np.array([[3322, 58], [3987, 2398], [3144, 417], [1273, 3380], [2792, 526], [2759, 3258],\
                         [2390, 4410], [3368, 2957], [841, 4658], [4674, 3347], [2749, 2452], [2237, 3424], [3086, 1432], [2160, 2810],\
                         [4622, 766], [3330, 4004], [4150, 3170], [3429, 4197], [1991, 2780], [1656, 383], [974, 207], [4907, 1616],\
                         [1377, 823], [3214, 4037], [4159, 3570], [2296, 14], [3110, 1510], [2577, 2966], [4255, 2547], [2637, 1885],\
                         [1406, 4309], [2450, 3962], [4295, 1183], [4369, 2409], [939, 967], [3699, 2823], [1711, 2909], [1462, 3568],\
                         [793, 4057], [4240, 1848], [4410, 2969], [1803, 3053], [1141, 328], [225, 4181], [674, 4990], [3913, 328], [2708, 3970],\
                         [3199, 188], [3273, 526], [1531, 1774]])


def getdistmat1(coordinates,coordinates2):
    num = coordinates.shape[0]  #矩阵的行数
    distmat1 = np.zeros((50,50)) #构造全零矩阵
    for i in range(50):
        for j in range(50):#利用数组求二范式计算距离
            distmat1[i][j]  = np.linalg.norm(coordinates[i] - coordinates2[j])
    return distmat1

distmat1=getdistmat1(coordinates,coordinates2)

gather=[]
for i in range (50):
    gather.append([])
for i in range (0,50):
    gather[np.argwhere(distmat1==min(distmat1[i]))[0][1]].append(coordinates[i])

sumpath=0
for z in range(0,len(gather)):
    l=z
    a=len(gather[l])
    if a==0:
        continue
    gather[l].append(coordinates2[l])

    def getdistmat(coordinates):
        num = len(coordinates)  #矩阵的行数
        distmat = np.zeros((num,num)) #构造全零矩阵
        for i in range(num):
            for j in range(i,num):#利用数组求二范式计算距离
                distmat[i][j] = distmat[j][i] = \
                                np.linalg.norm(coordinates[i] - coordinates[j])
        return distmat


    distmat = np.array(getdistmat(gather[l])) #距离矩阵
    numant = 2*a #蚂蚁个数
    numplace = a+1 #需求地个数
    alpha = 1       #信息素重要程度因子
    beta = 5        #启发函数重要程度因子
    rho = 0.1       #信息素的挥发速度
    Q = 1           #完成率
    iter = 0        #迭代初始
    itermax = 50    #迭代总数

    #启发矩阵 diag将对角元素设为1e10 表示从i到j的期望值
    etatable = 1.0 / (distmat+np.diag([1e10] * numplace))
    #信息素矩阵
    pheromonetable = np.ones((numplace,numplace))#构造全一矩阵
    pathtable = np.zeros((numant,numplace)).astype(int)#路径记录表
    distmat = np.array(getdistmat(gather[l]))
    lengthaver = np.zeros(itermax)#各代路径的平均长度
    lengthbest = np.zeros(itermax)#各代及其之前的最佳路径长度
    pathbest = np.zeros((itermax, numplace))#存放最佳路径地点的坐标

    while iter < itermax:
        if numant <= numplace:
            pathtable[:,0] = np.random.permutation(range(0,numplace))[:numant]
                    #随机排列一个序列
        else:   #将蚂蚁随机放置在需求点
            pathtable[:numplace,0] = np.random.permutation(range(0,numplace))[:]
            pathtable[numplace:,0] = \
                        np.random.permutation(range(0,numplace))[:numant-numplace]

        length = np.zeros(numant)#计算各个蚂蚁的路径距离

        for i in range(numant):
            visiting = pathtable[i,0] #当前所在位置
            unvisited = set(range(numplace))#未访问的地点
            unvisited.remove(visiting) #删除已经过的地点
            for j in range(1,numplace):#轮盘法选择下一个地点
                listunvisited = list(unvisited)
                probtrans = np.zeros(len(listunvisited))
                for k in range(len(listunvisited)):
                    probtrans[k] = \
                    np.power(pheromonetable[visiting][listunvisited[k]],alpha)\
                    *np.power(etatable[visiting][listunvisited[k]],beta)
                #求出本只蚂蚁的转移到各个地点的概率数列
                cumsumprobtrans = (probtrans / sum(probtrans)).cumsum()
                cumsumprobtrans -= np.random.rand()
                k = listunvisited[list(cumsumprobtrans>0).index(True)]#下一个城市
                pathtable[i,j] = k
                unvisited.remove(k)
                #计算到K城市的距离
                length[i] += distmat[visiting][k]
                visiting = k
            #一只蚂蚁总的路径
            length[i] += distmat[visiting][pathtable[i, 0]]
        #平均路径
        lengthaver[iter] = length.mean()


    #选出最佳路径
        if iter == 0:
            lengthbest[iter] = length.min()
            pathbest[iter] = pathtable[length.argmin()].copy()
        else:
            if length.min() > lengthbest[iter - 1]:
                lengthbest[iter] = lengthbest[iter - 1]
                pathbest[iter] = pathbest[iter - 1].copy()
            else:
                lengthbest[iter] = length.min()
                pathbest[iter] = pathtable[length.argmin()].copy()


    #更新信息素
        changepheromonetable = np.zeros((numplace, numplace))
        for i in range(numant):
            for j in range(numplace-1):
                changepheromonetable[pathtable[i, j]][pathtable[i, j + 1]] += \
                                Q / distmat[pathtable[i, j]][pathtable[i, j + 1]]
            changepheromonetable[pathtable[i, j + 1]][pathtable[i, 0]] += \
                                Q / distmat[pathtable[i, j + 1]][pathtable[i, 0]]
    #信息素更新公式
        pheromonetable = (1 - rho) * pheromonetable + changepheromonetable

        iter +=1
        print("this iteration end：",iter)
        if (iter - 1)%20 == 0:
            print("schedule:",iter - 1)



    #作出找到的最优路径图
    bestpath = pathbest[-1]
    for i in range(0,a):
        plt.plot(gather[l][i][0],gather[l][i][1],'r',marker=u'$\cdot$')
    plt.xlim([-100,5000])
    plt.ylim([-100,5000])
    for i in range(numplace-1):
      m, n = int(bestpath[i]), int(bestpath[i + 1])
      print ("best-path",m,n)
      plt.plot([gather[l][m][0],gather[l][n][0]],\
               [gather[l][m][1],gather[l][n][1]],'k')

    plt.plot([gather[l][int(bestpath[numplace-1])][0],gather[l][int(bestpath[0])][0]],\
               [gather[l][int(bestpath[numplace-1])][1],gather[l][int(bestpath[0])][1]],'k')

    plt.plot(gather[l][a][0],gather[l][a][1],'ob')
    sumpath+=lengthbest[a-1]

ax=plt.gca()
ax.set_title("Best Path")
ax.set_xlabel('X axis')
ax.set_ylabel('Y_axis')
plt.savefig('Best Path.png',dpi=500,bbox_inches='tight')
plt.show()
plt.close()
print(sumpath)

