#逆序,随机在路径中选出两个城市,将这两个城市之间的城市顺序完全倒置得出新的路径
def ch1(tpath):
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

#三变化，任选序号 u,v,w(设u ＜v ＜w ），将u和v 之间的路径插到 w 之后访问
def ch2(tpath):
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

#移位,指随机在路径中选出两个城市，把这两个城市以及它们中间的若干个城市，统一向左或者向右移动若干个位置
def ch3(tpath):
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

#交换,随机在路径中选出两个城市，把这两个城市位置交换
def ch4(tpath):
    x=random.randint(0,len(tpath)-1)
    y=random.randint(0,len(tpath)-1)
    while x==y:
        x=random.randint(0,len(tpath)-1)
    tpath[x],tpath[y]=tpath[y],tpath[x]
    return tpath
