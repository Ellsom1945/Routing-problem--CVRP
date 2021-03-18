"""Capacited Vehicles Routing Problem (CVRP) using an Ant Colony Algorithm (ACO)."""

from __future__ import print_function

import random

import numpy as np
from H_Hy_Men import VRPLibReader

Q = 1
RHO = 0.2

nk = {5: [32, 33, 34, 36, 37, 38, 39], 6: [33, 37, 39, 45], 7: [45, 46, 48, 53, 54], 9: [55, 61, 65]}


def get_problem_sol_file_pair(n, k):
    problem_fn = 'data/A/A-n' + str(n) + '-k' + str(k) + '.vrp'
    sol_fn = 'data/A/A-n' + str(n) + '-k' + str(k)+'.sol'
    write_fn = 'data/A-VRP-my-alpha/latest-A-n' + str(n) + '-k' + str(k)
    return problem_fn, sol_fn, write_fn


class Config:
    def __init__(self):
        self.iterations = 0
        self.ants = 0
        self.k = 0
        self.alpha = 2.0
        self.beta = 5.0
        self.iterations = 100
        # self._read_config_f()
        self.k = 5
        self.ants = 31
    #
    # def _read_config_f(self):
    #     with open('data/config', 'r') as f:
    #         for line in f.readlines():
    #             contents = line.split(' ')
    #             if contents[0] == 'iterations':
    #                 self.iterations = int(contents[2])
    #             if contents[0] == 'ants':
    #                 self.ants = int(contents[2])
    #             if contents[0] == 'k':
    #                 self.k = int(contents[2])

    def set_alpha(self, alpha):
        self.alpha = alpha

    def set_beta(self, beta):
        self.beta = beta


def read_solution_file(path):
    with open(path, 'r') as f:
        optimal_routes = []
        cost = 0
        for line in f.readlines():
            contents = line.split(' ')
            if 'cost' in contents[0].lower() or 'my_best' in contents[0].lower():
                cost = int(contents[1])
                break
            elif 'route' in contents[0].lower():
                route = []
                for i in range(2, len(contents)):
                    el = contents[i].strip()
                    if el == '':
                        break
                    route.append(int(el))
                optimal_routes.append(route)
    return optimal_routes, cost


class Coords:
    def __init__(self, filenames):
        problem_fn, sol_fn, self.write_fn = filenames
        self.capacities = []
        self.no_trucks = 5
        self.coords = []
        self.demands = []
        self.depot = None

        self._read_problem_f(problem_fn)

        self.distance_matrix = self._create_distance_matrix()

        self._read_sol_f(sol_fn)

    def _read_problem_f(self, problem_fn):
        reading_coords = False
        reading_demand = False
        reading_depot = False
        self.capacities= VRPLibReader.capacity
        self.coords= VRPLibReader.site
        self.demands= VRPLibReader.things


    def _read_sol_f(self, sol_fn):
        self.optimal_routes, self.cost = read_solution_file(sol_fn)

    def _create_distance_matrix(self):
        distances_m = []
        for i_coord in self.coords:
            distances = []
            for j_coord in self.coords:
                distance = int(round(np.linalg.norm(np.subtract(i_coord, j_coord))))
                distances.append(distance)
            distances_m.append(distances)
        return distances_m


class Pheromone_Trails:
    def __init__(self, no_cities):
        from random import uniform
        self.pheromones_matrix = []
        for distances in range(no_cities):
            pheromones = [uniform(0, 0.1) for _ in range(no_cities)]
            self.pheromones_matrix.append(pheromones)

    def get_pheromone_trail(self, city_i, city_j):
        return self.pheromones_matrix[city_i][city_j]

    def evaporate(self):
        self.pheromones_matrix = np.multiply(self.pheromones_matrix, (1 - RHO))

    def update(self, city_i, city_j, overall_trip_distance):
        delta_tau = Q / overall_trip_distance
        self.pheromones_matrix[city_i][city_j] += delta_tau
        self.pheromones_matrix[city_j][city_i] += delta_tau


