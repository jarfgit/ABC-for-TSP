# bees.py
# A solution to a 1-dimensional Traveling Salesman Problem
# that mimics the foraging behavior of honey bees

import copy
import csv
import math
import random
import sys
from scipy.spatial import distance

class Bee:
  def __init__(self, node_set):
    self.role = ''
    randomized_path = list(node_set) # creates an initial randomized path for each bee to explore
    random.shuffle(randomized_path)
    self.path = randomized_path
    self.distance = get_total_distance_of_path(self.path)


def generate_node_set(num_nodes):
    """
    Generates a randomized list of nodes
    """
    return random.sample(range(1, num_nodes * 100), num_nodes)


def get_total_distance_of_path(path):
    """
    Calculates the total distance of an individual bee's path
    """
    distance = sum([abs(j-i) for i, j in zip(path[1:], path[:-1])])
    return distance

def initialize_hive(population, node_set):
    """
    Initializes a hive and populates it with bees
    Bees will have a randomized path attribute
    """
    hive = [Bee(node_set) for i in range (0, population)]
    return hive


def assign_roles(hive, role_percentiles):
    """
    Assigns initial roles based on role percentiles
    to each bee in the hive
    """
    population = len(hive)
    onlooker_count = math.floor(population * role_percentiles[0])
    forager_count = math.floor(population * role_percentiles[1])

    for i in range(0, onlooker_count):
        hive[i].role = 'O'
    for i in range(onlooker_count, (onlooker_count + forager_count)):
        hive[i].role = 'F'
    return hive

def forage(bee):
    """
    Worker bee behavior, iteratively refines a potential shortest path
    by examining random neighbor indices
    """
    random_idx = random.randint(0, len(bee.path) - 2)
    # print("CURRENT PATH: {}".format(bee.path))
    # print("CURRENT PATH DISTANCE: {}".format(bee.distance))
    #
    # # This is basically bubble sort :(
    # new_path = list(bee.path)
    # new_path[random_idx], new_path[random_idx + 1] = new_path[random_idx + 1], new_path[random_idx]
    # new_path_distance = get_total_distance_of_path(new_path)
    # print("NEW PATH: {}".format(new_path))
    #
    # print("NEW PATH DISTANCE: {}".format(new_path_distance))
    # if new_path_distance < bee.distance:
    #     bee.path = new_path
    #     bee.distance = new_path_distance
    #     print("NEW PATH SWAPPED: {}".format(new_path_distance))

    if bee.path[random_idx] > bee.path[random_idx + 1]:
        new_path = list(bee.path)
        new_path[random_idx], new_path[random_idx + 1] = new_path[random_idx + 1], new_path[random_idx]
        bee.path = new_path
        bee.distance = get_total_distance_of_path(new_path)
    print("BEE PATH: {}".format(bee.distance))
    return bee.distance

def scout(bee):
    """
    Scout bee behavior, abandons unsuccessful path for new random path
    Resets role to forager
    """
    new_path = list(bee.path)
    random.shuffle(new_path)
    bee.path = new_path
    bee.role = 'F'


def manage(bee, best_distance, threshold):
    """
    Onlooker behavior, oversees perfomance of forager bees
    Assigns underperforming worker bees to scout role
    """
    if bee.role != 'O':
        if bee.distance > best_distance * threshold:
            bee.role = 'S'


def run():
    num_nodes = 20
    population = 20
    onlooker_percent = .5
    forager_percent = .5
    percentiles = [onlooker_percent, forager_percent]
    threshold = 2

    # graph_data = read_data_from_csv("data.csv")
    node_set = generate_node_set(num_nodes)
    sorted_node_set = list(node_set)
    sorted_node_set.sort()
    optimal_distance = get_total_distance_of_path(sorted_node_set)
    print("Sorted node set: {}".format(sorted_node_set))
    print("Optimal distance: {}".format(optimal_distance))

    hive = initialize_hive(population, node_set)
    hive = assign_roles(hive, percentiles)

    best_distance = sys.maxsize
    best_path = node_set
    cycle_limit = 11000
    cycle = 0

    while cycle < cycle_limit:
        for i in range(0, population):
            if best_distance == optimal_distance:
                break
            if hive[i].role == 'O':
                random_idx = random.randint(0, population - 1)
                manage(hive[random_idx], best_distance, threshold)
            elif hive[i].role == 'F':
                distance = forage(hive[i])
                if distance < best_distance:
                    best_distance = distance
                    best_path = list(hive[i].path)
                    print("CYCLE: {} BEST DIST: {}".format(cycle, best_distance))

            elif hive[i].role == 'S':
                scout(hive[i])

            if i == population - 1:
                i = 0
        cycle += 1


#=======================================================================

run()







# TODO:
# write artifical bee colony pseudo for TSP
# write artifical bee colony code
# https://medium.com/cesar-update/a-swarm-intelligence-approach-to-optimization-problems-using-the-artificial-bee-colony-abc-5d4c0302aaa4
# https://towardsdatascience.com/a-modified-artificial-bee-colony-algorithm-to-solve-clustering-problems-fc0b69bd0788
