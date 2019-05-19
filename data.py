# generate_graph.py
# generates a list of tuples that contain node ids and (x,y) coordinates
# writes data to a file

import csv
import random

def make_graph(num_nodes, x_max, y_max):
    """
    Generates a list of nodes and coordinates
    """
    graph = []
    for i in range(0, num_nodes):
        x = random.randint(1,x_max)
        y = random.randint(1,y_max)
        graph.append([i,x,y])
    return graph


def make_csv(data_list):
    """
    Writes data to csv file
    """
    with open("data.csv", "w+") as f:
        writer = csv.writer(f)
        writer.writerows(data_list)
    f.close()





###################################################

num_nodes = 10
x_max = 100
y_max = 100
file_name = "data.txt"

graph = make_graph(num_nodes, x_max, y_max)
print(graph)
make_csv(graph)
