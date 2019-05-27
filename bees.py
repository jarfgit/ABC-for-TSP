# bees.py
# A solution to the Traveling Salesman Problem
# that mimics the foraging behavior of honey bees

import csv
import math
import random
import sys
from scipy.spatial import distance

# Burning questions:
#   - How do we know when optimal solution is found????
#   - Should cycle be per bee? How should it increment?? What if bee is close???

class Bee:
  def __init__(self, node_set, table):
    self.role = 'F'
    # creates an initial randomized path for each bee to explore
    randomized_path = list(node_set)
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

def initialize_hive(population, data, table):
    """
    Initializes a hive and populates it with bees
    Bees will have a randomized path attribute
    """
    path = [x[0] for x in data]
    hive = [Bee(path, table) for i in range (0, population)]
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

def overlooker(hive, distances, paths):
    """
    Overlooker chooses best results,
    assigns new bee with least promising path to be a scout.
    """
    min_distance = min(distances)
    min_index = distances.index(min_distance)
    max_index = distances.index(max(distances))
    hive[max_index].role = 'S'
    return min_distance, min_index


def main():
    data = read_data_from_csv("data.csv")
    table = make_distance_table(data)
    # population = len(data) * 2
    population = len(data)

    hive = initialize_hive(population, data, table)
    best_distance = sys.maxsize
    best_path = data
    forager_limit = 100
    cycle_limit = 10000
    cycle = 0

    while cycle < cycle_limit:
        distances, paths = waggle_dance(hive, table, forager_limit)
        min_distance, min_index = overlooker(hive, distances, paths)
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
