# bees.py
# A solution to the Traveling Salesman Problem
# that mimics the foraging behavior of honey bees

# MIN PATH DISTANCE:
# data10.csv = 262.147
# data20.csv = 592.594

# CYCLE: 8636
# PATH: [14, 12, 9, 8, 2, 0, 4, 15, 19, 16, 7, 10, 5, 17, 13, 6, 3, 11, 1, 18]
# DISTANCE: 595.663
# BEE: 6

# CYCLE: 18185
# PATH: [7, 19, 15, 3, 13, 17, 8, 9, 12, 14, 18, 2, 4, 5, 10, 11, 1, 0, 6, 16]
# DISTANCE: 518.534
# BEE: 34

# CYCLE: 17264
# PATH: [3, 0, 4, 6, 16, 2, 5, 10, 11, 1, 18, 14, 8, 9, 12, 17, 13, 19, 7, 15]
# DISTANCE: 512.567
# BEE: 35

import csv
import math
import random
import sys
from scipy.spatial import distance

# Burning questions:
#   - How do we know when optimal solution is found????
#   - Should cycle be per bee? How should it increment?? What if bee is close???

class Bee:
    def __init__(self, node_set):
        self.role = ''
        self.path = list(node_set) # stores all nodes in each bee, will randomize foragers
        self.distance = 0
        self.cycle = 0 # number of iterations on current solution

# class Bee:
#     def __init__(self):
#         self.role = ''
#         self.path = [] #
#         self.distance = 0
#         self.cycle = 0 # number of iterations on current solution


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
    Terminates at starting node to complete cycle
    """
    # Creates a copy of path, puts head at end of list.
    # Zip lists to create pairs of neighbor coords,
    # will create a cycle that terminates at starting node.
    new_path = list(path)
    new_path.insert(len(path), path[0])
    new_path = new_path[1:len(new_path)]

    coordinates = zip(path, new_path)
    distance = sum([table[i[0]][i[1]] for i in coordinates])
    return round(distance, 3)


def initialize_hive(population, data):
    """
    Initializes a hive and populates it with bees
    Bees will have a randomized path attribute
    """
    path = [x[0] for x in data]
    hive = [Bee(path) for i in range (0, population)]
    return hive


def assign_roles(hive, role_percentiles, table):
    """
    Assigns initial roles based on role percentiles
    to each bee in the hive.
    Assigns randomized path to forager bees.
    """
    population = len(hive)
    onlooker_count = math.floor(population * role_percentiles[0])
    forager_count = math.floor(population * role_percentiles[1])

    for i in range(0, onlooker_count):
        hive[i].role = 'O'
    for i in range(onlooker_count, (onlooker_count + forager_count)):
        hive[i].role = 'F'
        random.shuffle(hive[i].path)
        hive[i].distance = get_total_distance_of_path(hive[i].path, table)
    return hive


def forage(bee, table, limit):
    """
    Worker bee behavior, iteratively refines a potential shortest path
    by swapping randomly selected neighbor indices
    """
    # Gets a random index 0 to next to last element
    # - will go out of range if last element is chosen.
    random_idx = random.randint(0, len(bee.path) - 2)

    # Copies path, swaps two nodes, compares distance.
    new_path = list(bee.path)
    new_path[random_idx], new_path[random_idx + 1] = new_path[random_idx + 1], new_path[random_idx]
    new_distance = get_total_distance_of_path(new_path, table)
    if new_distance < bee.distance:
        bee.path = new_path
        bee.distance = new_distance
    else:
        bee.cycle += 1
    if bee.cycle >= limit: # If bee is not making progress
        bee.role = 'S'
    return bee.distance, list(bee.path)


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


def waggle_dance(hive, table, forager_limit):
    """
    Captures results from work of forager bees,
    chooses new random path for scouts to explore,
    returns results for overlookers to assess.
    """
    distances = []
    paths = []
    for i in range(0, len(hive)):
        if hive[i].role == 'F':
            distance, path = forage(hive[i], table, forager_limit)
            distances.insert(i, distance)
            paths.insert(i, path)
        elif hive[i].role == 'S':
            scout(hive[i])
            hive[i].role = 'F'
    return distances, paths

def overlooker(hive, distances, paths, scout_percentage):
    """
    Overlooker chooses best results,
    assigns new bee with least promising path to be a scout.
    """
    min_distance = min(distances)
    min_index = distances.index(min_distance)

    # get new scout bee indices
    scout_num = int(scout_percentage * len(distances))
    sort_distances = list(distances)
    sort_distances.sort()
    scouts = sort_distances[-scout_num - 1:]
    for scout in scouts:
        i = distances.index(scout)
        hive[i].role = 'S'
    return min_distance, min_index

def recruit(hive, best_path, best_distance, table, forager_limit):
    distances = []
    paths = []
    for i in range(0, len(hive)):
        if hive[i].role == 'O':
            hive[i].path = list(best_path)
            hive[i].distance = best_distance
            distance, path = forage(hive[i], table, forager_limit)
            distances.insert(i, distance)
            paths.insert(i, path)
    return distances, paths

#
# def overlooker(hive, distances, paths, scout_percentage):
#     """
#     Overlooker chooses best results,
#     assigns new bee with least promising path to be a scout.
#     """
#     min_distance = min(distances)
#     min_index = distances.index(min_distance)
#
#     # assign all bees to pursue best path:
#     assign_paths(hive, paths[min_index])
#     # get new scout bee indices
#     scout_num = int(scout_percentage * len(distances))
#     sort_distances = list(distances)
#     sort_distances.sort()
#     scouts = sort_distances[-scout_num - 1:]
#     for scout in scouts:
#         i = distances.index(scout)
#         hive[i].role = 'S'
#     return min_distance, min_index


def main():
    data = read_data_from_csv("data10.csv")
    #data = read_data_from_csv("sahara.csv")

    table = make_distance_table(data)
    population = 30
    forager_percent = 0.5
    onlooker_percent = 0.5
    role_percentiles = [onlooker_percent, forager_percent]
    scout_percentile = 0.05

    hive = initialize_hive(population, data)
    assign_roles(hive, role_percentiles, table)
    best_distance = sys.maxsize
    best_path = data
    forager_limit = 10 * len(data)
    cycle_limit = 2500
    cycle = 0

    while cycle < cycle_limit:
        distances, paths = waggle_dance(hive, table, forager_limit)
        print(distances)
        min_distance, min_index = overlooker(hive, distances, paths, scout_percentile)
        if min_distance < best_distance:
            best_distance = min_distance
            best_path = list(paths[min_index])
            print("CYCLE: {}".format(cycle))
            print("PATH: {}".format(best_path))
            print("DISTANCE: {}".format(best_distance))
            print("BEE: {}".format(min_index))
            print("\n")
        distances, paths = recruit(hive, best_path, best_distance, table, forager_limit)
        if min_distance < best_distance:
            best_distance = min_distance
            best_path = list(paths[min_index])
            print("CYCLE: {}".format(cycle))
            print("PATH: {}".format(best_path))
            print("DISTANCE: {}".format(best_distance))
            print("BEE: {}".format(min_index))
            print("\n")
        cycle += 1

#------------------------------------------------------------------------------------#

if __name__ == '__main__':
    main()
