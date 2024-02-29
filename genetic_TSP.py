from graph import Graph
from functools import total_ordering
from random import sample, randint, choice
from copy import deepcopy

class Individual_TSP:

    def __init__(self, genome, starting_position=None, cyclical=False):
        if starting_position and genome[0] != starting_position:
            self.genome = [starting_position]
            self.genome[1:] = genome
        else:
            self.genome = genome
        if cyclical and self.genome[0] != self.genome[-1]:
            self.genome.append(self.genome[0])
        self.score = float('+inf')

class Genetic_TSP:

    def __init__(self, graph: dict, population_size:int=100, starting_position=None, cyclical=False):
        self._problem_map = Graph(graph)
        self._population_size = population_size
        self._population = None
        self._generation = 0
        self._min_genome_length = graph.vertices_count
        #list of lists for when nodes in graph have to be visited multiple times
        #first position is empty
        self._genome_pool = [graph.vertices_list * i for i in range(0,11)]
        #unless value is None it will start from this position
        self._starting_position = starting_position
        #if True the path will be ending in the same place as it started
        self._cyclical = cyclical
        self._best_ind = None

    def remove_unfeasible(self) -> None:
        # removes from population paths that cannot be traversed
        self._population = [individual for individual in self._population if self._problem_map.is_path_traversable(individual.genome)]

    def calculate_fitness(self) -> None:
        for individual in self._population:
            individual.score = self._problem_map.calculate_cost(individual.genome)

    def sort_by_fitness(self) -> None:
        self._population.sort(key=lambda individual: individual.score)

    def is_feasible(self, ind:Individual_TSP) -> bool:
        if self._cyclical and ind.genome[0] != ind.genome[-1]:
            return False
        if self._starting_position is not None and ind.genome[0] != self._starting_position:
            return False
        if not self._problem_map.is_path_traversable(ind.genome):
            return False
        else:
            for gene in self._genome_pool[1]:
                if gene not in ind.genome:
                    return False
        return True

    def populate(self) -> None:
        self._population = []
        safety_check = self._population_size * 1000
        while len(self._population) < self._population_size and safety_check > 0:
            safety_check -= 1
            genome = []
            if self._starting_position:
                genome.append(self._starting_position)
            else:
                genome.append(choice(self._genome_pool[1]))
            #checks if all nodes of the graph will be visited
            while not(all(gene in genome for gene in self._genome_pool[1])) and len(genome) < len(self._genome_pool[1]*10):
                #connected nodes
                viable_genes = self._problem_map.connected_to(genome[-1])
                if not viable_genes:
                    break
                genome.append(choice(viable_genes))
            ind = Individual_TSP(genome, self._starting_position, self._cyclical)
            if self.is_feasible(ind):
                self._population.append(ind)

    def choose_best(self) -> None:
        self.calculate_fitness()
        self._population.sort(key=lambda ind: ind.score)
        if self._population:
            if self._best_ind is None:
                self._best_ind = self._population[0]
            elif self._best_ind.score > self._population[0].score:
                self._best_ind = self._population[0]

    def next_generation(self) -> None:
        self._generation += 1
        #calculating fitness and sorting
        self.choose_best()
        #culling population
        if len(self._population) == 0:
            raise ValueError('Population is 0. No solution was found, next generation cannot be generated.')
        if self._population_size < 11:
            fraction = 1
        fraction = self._population_size//10
        surviving_population = self._population[:fraction]
        self._population = []
        for ind in surviving_population:
            safety_check = 10000
            count = 0
            while True and safety_check > 0:
                new_ind = self.mutate(ind)
                if self.is_feasible(new_ind):
                    self._population.append(new_ind)
                    count += 1
                    if count == 10:
                        break
                safety_check -= 1

    def mutate(self, individual) -> Individual_TSP:
        new_ind = Individual_TSP(deepcopy(individual.genome), self._starting_position, self._cyclical)
        if randint(0,100) <= 10:
            del new_ind.genome[randint(0,len(new_ind.genome)-1)]
        elif randint(0,100) <= 10:
            new_ind.genome.insert(randint(0,len(new_ind.genome)), new_ind.genome[randint(0, len(new_ind.genome)-1)])

        pos1 = randint(0, len(new_ind.genome)-1)
        pos2 = randint(0, len(new_ind.genome)-1)
        if pos1 > pos2:
            pos1, pos2 = pos2, pos1
        if randint(0,100) <= 90:
            new_ind.genome[pos1], new_ind.genome[pos2] = new_ind.genome[pos2], new_ind.genome[pos1]
        elif randint(0,100) < 50:
            new_ind.genome[pos1:pos2] = new_ind.genome[pos2-1:pos1-1:-1]
        else:
            moved = new_ind.genome[pos1:pos2]
            del new_ind.genome[pos1:pos2]
            pos3 = randint(0, len(new_ind.genome)-1)
            new_ind.genome[pos3:pos3] = moved
        return new_ind

