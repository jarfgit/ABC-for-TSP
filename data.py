# generate_graph.py
# generates a list of tuples that contain node ids and (x,y) coordinates
# writes data to a file

import random

def make_graph(num_nodes, x_max, y_max):
  graph = []
  for i in range(0, num_nodes):
      x = random.randint(1,x_max)
      y = random.randint(1,y_max)
      graph.append((i + 1, (x,y)))
  return graph

def write_graph_csv(graph_list, file_name):
    f = open(file_name, "w+")
    f.write('{}'.format(graph_list))
    f.close()

###################################################

num_nodes = 10
x_max = 100
y_max = 100
file_name = "data.txt"

graph = make_graph(num_nodes, x_max, y_max)
write_graph_csv(graph, file_name)
