from collections import defaultdict

class Graph:
	
    def __init__(self, directed=True):
        self._adjacency_dict = defaultdict(dict)
        self._directed = directed

    def add_edge(self, source: str, target: str, weight:int|float=1) -> None:
        self._adjacency_dict[source].update({target: weight})
        if not self._directed:
            self._adjacency_dict[target].update({source: weight})

    def calculate_cost(self, path: list) -> int|float:
        i = 0
        cost = 0
        while i<len(path)-1:
            try:
                cost += self._adjacency_dict[path[i]][path[i+1]]
            except KeyError as e:
                raise KeyError(f"The path cannot be traveled from {path[i]} to {path[i+1]}")
            i += 1
        return cost

    #does the path can be traversed
    def is_path_traversable(self, path: list) -> bool:
        i = 0
        while i < len(path)-1:
            try:
                self._adjacency_dict[path[i]][path[i+1]]
            except KeyError:
                return False
            i += 1
        return True

    @property
    def vertices_count(self):
        return len(self._adjacency_dict)

    @property
    def vertices_list(self):
        return list(self._adjacency_dict)

if __name__ == "__main__":
    tr_map = Graph()
    tr_map.add_edge('A','B',2)
    tr_map.add_edge('B','A',1) 
    tr_map.add_edge('B','C',3)
    assert tr_map.calculate_cost(['A','B','C']) == 5
    print(f"Everything's fine")
    print(tr_map.vertices_count)
    print(tr_map.is_path_traversable(['A','B','C']))
    tr_map.add_edge('D','E',7)
    print(tr_map.vertices_count)
    print(tr_map.is_path_traversable(['A','B','C','D','E']))
