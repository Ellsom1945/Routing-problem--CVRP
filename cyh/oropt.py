import numpy as np
from cyh.value_function import *

def oropt(list5,numplace,distmat,weight,things):
    v=value_function(distmat,list5,weight,things)
    i=0
    tl=list(list5).copy()
    #三个点的插入
    while (i+3<=numplace):
        if i>0:
            if i-1>=1:
                del tl[i:i+3]
                for k in range(1,i):
                    tl.insert(k,list5[i])
                    tl.insert(k+1,list5[i+1])
                    tl.insert(k+2,list5[i+2])
                    if (value_function(distmat,tl,weight,things)<v):
                        return np.array(tl)
                    tl=list(list5).copy()
                    del tl[i:i+3]
                tl=list(list5).copy()
                for k in range(i+4,numplace):
                    tl.insert(k,list5[i])
                    tl.insert(k+1,list5[i+1])
                    tl.insert(k+2,list5[i+2])
                    del tl[i:i+3]
                    if (value_function(distmat,tl,weight,things)<v):
                        return np.array(tl)
                    tl=list(list5).copy()
            else:
                tl=list(list5).copy()
                for k in range(i+4,numplace):
                    tl.insert(k,list5[i])
                    tl.insert(k+1,list5[i+1])
                    tl.insert(k+2,list5[i+2])
                    del tl[i:i+3]
                    if (value_function(distmat,tl,weight,things)<v):
                        return np.array(tl)
                    tl=list(list5).copy()
        else:
            tl=list(list5).copy()
            for k in range(i+4,numplace):
                tl.insert(k,list5[i])
                tl.insert(k+1,list5[i+1])
                tl.insert(k+2,list5[i+2])
                del tl[i:i+3]
                if (value_function(distmat,tl,weight,things)<v):
                    return np.array(tl)
                tl=list(list5).copy()
        i+=1
    #两个点的插入
    i=0
    tl=list(list5).copy()
    while (i+2<=numplace):
        if i>0:
            if i-1>=1:
                del tl[i:i+2]
                for k in range(1,i):
                    tl.insert(k,list5[i])
                    tl.insert(k+1,list5[i+1])
                    if (value_function(distmat,tl,weight,things)<v):
                        return np.array(tl)
                    tl=list(list5).copy()
                    del tl[i:i+2]
                tl=list(list5).copy()
                for k in range(i+3,numplace):
                    tl.insert(k,list5[i])
                    tl.insert(k+1,list5[i+1])
                    del tl[i:i+2]
                    if (value_function(distmat,tl,weight,things)<v):
                        return np.array(tl)
                    tl=list(list5).copy()
            else:
                tl=list(list5).copy()
                for k in range(i+3,numplace):
                    tl.insert(k,list5[i])
                    tl.insert(k+1,list5[i+1])
                    del tl[i:i+2]
                    if (value_function(distmat,tl,weight,things)<v):
                        return np.array(tl)
                    tl=list(list5).copy()
        else:
            tl=list(list5).copy()
            for k in range(i+3,numplace):
                tl.insert(k,list5[i])
                tl.insert(k+1,list5[i+1])
                del tl[i:i+2]
                if (value_function(distmat,tl,weight,things)<v):
                        return np.array(tl)
                tl=list(list5).copy()
        i+=1
    #一个点的插入
    i=0
    tl=list(list5).copy()
    while (i+1<=numplace):
        if i>0:
            if i-1>=1:
                del tl[i]
                for k in range(1,i):
                    tl.insert(k,list5[i])
                    if (value_function(distmat,tl,weight,things)<v):
                        return np.array(tl)
                    tl=list(list5).copy()
                    del tl[i]
                tl=list(list5).copy()
                for k in range(i+2,numplace):
                    tl.insert(k,list5[i])
                    del tl[i]
                    if (value_function(distmat,tl,weight,things)<v):
                        return np.array(tl)
                    tl=list(list5).copy()
            else:
                tl=list(list5).copy()
                for k in range(i+2,numplace):
                    tl.insert(k,list5[i])
                    del tl[i]
                    if (value_function(distmat,tl,weight,things)<v):
                        return np.array(tl)
                    tl=list(list5).copy()
        else:
            tl=list(list5).copy()
            for k in range(i+2,numplace):
                tl.insert(k,list5[i])
                del tl[i]
                if (value_function(distmat,tl,weight,things)<v):
                    return np.array(tl)
                tl=list(list5).copy()
        i+=1
    return list5
