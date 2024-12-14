import random

class GAmusic:
    def __init__(self,population_size,pitch_set_size,pitch_set_mapping,individual_length):
        self.population_size = population_size
        self.pitch_set_size = pitch_set_size
        self.pitch_set_mapping = pitch_set_mapping
        self.individual_length = individual_length
        self.initial_population = self.random_initial_population()
        self.population = self.initial_population[:]

    def random_initial_population(self):
        group = []
        for i in range(self.population_size):
            group.append(random.choices(range(self.pitch_set_size),k=self.individual_length))
        return group
    
    def run(self,maxIter):
        for i in range(maxIter):
            self.iterate()
    
    def iterate(self):
        self.mutation()
        self.transposition()
        self.inversion()
        self.retrograde()
        self.crossover()
        self.selection()
    
    # 直接在self.population上操作
    def crossover(self):
        return
    def mutation(self):
        return
    def transposition(self):
        return
    def inversion(self):
        return
    def retrograde(self):
        return
    
    # 从经过操作的扩大的population选出大小为self.population_size的子集作为新的population
    def selection(self):
        return
    def fitness(self,individual):
        return