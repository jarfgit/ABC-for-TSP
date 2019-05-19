# bees.py
# A solution to the Traveling Salesman Problem
# that mimics the foraging behavior of honey bees

import csv
import random
from scipy.spatial import distance

class Bee:
  def __init__(self, num_nodes):
    self.phase = 0  # 0 = onlooker, 1 = employed, 2 = scout
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
        for row in f:
            parsed_row = [int(s) for s in row.split(',')]
            data_list.append(parsed_row)
    return data_list

def convert_data_to_coords(data_row):
    """
    Converts the x and y coordinate values from data_list
    into a set of coordinates (i.e. a point)
    """
    return((data_row[1],data_row[2]))

def get_distance(p1, p2):
    """
    Calculates the Euclidean distance between two points
    """
    return distance.euclidean(p1, p2)


data = read_data_from_csv("data.csv")
# print(type(data))
# print(data)
# p1 = convert_data_to_coords(data[0])
# p2 = convert_data_to_coords(data[1])
# print(get_distance(p1, p2))
bee = Bee(len(data))
# print(len(data))
print(bee.path)




# TODO:
# write artifical bee colony pseudo for TSP
# write artifical bee colony code
# https://medium.com/cesar-update/a-swarm-intelligence-approach-to-optimization-problems-using-the-artificial-bee-colony-abc-5d4c0302aaa4
# https://towardsdatascience.com/a-modified-artificial-bee-colony-algorithm-to-solve-clustering-problems-fc0b69bd0788
