# bees.py
# A solution to the Traveling Salesman Problem
# that mimics the foraging behavior of honey bees

import csv
import math
import random
from scipy.spatial import distance

class Bee:
  def __init__(self, num_nodes):
    self.role = 'O'  # 0 = onlooker, 1 = forager, 2 = scout
    self.path = [i for i in range(0, num_nodes)] #
    random.shuffle(self.path) # creates an initial randomized path for each bee to explore
    # TODO: figure out what to do wih errors?????
    # self.error = error(self.path) # bee's current error

def read_data_from_csv(file_name):
    """
    Returns data read from file
    """
    data_list = []
    with open(file_name) as f:
        reader = csv.reader(f)
        data_list = [[int(s) for s in row.split(',')] for row in f]
    return data_list

def convert_data_to_coords(data_row):
    """
    Converts the x and y coordinate values from data_list
    into a set of coordinates (i.e. a point)
    """
    return((data_row[1],data_row[2]))

def get_distance_between_nodes(n1, n2):
    """
    Calculates the Euclidean distance between two nodes
    """
    return distance.euclidean(n1, n2)

def get_total_distance_of_path(path, data_list):
    """
    Calculates the total distance of an individual bee's path
    """
    coordinates = [convert_data_to_coords(data_list[i]) for i in path]
    distance = 0
    for i in range(0,len(coordinates) - 2):
        distance += get_distance_between_nodes(coordinates[i], coordinates[i+1])
    return distance

# Initialize hive
def initialize_hive(population, path_len):
    hive = [Bee(path_len) for i in range (0, population)]
    return hive

def assign_roles(hive, role_percentiles):
    population = len(hive)
    onlooker_count = math.floor(population * role_percentiles[0])
    forager_count = math.floor(population * role_percentiles[1])
    scout_count = population - (onlooker_count + forager_count)

    for i in range(0, onlooker_count):
        hive[i].role = 'O'
    for i in range(onlooker_count, (onlooker_count + forager_count)):
        hive[i].role = 'F'
    for i in range ((len(hive) - scout_count), len(hive)):
        hive[i].role = 'S'

    return hive



data = read_data_from_csv("data.csv")
# print(type(data))
print(data)
# p1 = convert_data_to_coords(data[0])
# p2 = convert_data_to_coords(data[1])
# print(get_distance(p1, p2))
bee = Bee(len(data))
# print(len(data))
print(bee.path)
# print(get_total_distance_of_path(bee.path, data))
# print((initialize_hive(100, len(data)))[0].path)
hive = initialize_hive(100, len(data))
hive = assign_roles(hive, [0.5,0.25,(1-0.5-0.25)])

for bee in hive:
    print("bee: {} role: {}".format(bee.path, bee.role))







# TODO:
# write artifical bee colony pseudo for TSP
# write artifical bee colony code
# https://medium.com/cesar-update/a-swarm-intelligence-approach-to-optimization-problems-using-the-artificial-bee-colony-abc-5d4c0302aaa4
# https://towardsdatascience.com/a-modified-artificial-bee-colony-algorithm-to-solve-clustering-problems-fc0b69bd0788
