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


cost = 0
distances = VRPLibReader.distmat
dimension = VRPLibReader.n
capacity = VRPLibReader.capacity
customers = []
UAVs = []
for i in range(dimension):
    customers.append(Customer(i, VRPLibReader.things[i]))
for i in range(dimension):
    UAVs.append(UAV(capacity))


def unassigned_customer_exists(cus_list):
    for i in cus_list:
        if not i.is_visited:
            return True
    return False


def greedy_solver():
    uav_index = 0
    global cost
    while unassigned_customer_exists(customers):
        cus_index = 0
        candidate = None
        min_cost = float('inf')
        if len(UAVs[uav_index].routes) == 0:
            UAVs[uav_index].transport(customers[0])
            if not customers[cus_index].is_visited:
                customers[cus_index].is_visited = True
        for i in range(dimension):
            if not customers[i].is_visited:
                if UAVs[uav_index].check_if_fit(customers[i].demand):
                    candidate_cost = distances[UAVs[uav_index].current_location][i]
                    if min_cost > candidate_cost:
                        min_cost = candidate_cost
                        cus_index = i
                        candidate = customers[i]
        if candidate is None:
            if uav_index + 1 < len(UAVs):
                if UAVs[uav_index].current_location != 0:
                    final_cost = distances[UAVs[uav_index].current_location][0]
                    UAVs[uav_index].transport(customers[0])
                    cost += final_cost
                uav_index += 1
            else:
                exit("The problem cannot be resolved under these constrains")
        else:
            UAVs[uav_index].transport(candidate)
            customers[cus_index].is_visited = True
            cost += min_cost
    final_cost = distances[UAVs[uav_index].current_location][0]
    UAVs[uav_index].transport(customers[0])
    cost += final_cost


greedy_solver()
# for i in range(dimension):
#     if UAVs[i].routes:
#         print("UAV", i, ":")
#         for j in range(len(UAVs[i].routes)):
#             if j == len(UAVs[i].routes) - 1:
#                 print(UAVs[i].routes[j].num)
#             else:
#                 print(UAVs[i].routes[j].num, "->")
#         print()

print("best cost=", cost)
