import numpy as np

class readmessage(object):
    def __init__(self,filename):
        self.file=open(filename, 'r')
        self.n = 0 #供应地+需求地数
        self.capacity=0
        self.site=[]
        self.things=[]
        self.distmat=[]
    def rdmessage(self):
        j = 0
        i=0
        lines = []
        line = self.file.readline().strip('\n')
        while line:
            lines.append(line)
            line = self.file.readline().strip('\n')
            if line.__contains__("DIMENSION"):
                self.n = int(line.lstrip('DIMENSION : '))
            self.site = np.zeros((self.n , 2))
            self.things=np.zeros(self.n).astype(int)
            if line.__contains__("CAPACITY"):
                self.capacity = int(line.lstrip('CAPACITY : '))
            self.site = np.zeros((self.n , 2))
            if line.__contains__("NODE_COORD_SECTION"):
                line = self.file.readline().strip('\n')
                while not line.__contains__("DEMAND_SECTION"):
                    a, self.site[j][0], self.site[j][1] = line.strip().split(" ")
                    j =int(a)
                    line = self.file.readline().strip('\n')
            if line.__contains__("DEMAND_SECTION"):
                line = self.file.readline().strip('\n')
                while not line.__contains__("DEPOT_SECTION"):
                    a, self.things[i] = line.strip().split(" ")
                    i = int(a)
                    line = self.file.readline().strip('\n')
            if line.__contains__("DEPOT_SECTION"):
                break

        num1 = self.site.shape[0]  # 矩阵的行数
        self.distmat = np.zeros((num1, num1))  # 构造全零矩阵
        for i in range(0, num1):
            for j in range(0, num1):  # 利用数组求二范式计算距离
                self.distmat[i][j]  = np.linalg.norm(self.site[i] - self.site[j])
