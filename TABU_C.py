from H_Hy_Men import VRPLibReader
import random


def value(a):
    s = 0
    for i in a:
        for j in range(len(i) - 1):
            s += VRPLibReader.distmat[i[j]][i[j + 1]]
    return s


def tabu_solver(path):
    iterations = 20
    capacity = VRPLibReader.capacity
    things = VRPLibReader.things
    while iterations > 0:
        count = 0
        i = random.randint(0, len(path) - 1)
        j = random.randint(0, len(path) - 1)
        while i == j:
            j = random.randint(0, len(path) - 1)
        i_w, j_w = 0, 0
        for a in path[i]:
            i_w += things[a]
        for a in path[j]:
            j_w += things[a]
        sw_from = random.randint(1, len(path[i]) - 2)
        sw_to = random.randint(1, len(path[j]) - 2)
        while i_w - things[path[i][sw_from]] + things[path[j][sw_to]] > capacity or j_w + things[path[i][sw_from]] - \
                things[path[j][sw_to]] > capacity:
            if count < 10:
                sw_from = random.randint(1, len(path[i]) - 2)
                sw_to = random.randint(1, len(path[j]) - 2)
            else:
                return path, value(path)
            count += 1
        temp = path[i][sw_from]
        path[i][sw_from] = path[j][sw_to]
        path[j][sw_to] = temp
        iterations -= 1
    return path