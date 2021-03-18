import random
from H_Hy_Men import VRPLibReader

import matplotlib.pyplot as plt

bp = [[0, 11, 34, 2, 8, 37, 28, 40, 0], [0, 1, 7, 62, 13, 0], [0, 3, 64, 33, 15, 56, 55, 9, 54, 72, 76, 70, 0],
      [0, 10, 71, 52, 79, 18, 48, 14, 21, 0], [0, 27, 59, 75, 19, 26, 35, 65, 69, 47, 41, 25, 46, 0],
      [0, 51, 31, 20, 57, 61, 16, 43, 68, 78, 23, 0], [0, 58, 32, 4, 22, 45, 50, 73, 0],
      [0, 74, 29, 17, 60, 39, 77, 36, 0], [0, 12, 44, 5, 30, 6, 24, 63, 0], [0, 49, 38, 67, 66, 53, 42, 0]]

def value(a):
    s = 0
    for i in a:
        for j in range(len(i) - 1):
            s += VRPLibReader.distmat[i[j]][i[j + 1]]
    return s


def draw_path(path, sites):
    color = ['r', 'k', 'y', 'c', 'b', 'g', 'm', 'dodgerblue', 'gold', 'peru', 'darkolivegreen', 'indigo', 'lime',
             'deeppink']
    plt.xlim(0, 100)
    plt.ylim(0, 100)
    for i in path:
        c = random.choice(color)
        for j in range(0, len(i) - 1):
            plt.plot((sites[i[j]][0], sites[i[j + 1]][0]), (sites[i[j]][1], sites[i[j + 1]][1]), c, marker='.')
    plt.show()


draw_path(bp, VRPLibReader.site)
print(value(bp))
