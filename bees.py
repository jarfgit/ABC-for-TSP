# bees.py
# A solution to the Traveling Salesman Problem
# that mimics the foraging behavior of honey bees

def get_data(file_name):
    with open(file_name) as f:
        data = f.read().replace('\n', '')
    return data


data = get_data("data.txt")
print(data)