class Ant:
    def __init__(self, capacity, depot, demands, distance_m, pheromone_trails, config):
        self.current_city = depot
        self.depot = depot
        self.distance_m = distance_m
        self.not_visited = self.create_not_visited(distance_m)
        self.capacity = capacity
        self.load = capacity
        self.demands = demands
        self.trips = []
        self.current_trip = []
        self.pheromone_trails = pheromone_trails
        self.trips_distance = None
        self.config = config

        self.start()

    def create_not_visited(self, distance_m):
        nv = set()
        for i, _ in enumerate(distance_m):
            if i != self.depot:
                nv.add(i)
        return nv

    def start(self):
        from random import randint
        start_city = randint(1, len(self.distance_m) - 1)
        self.visit_city(start_city)

    def visit_city(self, index):
        self.not_visited.remove(index)
        self.load -= self.demands[index]
        distance = self.distance_m[self.current_city][index]
        self.current_city = index
        self.current_trip.append((index, distance))

    def visit_depot(self):
        self.load = self.capacity
        distance = self.distance_m[self.current_city][self.depot]
        self.current_city = self.depot
        self.current_trip.append((self.depot, distance))
        self.trips.append(self.current_trip)
        self.current_trip = []

    def get_intensity(self, city):
        return self.pheromone_trails.get_pheromone_trail(self.current_city, city)

    def get_visibility(self, city):
        distance = self.distance_m[self.current_city][city]
        if distance == 0:
            return 1
        return 1 / distance

    def calc_val(self, city):
        intensity = self.get_intensity(city)
        visibility = self.get_visibility(city)
        return pow(intensity, self.config.alpha) * pow(visibility, self.config.beta)

    def get_neighbours_with_probab(self):
        not_visited = list(self.not_visited)

        l = [self.calc_val(city) for city in not_visited]
        m = np.divide(l, sum(l))

        for i in range(1, len(m)):
            m[i] += m[i - 1]
        return not_visited, m

    def create_path(self):
        while len(self.not_visited) > 0:
            neighbours, probabilities = self.get_neighbours_with_probab()
            r = random.random()
            next_to_visit = neighbours[-1]
            for i in range(len(probabilities)):
                if r < probabilities[i]:
                    next_to_visit = neighbours[i]
                    break

            if self.demands[next_to_visit] > self.load:
                # Come back to the depot to reload
                self.visit_depot()
            else:
                self.visit_city(next_to_visit)

        self.visit_depot()

    def calculate_paths_quality(self):
        overall_distance = 0
        for trip in self.trips:
            for _, dist in trip:
                overall_distance += dist
        self.trips_distance = overall_distance

    def leave_pheromone(self):
        for trip in self.trips:
            prev_city = self.depot
            for i, (city, _) in enumerate(trip):
                self.pheromone_trails.update(prev_city, city, self.trips_distance)
                prev_city = city
            self.pheromone_trails.update(prev_city, self.depot, self.trips_distance)

    def reset(self):
        self.current_city = 0
        self.not_visited = self.create_not_visited(self.distance_m)
        self.current_trip = []
        self.trips = []
        self.load = self.capacity
        self.start()


def trips_to_str(trips):
    s = ''
    for index, trip in enumerate(trips):
        line = 'Route #' + str(index + 1) + ": "
        for city, _ in trip:
            if city == 0:
                break
            line += str(city) + " "

        s += line + '\n'
    return s


def save(filename, optimal, my_best, routes):
    with open(filename, 'w')as f:
        f.write(routes)
        f.write("my_best: " + str(my_best) + '\n')
        f.write("optimal: " + str(optimal))


def plot_data(xs, ys):
    import matplotlib.pyplot as plt
    plt.plot(xs, ys, c='red')
    plt.xlabel('beta')
    plt.ylabel('error')
    plt.savefig('beta1.svg')


def solve_using_ants():
    config = Config()
    no_ants = config.ants
    iterations = config.iterations

    overall_score = 0

    for k, ns in nk.items():
        k_score = 0
        for n in ns:

            data = Coords(get_problem_sol_file_pair(n, k))
            no_cities = len(data.distance_matrix)
            pheromone_trails = Pheromone_Trails(no_cities)
            ants = [Ant(capacity=data.capacities[0], depot=data.depot, demands=data.demands,distance_m=data.distance_matrix, pheromone_trails=pheromone_trails, config=config) for _ in range(no_ants)]
            import sys
            best_trip = sys.maxsize
            routes = ''
            last_record = 100000000
            for iteration in range(iterations):
                for ant in ants:
                    ant.create_path()
                    ant.calculate_paths_quality()
                    if ant.trips_distance < best_trip:
                        best_trip = ant.trips_distance
                        routes = trips_to_str(ant.trips)

                for ant in ants:
                    pheromone_trails.evaporate()
                    ant.leave_pheromone()
                    ant.reset()
                metric = (best_trip - data.cost) / data.cost
                if iteration % 100 == 0:
                    if abs(last_record - metric) < 0.001:
                        break

                    last_record = metric
            print("n", n, "k", k, "optimal", data.cost, "my_best", best_trip,
                  'metric', metric)
            save(data.write_fn, data.cost, best_trip, routes)
            k_score += metric
        k_score /= len(ns)
        print('k', k, 'mean k_score', k_score)
        overall_score += k_score
    overall_score /= len(nk)
    print('mean overall_score', overall_score)


def visualize_graph(coords, routes, title):
    import networkx as nx
    import matplotlib.pyplot as plt

    G = nx.Graph()

    for route in routes:
        last_city = 0
        for city in route:
            G.add_edge(last_city, city)
            last_city = city

        G.add_edge(last_city, 0)

    edgelist = [(u, v) for (u, v, d) in G.edges(data=True)]

    for i, pos in enumerate(coords):
        G.add_node(i, pos=pos)

    pos = nx.get_node_attributes(G, 'pos')

    # nodes
    nx.draw_networkx_nodes(G, pos)

    # edges
    nx.draw_networkx_edges(G, pos, edgelist=edgelist)

    # labels
    nx.draw_networkx_labels(G, pos, font_size=20, font_family='sans-serif')

    plt.axis('off')
    plt.title(title)
    plt.show()


def main():
    random.seed(1)

    solve_using_ants()

    # Visualize one use case from the dataset
    n = 32
    k = 5
    problem_fn, sol_fn, write_fn = get_problem_sol_file_pair(n, k)
    data = Coords((problem_fn, sol_fn, write_fn))
    coords = data.coords
    optimal_routes = data.optimal_routes
    my_routes, my_cost = read_solution_file(write_fn)
    visualize_graph(coords, optimal_routes, 'optimal routes. cost: ' + str(data.cost))
    visualize_graph(coords, my_routes, 'my routes. cost: ' + str(my_cost))


if __name__ == '__main__':
    main()