# bees.py
# A solution to the Traveling Salesman Problem
# that mimics the foraging behavior of honey bees

import copy
import csv
import math
import random
import sys
from itertools import takewhile
from scipy.spatial import distance


class Bee:
  def __init__(self, node_set, table):
    self.role = ''
    randomized_path = list(node_set) # creates an initial randomized path for each bee to explore
    random.shuffle(randomized_path)
    self.path = randomized_path
    self.distance = get_total_distance_of_path(self.path, table)
    self.cycle = 0 # number of iterations on current solution


def read_data_from_csv(file_name):
    """
    Returns data read from file
    """
    data_list = []
    with open(file_name) as f:
        reader = csv.reader(f)
        data_list = [[int(s) for s in row.split(',')] for row in f]
    return data_list


def get_distance_between_nodes(n1, n2):
    """
    Calculates the Euclidean distance between two nodes
    """
    return distance.euclidean(n1, n2)


def make_distance_table(data_list):
    """
    Creates a table that stores distance between every pair of nodes
    """
    length = len(data_list)
    table = [[get_distance_between_nodes(
        (data_list[i][1],data_list[i][2]), (data_list[j][1],data_list[j][2]))
        for i in range(0, length)] for j in range(0, length)]
    return table


def get_total_distance_of_path(path, table):
    """
    Calculates the total distance of an individual bee's path
    """
    new_path = list(path)
    new_path.insert(len(path), path[0])
    new_path = new_path[1:len(new_path)]
    coordinates = zip(path, new_path)
    distance = sum([table[i[0]][i[1]] for i in coordinates])
    return distance

def initialize_hive(population, data, table):
    """
    Initializes a hive and populates it with bees
    Bees will have a randomized path attribute
    """

    path = [x[0] for x in data]
    hive = [Bee(path, table) for i in range (0, population)]
    print(path)
    return hive


def assign_roles(hive, role_percentiles):
    """
    Assigns initial roles based on role percentiles
    to each bee in the hive
    """
    population = len(hive)
    onlooker_count = int(population * role_percentiles[0])
    forager_count = int(population * role_percentiles[1])

    for i in range(0, onlooker_count):
        hive[i].role = 'O'
    for i in range(onlooker_count, (onlooker_count + forager_count)):
        hive[i].role = 'F'
    return hive


def forage(bee, table, limit):
    """
    Worker bee behavior, iteratively refines a potential shortest path
    by examining random neighbor indices
    """
    random_idx = random.randint(0, len(bee.path) - 2) # random index 0 to next to last element
    # print("BEE PATH: {}".format(bee.path))
    new_path = list(bee.path)
    new_path[random_idx], new_path[random_idx + 1] = new_path[random_idx + 1], new_path[random_idx]
    new_distance = get_total_distance_of_path(new_path, table)
    if new_distance < bee.distance:
        bee.path = new_path
        bee.distance = new_distance
    bee.cycle += 1
    if bee.cycle >= limit:
        bee.role = 'S'
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
    bee.cycle = 0
    ## Alternatively, could select randomly from best solutions?


def manage(bee, best_distance, threshold):
    """
    Onlooker behavior, oversees perfomance of forager bees
    Assigns underperforming worker bees to scout role
    """
    if bee.role != 'O':
        if bee.distance > best_distance * threshold:
            bee.role = 'S'


def run():
    data = read_data_from_csv("data.csv")
    #data = [[0,0,0], [1,3,4], [2,-3,4], [3,-3,-4]]

    print(data)

    table = make_distance_table(data)
    population = len(data)
    onlooker_percent = 0
    forager_percent = 1
    percentiles = [onlooker_percent, forager_percent]
    threshold = 2


    hive = initialize_hive(population, data, table)
    hive = assign_roles(hive, percentiles)

    best_distance = sys.maxsize
    best_path = data
    cycle_limit = 10000
    cycle = 0

    while cycle < cycle_limit:
        for i in range(0, population):
            # if best_distance == optimal_distance:
            #     break
            # if hive[i].role == 'O':
            #     random_idx = random.randint(0, population - 1)
            #     manage(hive[random_idx], best_distance, threshold)

            if hive[i].role == 'F':
            # elif hive[i].role == 'F':
                distance = forage(hive[i], table, 100)
                if distance < best_distance:
                    best_distance = distance
                    best_path = list(hive[i].path)
                    print("CYCLE: {} BEST DIST: {}".format(cycle, best_distance))
                    print("PATH: {}".format(best_path))
                    print("BEE: {}".format(i))
            elif hive[i].role == 'S':
                scout(hive[i])

            cycle += 1

#===============#

run()
# print(get_distance_between_nodes((0,0), (3,4)))
# data = [[1,0,0], [2,3,4], [3,-3,4], [4,-3,-4]]
# table = make_distance_table(data)
# for row in table:
#     print(row)
#     # print(sum(row))
#
# # path = (0,1,2)
# #
#
# path = [3,1,2,0]
# print(get_total_distance_of_path(path, table))
#






# TODO:
# write artifical bee colony pseudo for TSP
# write artifical bee colony code
# https://medium.com/cesar-update/a-swarm-intelligence-approach-to-optimization-problems-using-the-artificial-bee-colony-abc-5d4c0302aaa4
# https://towardsdatascience.com/a-modified-artificial-bee-colony-algorithm-to-solve-clustering-problems-fc0b69bd0788
