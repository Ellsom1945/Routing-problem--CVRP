import random
import numpy as np
from numpy import random

# 随机解生成函数
def rand(array_1,num_place):
    array_1=np.random.permutation(range(1,num_place+1))
    return array_1
    
#产生新解——逆序
def chpa1(tpath):
    x=random.randint(0,len(tpath)-1)
    y=random.randint(0,len(tpath)-1)
    while x==y:
        x=random.randint(0,len(tpath)-1)
    if x<y:
        while x!=y and x<y:
            tpath[x],tpath[y]=tpath[y],tpath[x]
            x+=1
            y-=1
    else:
        while x!=y and y<x:
            tpath[x],tpath[y]=tpath[y],tpath[x]
            y+=1
            x-=1
    return tpath

#产生新解——三变化
def chpa2(tpath):
    path=[]
    x=random.randint(0,len(tpath)-2)
    y=random.randint(0,len(tpath)-2)
    while x==y:
        x=random.randint(0,len(tpath)-2)
    if x<y:
        z=random.randint(y+1,len(tpath)-1)
        path[0:x]=tpath[0:x]
        path.append(tpath[z])
        path[x+1:y+2]=tpath[x:y+1]
        path[y+2:z+1]=tpath[y+1:z]
        if z+1<=len(tpath)-1:
            path[z+1:]=tpath[z+1:]
    else:
        z=random.randint(y+1,len(tpath)-1)
        path[0:y]=tpath[0:y]
        path.append(tpath[z])
        path[y+1:x+2]=tpath[y:x+1]
        path[x+2:z+1]=tpath[x+1:z]
        if z+1<=len(tpath)-1:
            path[z+1:]=tpath[z+1:]
    return path

#产生新解——移位
def chpa3(tpath):
    path=[]
    x=random.randint(0,len(tpath)-2)
    y=random.randint(0,len(tpath)-2)
    while x==y:
        x=random.randint(0,len(tpath)-2)
    if x<y:
        z=random.randint(1,len(tpath)-1-y)
        j=len(tpath)-1
        for i in range(z):
            path.append(tpath[j])
            j-=1
        path[z:]=tpath[:len(tpath)-z]
    else:
        z=random.randint(1,len(tpath)-1-x)
        j=len(tpath)-1
        for i in range(z):
            path.append(tpath[j])
            j-=1
        path[z:]=tpath[:len(tpath)-z]
    return path

#产生新解——交换
def chpa4(tpath):
    x=random.randint(0,len(tpath)-1)
    y=random.randint(0,len(tpath)-1)
    while x==y:
        x=random.randint(0,len(tpath)-1)
    tpath[x],tpath[y]=tpath[y],tpath[x]
    return tpath

#产生新解
def changepath(tpath):
    i=random.randint(1,5)
    if i==1:
        return chpa1(tpath)
    elif i==2:
        return chpa2(tpath)
    elif i==3:
        return chpa3(tpath)
    elif i==4:
        return chpa4(tpath)
    else:
        return rand(tpath,len(list(tpath)))