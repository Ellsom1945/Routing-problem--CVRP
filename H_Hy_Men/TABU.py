import datetime
import random
import matplotlib.pyplot as plt

import numpy as np

from H_Hy_Men import VRPLibReader


class Customer:

    def __init__(self, num, demand):
        self.num = num
        self.demand = demand
        self.is_visited = False


class UAV:

    def __init__(self, cap):
        self.cap = cap
        self.load = 0
        self.routes = []
        self.current_location = 0

    def check_if_fit(self, demand):
        return self.load + demand <= self.cap

    def transport(self, cus):
        self.routes.append(cus)
        self.load += cus.demand
        self.current_location = cus.num


def value(a):
    s = 0
    for i in a:
        for j in range(len(i) - 1):
            s += VRPLibReader.distmat[i[j]][i[j + 1]]
    return s


def tabu_solver(path):
    TABU_horizon = 5
    iterations = 20
    distances = VRPLibReader.distmat
    dimension = VRPLibReader.n
    capacity = VRPLibReader.capacity
    cost = value(path)
    mark = False
    UAVs = []
    for i in range(VRPLibReader.n):
        UAVs.append(UAV(VRPLibReader.capacity))
    for i in range(len(path)):
        for j in path[i]:
            aaa = Customer(j, VRPLibReader.things[j])
            UAVs[i].transport(aaa)
    start_time = datetime.datetime.now()
    best_solution_uavs = []
    for i in range(dimension):
        best_solution_uavs.append(UAV(capacity))
    swap_index_a = -1
    swap_index_b = -1
    swap_route_from = -1
    swap_route_to = -1
    iteration_num = 0
    tabu_matrix = np.zeros((dimension, dimension))
    best_solve_cost = cost

    while True:
        best_neb_cost = float('inf')
        for uav_index_from in range(len(UAVs)):
            routes_from = UAVs[uav_index_from].routes
            routes_from_length = len(routes_from)
            for i in range(1, routes_from_length - 1):
                for uav_index_to in range(len(UAVs)):
                    routes_to = UAVs[uav_index_to].routes
                    routes_to_length = len(routes_to)
                    for j in range(0, routes_to_length - 1):
                        moving_cus_demand = routes_from[i].demand
                        if uav_index_to == uav_index_from or UAVs[uav_index_to].check_if_fit(moving_cus_demand):
                            if not (uav_index_from == uav_index_to and (j == i or j == i - 1)):
                                minus_cost1 = distances[routes_from[i - 1].num][routes_from[i].num]
                                minus_cost2 = distances[routes_from[i].num][routes_from[i + 1].num]
                                minus_cost3 = distances[routes_to[j].num][routes_to[j + 1].num]

                                added_cost1 = distances[routes_from[i - 1].num][routes_from[i + 1].num]
                                added_cost2 = distances[routes_to[j].num][routes_from[i].num]
                                added_cost3 = distances[routes_from[i].num][routes_to[j + 1].num]

                                if (tabu_matrix[routes_from[i - 1].num][routes_from[i + 1].num] != 0 or
                                        tabu_matrix[routes_to[j].num][routes_from[i].num] != 0 or
                                        tabu_matrix[routes_from[i].num][routes_to[j + 1].num] != 0):
                                    break
                                neighbor_cost = added_cost1 + added_cost2 + added_cost3 - minus_cost1 - minus_cost2 - minus_cost3
                                if neighbor_cost < best_neb_cost:
                                    best_neb_cost = neighbor_cost
                                    swap_index_a = i
                                    swap_index_b = j
                                    swap_route_from = uav_index_from
                                    swap_route_to = uav_index_to
        for o in range(len(tabu_matrix[0])):
            for p in range(len(tabu_matrix[0])):
                if tabu_matrix[o][p] > 0:
                    tabu_matrix[o][p] -= 1
        routes_from = UAVs[swap_route_from].routes
        routes_to = UAVs[swap_route_to].routes
        UAVs[swap_route_from].routes = []
        UAVs[swap_route_to].routes = []

        swap_cus = routes_from[swap_index_a]

        cus_id_before = routes_from[swap_index_a - 1].num
        cus_id_after = routes_from[swap_index_a + 1].num
        cus_id_F = routes_to[swap_index_b].num
        cus_id_G = routes_to[swap_index_b + 1].num

        random_delay1 = random.randint(0, 5)
        random_delay2 = random.randint(0, 5)
        random_delay3 = random.randint(0, 5)

        tabu_matrix[cus_id_before][swap_cus.num] = TABU_horizon + random_delay1
        tabu_matrix[swap_cus.num][cus_id_after] = TABU_horizon + random_delay2
        tabu_matrix[cus_id_F][cus_id_G] = TABU_horizon + random_delay3

        del routes_from[swap_index_a]

        if swap_route_from == swap_route_to:
            if swap_index_a < swap_index_b:
                routes_to.insert(swap_index_b, swap_cus)
            else:
                routes_to.insert(swap_index_b + 1, swap_cus)
        else:
            routes_to.insert(swap_index_b + 1, swap_cus)

        UAVs[swap_route_from].routes = routes_from
        UAVs[swap_route_from].load -= swap_cus.demand
        UAVs[swap_route_to].routes = routes_to
        UAVs[swap_route_to].load += swap_cus.demand
        cost += best_neb_cost

        if cost < best_solve_cost:
            mark = True
            iteration_num = 0
            best_solve_cost = cost
            for i in range(dimension):
                best_solution_uavs[i].routes.clear()
                if len(UAVs[i].routes) != 0:
                    routes_size = len(UAVs[i].routes)
                    for j in range(routes_size):
                        n = UAVs[i].routes[j]
                        best_solution_uavs[i].routes.append(n)
        else:
            iteration_num += 1
        if iteration_num == iterations:
            break
    if mark:
        UAVs = best_solution_uavs
        cost = best_solve_cost
    path = []
    for i in UAVs:
        way = []
        if i.routes.__len__() > 2:
            for j in i.routes:
                way.append(j.num)
        if len(way) > 0:
            path.append(way)
    # if len(path) < 1:
    #     print(path, pathcopy)
    # end_time = datetime.datetime.now()
    # print("best cost=", cost)
    # print('算法时间:', end_time - start_time)
    npa = [col for col in path if col]
    return npa


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



