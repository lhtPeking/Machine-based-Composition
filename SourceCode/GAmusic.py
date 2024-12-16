import random

class GAmusic:
    def __init__(self,populationSize,pitchSetSize,Flag_M,Flag_T,Flag_I,Flag_R,
                 Flag_C,selectionRatio,mutationRatio,maxIter):
        self.populationSize = populationSize
        self.pitch_set_size = pitch_set_size
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
        if Flag_M:
            self.mutation()
        if Flag_T:
            self.transposition()
        if Flag_I:
            self.inversion()
        if Flag_R:
            self.retrograde()
        if Flag_C:
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
    def Fitness_A(self,individual):
        return
    def Fitness_B(self,individual):
        return