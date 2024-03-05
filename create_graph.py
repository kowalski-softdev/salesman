from random import randint
from graph import Graph
from math import sqrt

def create_graph(vertices_num:int) -> dict:
    class Coordinate:
        def __init__(self, x, y):
            self.x = x
            self.y = y
        def calculate_distance(self, other) -> float:
            x_side = abs(self.x - other.x)
            y_side = abs(self.y - other.y)
            distance = sqrt(x_side**2 + y_side**2)
            return distance
    
    vertices_arr = []
    for _ in range(vertices_num):
        vertices_arr.append(Coordinate(randint(0,100), randint(0,100)))

    graph = Graph()
    for source_idx, source_vertex in enumerate(vertices_arr):
        for target_idx, target_vertex in enumerate(vertices_arr):
            if source_idx != target_idx:
                graph.add_edge(source_idx, target_idx, source_vertex.calculate_distance(target_vertex))

    return graph

if __name__ == "__main__":
    vertices_num = int(input("How many vertices? "))
    d = create_graph(vertices_num)._adjacency_dict
    type(d)
    print(d)
