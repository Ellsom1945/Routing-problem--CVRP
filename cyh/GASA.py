#改进遗传:四种交叉方式—改进退火
from cyh.SA import *
import random
import numpy as np
import math
from cyh.GASA_cross import *
from cyh.value_function import *

#初始化
def GASA_init(N,n,pop):
    for i in range(N):
        pop[i]=np.random.permutation(range(1,n+1))

#计算种群适应值
def GASA_value(pop,popvalue,distmat,weight,things):
    for i in range(len(pop)):
        popvalue[i]=value_function(distmat,list(pop[i]),weight,things)

#更新种群最优解
def GASA_update_pop(pop,popvalue,bpop,bvalue):
    for i in range(len(popvalue)):
        if popvalue[i]<bvalue:
            bpop=pop[i].copy()
            bvalue=popvalue[i]
            bol=True
    return bpop,bvalue

#变异函数，随机变换一个位置
def mutate(n,path,mutate_rate):
    temp=path.copy()
    rate = random.random()
    if (rate < mutate_rate):
        x=random.randint(0,n-1)
        y=random.randint(0,n-1)
        while x==y:
            x=random.randint(0,n-1)
        temp[x],temp[y]=temp[y],temp[x]
    return temp

#退火选择
def GASA_SA_choice(fpop,s1,s2,distmat,weight,things,T):
    f1=value_function(distmat,list(fpop[0]),weight,things)
    f2=value_function(distmat,list(fpop[1]),weight,things)
    v1=value_function(distmat,list(s1),weight,things)
    v2=value_function(distmat,list(s2),weight,things)
    if v1<=f1:
        tp1=s1.copy()
    elif (random.random()<math.exp((f1 - v1)/T)):
        tp1=s1.copy()
    else:
        tp1=fpop[0].copy()
    if v2<=f2:
        tp2=s2.copy()
    elif (random.random()<math.exp((f2 - v2)/T)):
        tp2=s2.copy()
    else:
        tp2=fpop[1].copy()
    return tp1,tp2

class GASA(object):
    def __init__(self,Tmax=300,Tmin=1e-2,t=0.9,L=200,\
        maxgen=300,mutate_rate=0.1,N=50):
        self.T=Tmax
        self.T_end=Tmin
        self.t=t
        self.L=L
        self.maxgen=maxgen
        self.mutate_rate=mutate_rate
        self.N=N                                #种群中个体数

    def GASA_solver(self,distmat,things,weight,path=[]):
        gen=0
        n=distmat.shape[0]-1                #需求地数
        pop_value=np.zeros(self.N)               #种群每个个体适应值
        pop_path=np.zeros((self.N,n)).astype(int)#种群每个个体解
        if path!=[]:
            bestpath=path.copy()
            bestvalue=value_function(distmat,bestpath,weight,things)
        else:
            bestpath=np.zeros(n).astype(int)
            bestvalue=n*10000
        new_pop=np.zeros((self.N,n)).astype(int)

        GASA_init(self.N,n,pop_path)
        GASA_value(pop_path,pop_value,distmat,weight,things)
        bestpath,bestvalue=GASA_update_pop(pop_path,pop_value,bestpath,bestvalue)
        yc=0
        judge=1
        while gen<self.maxgen and judge:
            while(True):
                for i in range(0,self.N,2):
                    new1,new2,father_pop=GASA_cross(pop_value,pop_path,n,distmat,self.N)
                    s_1,s_2=GASA_SA_choice(father_pop,new1,new2,distmat,weight,things,self.T)
                    s_1=mutate(n,s_1,self.mutate_rate)
                    s_2=mutate(n,s_2,self.mutate_rate)
                    new_pop[i],new_pop[i+1]=s_1.copy(),s_2.copy()
                pop_path=new_pop.copy()
                gen+=1
                self.T*=self.t
                GASA_value(pop_path,pop_value,distmat,weight,things)
                if np.min(pop_value)>=bestvalue:
                    yc+=1
                else:
                    yc=0
                    bestvalue=np.min(pop_value)
                    bestpath=pop_path[list(pop_value).index(bestvalue)].copy()
                if yc==5 or self.T<self.T_end or gen>self.maxgen:
                    judge=0
                    break
                else:
                    continue
        sa=SA(self.T,self.T_end,self.t,self.L)
        finalpath,tbest=sa.SA_solver(distmat,things,weight,bestpath)
        return finalpath,tbest
