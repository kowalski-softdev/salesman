import unittest
from genetic_TSP import Individual_TSP as Ind

class TestGeneticTSP(unittest.TestCase):
    def setUp(self):
        self.genome = [0,1,2,3]
        self.cyclical_genome = [0,1,2,3,0]
    
    def tearDown(self):
        del self.genome
        del self.cyclical_genome

    def test_Individual_initialization_no_starting_position_no_cyclical(self):
        #no starting position, no cyclical
        ind = Ind(self.genome, starting_position=None, cyclical=False)
        self.assertEqual(ind.genome, [0,1,2,3])

    def test_Individual_initialization_starting_position_no_cyclical(self):
        #starting position, no cyclical
        ind = Ind(self.genome, starting_position=0, cyclical=False)
        self.assertEqual(ind.genome, [0,1,2,3])
        ind = Ind(self.genome, starting_position=2, cyclical=False)
        self.assertEqual(ind.genome, [2,0,1,2,3])

    def test_Individual_initialization_no_starting_position_cyclical(self):
        #no starting position, cyclical
        ind = Ind(self.genome, starting_position=None, cyclical=True)
        self.assertEqual(ind.genome, [0,1,2,3,0])
        ind = Ind(self.cyclical_genome, starting_position=None, cyclical=True)
        self.assertEqual(ind.genome, [0,1,2,3,0])

    def test_Individual_initialization_starting_position_cyclical(self):
        #starting position, cyclical
        ind = Ind(self.genome, starting_position=0, cyclical=True)
        self.assertEqual(ind.genome, [0,1,2,3,0])
        ind = Ind(self.cyclical_genome, starting_position=0, cyclical=True)
        self.assertEqual(ind.genome, [0,1,2,3,0])
        #it's changed by Individual_TSP initialization
        #it's shallow copy of list
        self.genome = [0,1,2,3]
        self.cyclical_genome = [0,1,2,3,0]
        ind = Ind(self.genome, starting_position=2, cyclical=True)
        self.assertEqual(ind.genome, [2,0,1,2,3,2])
        ind = Ind(self.cyclical_genome, starting_position=2, cyclical=True)
        self.assertEqual(ind.genome, [2,0,1,2,3,0,2])

if __name__ == "__main__":
    unittest.main()
