from collections import defaultdict

class Graph:
    """
    A class used to represent a graph.
    
    A graph can be undirected or directed, weighted or not.
    The unweighted graph is created by not passing 'weight' parameters
    to add_edge method, default value of 1 is used.

    ...

    Attributes
    ----------
    _adjacency_dict: defaultdict(dict)
        dictionary of dictionaries; _adjacency_dict['A']['B] = 5 means
        that edge from vertex 'A' to vertex 'B' exists and its values
        is 5
    _directed: bool
        a flag denoting if graph is directed or not (default True)
    vertices_count: int
        a number of vertices in the graph
    vertices_list: list
        a list of all vertices in the graph (keys of _adjacency_dict)

    Methods
    -------
    add_edge(source, target, weight=1)
        Adds an edge from source to target of value weight, represented
        as a dictionary inside a dictionary; adjacency[source][target]
    calculate_cost(path)
        Returns a sum of edges weights between vertices in path.
        path = ['A','B','C'] returns sum of edges from 'A' to 'B' and
        from 'B' to 'C'.
    is_path_traversable(path)
        Returns True if there're edges between every element of
        the path and the next element. Returns False otherwise.
    """
        
    def __init__(self, graph=None, directed:bool=True):
        self._adjacency_dict = defaultdict(dict)
        if graph is not None:
            self._adjacency_dict.update(graph)
            for vertex in graph.keys():
                for target_vertex in self._adjacency_dict[vertex]:
                    if self._adjacency_dict.get(target_vertex, None) is None:
                        self._adjacency_dict[target_vertex] = {}
        self._directed = directed

    def add_edge(self, source: str, target: str, weight:int|float=1) -> None:
        self._adjacency_dict[source].update({target: weight})
        if not self._directed:
            self._adjacency_dict[target].update({source: weight})
        else:
            if self._adjacency_dict.get(target) is None:
                self._adjacency_dict[target]

    def calculate_cost(self, path: list) -> float:
        i = 0
        cost = 0.0
        while i<len(path)-1:
            try:
                cost += self._adjacency_dict[path[i]][path[i+1]]
            except KeyError as e:
                raise KeyError(f"There's no edge from {path[i]} to {path[i+1]}")
            i += 1
        return cost

    def is_path_traversable(self, path: list) -> bool:
        if len(path) == 0:
            raise ValueError('The path cannot be empty.')

        if len(path) == 1:
            if path[0] in self.vertices_list:
                return True
            else:
                return False

        i = 0
        while i < len(path)-1:
            try:
                condition = self._adjacency_dict.get(path[i]).get(path[i+1])
            except (KeyError, AttributeError):
                return False
            if condition is None:
                return False
            i += 1
        return True

    def connected_to(self, source):
        """Returns list of vertices connected by edge from source, if none returns empty list."""
        return list(self._adjacency_dict[source])

    @property
    def vertices_count(self):
        """The number of vertices in the graph.""" 
        return len(self._adjacency_dict)

    @property
    def vertices_list(self):
        """The list of names for vertices."""
        return list(self._adjacency_dict)

if __name__ == "__main__":
    tr_map = Graph()
    tr_map.add_edge('A','B',2)
    tr_map.add_edge('B','A',1) 
    tr_map.add_edge('B','C',3)
    assert tr_map.calculate_cost(['A','B','C']) == 5
    print(f"Everything's fine")
    print(tr_map.vertices_count)
    #print(tr_map.is_path_traversable(['A','B','C']))
    tr_map.add_edge('D','E',7)
    print(tr_map.vertices_count)
    #print(tr_map.is_path_traversable(['A','B','C','D','E']))

    tr_map = Graph(graph={'A':{'B':1, 'D':2, 'E':1},
                'B':{'C':1, 'A':2},
                'C':{'D':1, 'B':2},
                'D':{'A':1, 'C':2},
                'E':{'A':1}
                })
    path = ['E','A','B','C','D','E']
    assert (tr_map.is_path_traversable(path) == False)
    path = ['E']
    print(tr_map._adjacency_dict)
    assert tr_map.is_path_traversable(path)
    path = ['E','A','B','C','D','A','E']
    assert tr_map.is_path_traversable(path) 
