def value_function(distmat,list1,weight,things):
    s=0
    w=weight
    tlist=list(list1).copy()
    tlist.insert(0,0)
    for i in range(0,len(tlist)-1):
        w=w-things[tlist[i+1]]
        if(w<0):  #已超过最大运输距离或货物不足，返回
            s+=distmat[tlist[i]][0]+distmat[0][tlist[i+1]]
            w=weight-things[tlist[i+1]]
        else:
        #计算到K城市的距离
            s += distmat[tlist[i]][tlist[i+1]]
    s+=distmat[tlist[-1]][0]
    return s