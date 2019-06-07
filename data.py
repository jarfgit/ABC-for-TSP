# generate_graph.py
# generates a list of tuples that contain node ids and (x,y) coordinates
# writes data to a file

import csv
import os
import random
import re

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


def make_csv(data_list, file_name):
    """
    Writes data to csv file
    """
    with open(file_name, "w+") as f:
        writer = csv.writer(f)
        writer.writerows(data_list)
    f.close()


def generate_data(node_num, x_max, y_max):
    """
    Generates graph data and csv for a test run.
    """
    file_name = "data/data_{}.csv".format(num_nodes)
    graph = make_graph(num_nodes, x_max, y_max)
    make_csv(graph, file_name)


def read_data_from_csv(file_path, file_name):
    """
    Returns data read from file
    """
    data_list = []
    types = [int,str,float,str]
    with open(file_path + file_name) as f:
        reader = csv.reader(f)
        for row in f:
            regex = re.compile("\[(.*?)\]")
            result = re.sub(regex, "", row)
            result_list = [s for s in result.split(',')]
            result_list = [t(x) for (t,x) in zip(types, result_list)]
            result_list.append(file_name)
            data_list.append(result_list)
    return data_list


def get_accuracy_count(data_list, optimal_distance):
    """
    Processes data list from file to find accuracy count.
    Returns accuracy count.
    """
    count = sum(1 for i in data_list if optimal_distance in i)
    return count


def get_bee_count(data_list):
    """
    Processes data list from file to find bee count.
    Returns #foragers, # recruits per test run.
    """
    count = sum(1 for i in data_list if "F\n" in i)
    return count, len(data_list) - count


def get_cycle_stats(data_list):
    """
    Calculates cycle statistics for test run.
    Returns min, max, avg cycle count.
    """
    cycles = [data[0] for data in data_list]
    min_cycles = min(cycles)
    max_cycles = max(cycles)
    avg_cycles = sum(cycles) / len(cycles)
    return min_cycles, max_cycles, avg_cycles


def gather_results(data, optimal_distance):
    """
    Collates accuracy, bee count, cycle stats per test file.
    Returns list to be written to csv.
    """
    file_name = data[-1][-1]
    accuracy = get_accuracy_count(data, optimal_distance)
    foragers, recruits = get_bee_count(data)
    min, max, avg = get_cycle_stats(data)
    results = [accuracy, foragers, recruits, min, max, avg, file_name]
    return results


def make_results_file(file_name, result_list):
    """
    Writes data to csv file
    """
    with open(file_name, 'a') as f:
        writer = csv.writer(f)
        writer.writerow(["accuracy", "foragers", "recruits", "min_cycles", "max_cycles", "avg_cycles", "file_name"])
        for result in result_list:
            writer.writerow(result)
    f.close()


def process_results(num_nodes, optimal_distance):
    """
    Processed all results in a directory.
    Saves results to file in results in compiled_data directory.
    """
    new_file = "results/compiled_data/{}_nodes_results.txt".format(num_nodes)
    data_files = os.listdir("results/{}_nodes/".format(num_nodes))

    data_list = []
    result_list = []

    for data_file in data_files:
        data = read_data_from_csv("results/{}_nodes/".format(num_nodes), data_file)
        data_list.append(data)

    for data in data_list:
        result = gather_results(data, optimal_distance)
        result_list.append(result)

    result_list.sort(reverse = True)

    # for result in result_list:
    make_results_file(new_file, result_list)


#==============================================

def run():
    num_nodes = 12
    x_max = 100
    y_max = 100

    # optimal_distance = 262.174 # 10 nodes
    # optimal_distance = 310.951 # 11 nodes
    optimal_distance = 333.99  # 12 nodes

    # generate_data(num_nodes, x_max, y_max)
    process_results(num_nodes, optimal_distance)

run()
