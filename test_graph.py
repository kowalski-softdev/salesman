import unittest
from graph import Graph

class TestGraph(unittest.TestCase):
    def setUp(self):
        self.graph = Graph()
        self.undirected_graph = Graph(directed=False)

    def tearDown(self):
        self.graph = None

    def test_add_edge_existing_vertices_directed_graph(self):
        """
        Test that it can add an edge between vertices. Directed graph.
        """
        #unexisting vertices, unweighted graph (default value)
        self.graph.add_edge('A','B')
        self.assertEqual(self.graph._adjacency_dict['A']['B'], 1)
        #updating existng edge
        self.graph.add_edge('A','B', 5)
        self.assertEqual(self.graph._adjacency_dict['A']['B'], 5)
        #graph is directed - checking that reversed edge didn't appear
        with self.assertRaises(KeyError):
            self.graph._adjacency_dict['B']['A']
        #checking if there is no self-directed edge
        with self.assertRaises(KeyError):
            self.graph._adjacency_dict['A']['A']
        #adding edge from existing vertex to unexisting vertex
        self.graph.add_edge('B','C', 15)
        self.assertEqual(self.graph._adjacency_dict['B']['C'], 15)
        #checking old edge if it remains unchanged
        self.assertEqual(self.graph._adjacency_dict['A']['B'], 5)
        #adding edge from unexisting vertex to existing vertex
        self.graph.add_edge('D','C',4)
        self.assertEqual(self.graph._adjacency_dict['D']['C'], 4)
        #adding edge between existing vertices
        self.graph.add_edge('A','D',2)
        self.assertEqual(self.graph._adjacency_dict['A']['D'], 2)

        #unexisting vertices, unweighted undirected_graph (default value)
        self.undirected_graph.add_edge('A','B')
        self.assertEqual(self.undirected_graph._adjacency_dict['A']['B'], 1)
        self.assertEqual(self.undirected_graph._adjacency_dict['B']['A'], 1)
        #updating existng edge
        self.undirected_graph.add_edge('A','B', 5)
        self.assertEqual(self.undirected_graph._adjacency_dict['A']['B'], 5)
        #undirected_graph is directed - checking that reversed edge did appear and was updated
        self.assertEqual(self.undirected_graph._adjacency_dict['B']['A'], 5)
        #checking if there is no self-directed edge
        with self.assertRaises(KeyError):
            self.undirected_graph._adjacency_dict['A']['A']
        #adding edge from existing vertex to unexisting vertex
        self.undirected_graph.add_edge('B','C', 15)
        self.assertEqual(self.undirected_graph._adjacency_dict['B']['C'], 15)
        #checking old edge if it remains unchanged
        self.assertEqual(self.undirected_graph._adjacency_dict['A']['B'], 5)
        #adding edge from unexisting vertex to existing vertex
        self.undirected_graph.add_edge('D','C',4)
        self.assertEqual(self.undirected_graph._adjacency_dict['D']['C'], 4)
        #adding edge between existing vertices
        self.undirected_graph.add_edge('A','D',2)
        self.assertEqual(self.undirected_graph._adjacency_dict['A']['D'], 2)


    def test_calculate_cost(self):
        self.graph.add_edge('A','B',5)
        self.graph.add_edge('B','C',10)
        self.assertEqual(self.graph.calculate_cost(['A','B','C']), 15)
        with self.assertRaises(KeyError):
            self.graph.calculate_cost(['A','C'])

        self.undirected_graph.add_edge('A','B',5)
        self.undirected_graph.add_edge('B','C',10)
        self.assertEqual(self.undirected_graph.calculate_cost(['A','B','C']), 15)
        self.assertEqual(self.undirected_graph.calculate_cost(['C','B','A']), 15)
        with self.assertRaises(KeyError):
            self.undirected_graph.calculate_cost(['A','C'])

    def test_is_path_traversable(self):
        self.graph.add_edge('A','B',5)
        self.graph.add_edge('B','C',10)
        self.assertTrue(self.graph.is_path_traversable(['A','B','C']))
        self.assertFalse(self.graph.is_path_traversable(['A','C']))

        self.undirected_graph.add_edge('A','B',5)
        self.undirected_graph.add_edge('B','C',10)
        self.assertTrue(self.undirected_graph.is_path_traversable(['A','B','C']))
        self.assertTrue(self.undirected_graph.is_path_traversable(['C','B','A']))
        self.assertFalse(self.undirected_graph.is_path_traversable(['A','C']))

    def test_vertices_count(self):
        self.assertEqual(self.graph.vertices_count, 0)
        self.graph.add_edge('A','B',5)
        self.assertEqual(self.graph.vertices_count, 2)
        self.graph.add_edge('B','C',10)
        self.assertEqual(self.graph.vertices_count, 3)

        self.assertEqual(self.undirected_graph.vertices_count, 0)
        self.undirected_graph.add_edge('A','B',5)
        self.assertEqual(self.undirected_graph.vertices_count, 2)
        self.undirected_graph.add_edge('B','C',10)
        self.assertEqual(self.undirected_graph.vertices_count, 3)

    def test_vertices_list(self):
        #note: dictionaries are ordered since python 3.7
        self.assertEqual(self.graph.vertices_list, [])
        self.graph.add_edge('A','B',5)
        self.assertEqual(self.graph.vertices_list, ['A','B'])
        self.graph.add_edge('B','C',10)
        self.assertEqual(self.graph.vertices_list, ['A','B','C'])

        self.assertEqual(self.undirected_graph.vertices_list, [])
        self.undirected_graph.add_edge('A','B',5)
        self.assertEqual(self.undirected_graph.vertices_list, ['A','B'])
        self.undirected_graph.add_edge('B','C',10)
        self.assertEqual(self.undirected_graph.vertices_list, ['A','B','C'])

if __name__ == "__main__":
    unittest.main()
