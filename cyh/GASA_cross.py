import random
import numpy as np
#三交叉算子
def GASA_threecross(popva,poppath,n):
    probability=((1/popva)/((1/popva).sum())).cumsum()
    father_pop=np.zeros((3,n)).astype(int)
    k=[]
    for i in range(3):
        t=probability.copy()
        t-=np.random.rand()
        j=list(t>0).index(True)
        while j in k:
            t=probability.copy()
            t-=np.random.rand()
            j=list(t>0).index(True)
        k.append(j)
        father_pop[i]=poppath[j].copy()
    return father_pop

#右轮变换    
def GASA_right_rotation(i,path,n):
    j=list(path).index(i)
    temppath=np.zeros(n).astype(int)
    temppath[:n-j]=path[j:]
    temppath[n-j:]=path[:j]
    return temppath

#左轮变换
def GASA_left_rotation(i,path,n):
    j=list(path).index(i)
    temppath=np.zeros(n).astype(int)
    temppath[:n-j-1]=path[j+1:]
    temppath[n-j-1:]=path[:j+1]
    return temppath

#产生子代1
def son1(fpop,n,distmat):
    new1=[0]*n
    q=random.randint(1,n)
    new1[0]=q
    unv=list(set(range(1,n+1)))
    unv.remove(q)
    for i in range(1,n):
        for k in range(3):
            fpop[k]=GASA_right_rotation(q,fpop[k],n)
        b=0
        for k in range(3):
            if (fpop[k][1] in unv)==False:
                continue
            if distmat[fpop[k][0]][fpop[k][1]]<distmat[fpop[b][0]][fpop[b][1]] or (fpop[b][1] in unv)==False:
                b=k
        if (fpop[b][1] in unv)==False:
            q=random.choice(unv)
        else:
            q=fpop[b][1]
        unv.remove(q)
        new1[i]=q
    return new1

#产生子代2
def son2(fpop,t,n,distmat):
    new2=[0]*n
    q=t
    new2[0]=q
    unv=list(set(range(1,n+1)))
    unv.remove(q)
    for i in range(1,n):
        for k in range(3):
            fpop[k]=GASA_left_rotation(q,fpop[k],n)
        b=0
        for k in range(3):
            if (fpop[k][-2] in unv)==False:
                continue
            if distmat[fpop[k][-1]][fpop[k][-2]]<distmat[fpop[b][-1]][fpop[b][-2]] or (fpop[b][-2] in unv)==False:
                b=k
        if (fpop[b][-2] in unv)==False:
            q=random.choice(unv)
        else:
            q=fpop[b][-2]
        unv.remove(q)
        new2[i]=q
    return new2

#交叉函数,顺序交叉
def GASA_cross1(ans1,ans2,n):
    new1=[0]*n
    new2=[0]*n
    x=random.randint(0,n-1)
    y=random.randint(0,n-1)
    if x<y:     #子代1
        new1[x:y+1]=ans1[x:y+1].copy()
    else:
        new1[y:x+1]=ans1[y:x+1].copy()
    j=0
    for i in range(n):
        if (new1[i]!=0):
            continue
        else:
            while(ans2[j] in new1):
                j+=1
            new1[i]=ans2[j]
            j+=1
    x=random.randint(0,n-1)
    y=random.randint(0,n-1)
    if x<y:     #子代2
        new2[x:y+1]=ans2[x:y+1]
    else:
        new2[y:x+1]=ans2[y:x+1]
    i=0
    j=0
    for i in range(n):
        if (new2[i]!=0):
            continue
        else:
            while(ans1[j] in new2):
                j+=1
            new2[i]=ans1[j]
            j+=1
    return np.array(new1),np.array(new2)

#部分映射交叉
def GASA_cross2(ans1,ans2,n):
    new1=[0]*n
    new2=[0]*n
    new1=list(ans1)
    new2=list(ans2)
    x=random.randint(0,n-1)
    y=random.randint(0,n-1)
    while x==y:
        x=random.randint(0,n-1)
    l1=[]
    l2=[]
    if x<y:     #子代1
        new1[x:y+1]=ans2[x:y+1]
        new2[x:y+1]=ans1[x:y+1]
        for i in range(x,y+1):
            if (ans1[i] in ans2[x:y+1]):
                continue
            l1.append(ans1[i])
        for i in range(x,y+1):
            if(ans2[i] in ans1[x:y+1]):
                 continue
            l2.append(ans2[i])
        d1=dict(zip(l1,l2))
        d2=dict(zip(l2,l1))
        for i in range(n):
            if i>=x and i<=y:
                continue
            if d2.__contains__(new1[i])==True:
                new1[i]=d2[new1[i]]
            if d1.__contains__(new2[i])==True:
                new2[i]=d1[new2[i]]
    else:
        new1[y:x+1]=ans2[y:x+1]
        new2[y:x+1]=ans1[y:x+1]
        for i in range(y,x+1):
            if (ans1[i] in ans2[y:x+1]):
                continue
            l1.append(ans1[i])
        for i in range(y,x+1):
            if (ans2[i] in ans1[y:x+1]):
                continue
            l2.append(ans2[i])
        d1=dict(zip(l1,l2))
        d2=dict(zip(l2,l1))
        for i in range(n):
            if i>=y and i<=x:
                continue
            if d2.__contains__(new1[i])==True:
                new1[i]=d2[new1[i]]
            if d1.__contains__(new2[i])==True:
                new2[i]=d1[new2[i]]
    return np.array(new1),np.array(new2)

#部分位置交叉
def GASA_cross3(ans1,ans2,n):
    new1=[0]*n
    new2=[0]*n
    l1=list(range(0,n))
    random.shuffle(l1)
    for i in range(n//2):
        new1[l1[i]]=ans1[l1[i]]
    j=0
    for i in range(n):
        if (new1[i]!=0):
            continue
        else:
            while(ans2[j] in new1):
                j+=1
            new1[i]=ans2[j]
            j+=1
    l1=list(range(0,n))#子代2
    random.shuffle(l1)
    for i in range(n//2):
        new2[l1[i]]=ans2[l1[i]]
    j=0
    for i in range(n):
        if (new2[i]!=0):
            continue
        else:
            while(ans1[j] in new2):
                j+=1
            new2[i]=ans1[j]
            j+=1
    return np.array(new1),np.array(new2)

def GASA_cross(pop_value,pop_path,n1,distmat,N):
    a=random.randint(0,N-1)
    b=random.randint(0,N-1)
    while a==b:
        a=random.randint(0,N-1)
    z=random.randint(0,3)
    if (z==0):
        ff=np.zeros((2,n1)).astype(int)
        ff[0]=pop_path[a].copy()
        ff[1]=pop_path[b].copy()
        t1,t2=GASA_cross1(pop_path[a],pop_path[b],n1)
        return t1,t2,ff
    elif (z==1):
        ff=np.zeros((2,n1)).astype(int)
        ff[0]=pop_path[a].copy()
        ff[1]=pop_path[b].copy()
        t1,t2=GASA_cross2(pop_path[a],pop_path[b],n1)
        return t1,t2,ff
    elif (z==2):
        ff=np.zeros((2,n1)).astype(int)
        ff[0]=pop_path[a].copy()
        ff[1]=pop_path[b].copy()
        t1,t2=GASA_cross3(pop_path[a],pop_path[b],n1)
        return t1,t2,ff
    else:
        ff=GASA_threecross(pop_value,pop_path,n1)
        t1=son1(ff,n1,distmat)
        t2=son2(ff,t1[0],n1,distmat)
        return t1,t2,ff