if __name__ == "__main__":
    adj_dict = {'A':{'B':1, 'D':2},
                'B':{},
                'C':{'D':1},
                'D':{'A':1, 'C':2},
                'E':{'A':1}
                }
    problem_map = Graph(graph=adj_dict)
    print('\nNon-cyclical test impossible graph\n')
    test_tube = Genetic_TSP(problem_map, population_size=100)
    test_tube.populate()
    test_tube.calculate_fitness()
    for ind in test_tube._population:
        print(f"{ind.genome} fitnes: {ind.score}")

    adj_dict = {'A':{'B':1, 'D':2},
                'B':{'C':1, 'A':2},
                'C':{'D':1, 'B':2},
                'D':{'A':1, 'C':2},
                'E':{'A':1}
                }
    problem_map = Graph(graph=adj_dict)
    print('\nNon-cyclical test possible graph\n')
    test_tube = Genetic_TSP(problem_map, population_size=100)
    test_tube.populate()
    test_tube.calculate_fitness()
    for ind in test_tube._population:
        print(f"{ind.genome} fitnes: {ind.score}")

    print('\nCyclical test (impossible graph)\n')
    test_tube = Genetic_TSP(problem_map, population_size=100, cyclical=True)
    test_tube.populate()
    test_tube.calculate_fitness()
    for ind in test_tube._population:
        print(f"{ind.genome} fitnes: {ind.score}")

    adj_dict = {'A':{'B':1, 'D':2, 'E':1},
                'B':{'C':1, 'A':2},
                'C':{'D':1, 'B':2},
                'D':{'A':1, 'C':2},
                'E':{'A':1}
                }
    problem_map = Graph(graph=adj_dict)
    print('\nCyclical test possible graph (genome length)\n')
    test_tube = Genetic_TSP(problem_map, population_size=100, cyclical=True)
    test_tube.populate()
    test_tube.calculate_fitness()
    if not test_tube._population: print('Empty population')
    for ind in test_tube._population:
        print(f"{ind.genome} fitnes: {ind.score}")

    problem_map = Graph(graph=adj_dict)
    print('\nCyclical test possible graph (genome length) with starting position "E"\n')
    test_tube = Genetic_TSP(problem_map, population_size=100, starting_position='E', cyclical=True)
    test_tube.populate()
    test_tube.calculate_fitness()
    if not test_tube._population: print('Empty population')
    for ind in test_tube._population:
        print(f"{ind.genome} fitnes: {ind.score}")

    problem_map = Graph(graph=adj_dict)
    print('\nCyclical test possible graph (genome length) with starting position "B"\n')
    test_tube = Genetic_TSP(problem_map, population_size=100, starting_position='B', cyclical=True)
    test_tube.populate()
    test_tube.calculate_fitness()
    if not test_tube._population: print('Empty population')
    for ind in test_tube._population:
        print(f"{ind.genome} fitnes: {ind.score}")

    adj_dict = {'A':{'B':1, 'C':1, 'D':2, 'E':1},
                'B':{'C':1, 'A':2, 'D':1, 'E':1},
                'C':{'D':1, 'B':2, 'A':1, 'E':1},
                'D':{'A':1, 'C':2, 'B':1, 'E':1},
                'E':{'A':1, 'B':1, 'C':1, 'D':5}
                }

    problem_map = Graph(graph=adj_dict)
    print('\nCyclical test possible graph (more interconnected) (genome length) without a starting position \n')
    test_tube = Genetic_TSP(problem_map, population_size=100, starting_position=None, cyclical=True)
    test_tube.populate()
    test_tube.calculate_fitness()
    test_tube.sort_by_fitness()
    if not test_tube._population: print('Empty population')
    for ind in test_tube._population:
        print(f"{ind.genome} fitnes: {ind.score}")

    print('\nNew kind of problem!!!\n')
    from collections import defaultdict
    adj_dict = defaultdict(dict)
    for key in range(0,20):
        adj_dict[key] = {}
    for key in adj_dict:
        for target in adj_dict:
            if key+1 == target or (target==0 and key==19):
                adj_dict[key].update({target:1})
            else:
                adj_dict[key].update({target:randint(2,50)})

    from time import time
    start = time()
    new_start_time = start
    problem_map = Graph(graph=adj_dict)
    test_tube = Genetic_TSP(problem_map, population_size=1000, starting_position=0, cyclical=True)
    test_tube.populate()
    test_tube.choose_best()
    print(test_tube._best_ind.genome)
    print(f'score={test_tube._best_ind.score}')
    print()
    best = test_tube._best_ind
    while test_tube._generation < 1 and test_tube._best_ind.score > 20:
        test_tube.next_generation()
        test_tube.choose_best()
        new_best = test_tube._best_ind
        if new_best is not best:
            best = new_best
            print(new_best.genome)
            print(f'score={new_best.score}')
            print(f'length={len(new_best.genome)}')
            print(f'absolute time={time()-start:.02f} seconds')
            print(f'Since last best={(time()-new_start_time):.02f} seconds')
            new_start_time = time()
    print(f'It toook {time()-start} seconds')

    from time import sleep
    print('*********************'.center(80))
    print('NEW GAME'.center(80))
    for key in range(20,40):
        adj_dict[key] = {}
        for _ in range(0,10):
            adj_dict[key].update({randint(0,key-1):randint(1,50)})
    for key in range(0,20):
        for _ in range(0,5):
            adj_dict[key].update({randint(20,39):randint(1,50)})
    #print(adj_dict)
    problem_map = Graph(graph=adj_dict)
    test_tube = Genetic_TSP(problem_map, population_size=1000, starting_position=None, cyclical=False)
    #NEW POPULATE TEST
    test_tube.populate()
    print(len(test_tube._population))
    test_tube.choose_best()
    print(len(test_tube._population))
    print(test_tube._best_ind.genome)
    print(f'score={test_tube._best_ind.score}')
    print()
    best = test_tube._best_ind
    from collections import Counter
    while test_tube._generation < 10000000 and test_tube._best_ind.score > 20:
        test_tube.next_generation()
        test_tube.choose_best()
        new_best = test_tube._best_ind
        if new_best is not best:
            best = new_best
            print(new_best.genome)
            print(f'score={new_best.score}')
            print(f'length={len(new_best.genome)}')
            print(f'absolute time={time()-start:.02f} seconds')
            print(f'Since last best={(time()-new_start_time):.02f} seconds')
            print(f'{sorted(new_best.genome)}')
            counter = Counter(new_best.genome)
            print(f'Most visited: {counter.most_common(1)}')
            print('-'*20)
            new_start_time = time()
    print(f'It toook {time()-start} seconds')


