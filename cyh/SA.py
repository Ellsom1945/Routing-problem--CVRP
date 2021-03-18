import math
import random
import numpy as np
from numpy import random
from cyh.change_path import *
from cyh.value_function import *

class SA(object):
    def __init__(self,Tmax=300,Tmin=1e-2,t=0.9,L=200):
        self.T=Tmax
        self.T_end=Tmin
        self.t=t
        self.L=L
        
    def SA_solver(self,distmat,things,weight,path=[]):
        n=distmat.shape[0]-1
        if path==[]:
            path=sa_nearest_path(distmat,n)
        temp1=list(path).copy()
        temp3=temp1.copy()
        tpath=temp1.copy()#最佳路径
        tbest=value_function(distmat,tpath,weight,things)#最佳总长度
        th=0
        while self.T>self.T_end:
            self.T *= self.t
            z=self.L
            while z>0:
                z-=1
                temp2=list(temp1)
                temp2=changepath(temp2)#扰动解
                t1=value_function(distmat,temp1,weight,things)    
                t2=value_function(distmat,temp2,weight,things)    
                if(t1>t2):
                    temp1=list(temp2)
                    if(t2<tbest):
                        tpath=temp2.copy()
                        tbest=t2
                    continue
                p=math.exp((t1 - t2)/self.T)
                if (random.random()< p):
                    temp1 = list(temp2)
            if (temp3==temp1):
                th+=1
            else:
                th=0
                temp3=temp1.copy()
            if th==5:
                break
        return tpath,tbest

#邻近算法求初始解
def sa_nearest_path(distmat,n):
    uvisited=list(range(1,n+1))
    visit=[]
    k=0
    for i in range(n):
        j=0
        r=np.argsort(distmat[k])
        while r[j]==0 or r[j] in visit :
            j+=1
        visit.append(r[j])
        k=r[j]
        uvisited.remove(r[j])
    return visit

