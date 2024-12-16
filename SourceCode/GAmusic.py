import random

class GAmusic:
    def __init__(self,populationSize,individualLength,Flag_M,Flag_T,Flag_I,Flag_R,
                 Flag_C,selectionRatio,mutationRatio,maxIter,fitness_Iter,fitness_Final,fitnessFunction):
        self.populationSize = populationSize
        self.individualLength = individualLength
        
        self.Flag_M = Flag_M
        self.Flag_T = Flag_T
        self.Flag_I = Flag_I
        self.Flag_R = Flag_R
        self.Flag_C = Flag_C
        
        self.selectionRatio = selectionRatio
        self.mutationRatio = mutationRatio
        self.maxIter = maxIter
        
        self.fitness_Iter = fitness_Iter
        self.fitness_Final = fitness_Final
        
        self.initialPopulation = self.random_initial_population()
        self.population = self.initial_population[:]
        
        self.fitnessFunction = fitnessFunction

    def random_initial_population(self):
        group = []
        for i in range(self.population_size):
            # 跨两个八度, 0作为休止符, 1-16作为音符, 17为延音符 
            group.append(random.choices(range(18),k=self.individualLength))
        return group
    
    def run(self,maxIter):
        for i in range(maxIter):
            self.iterate()
    
    def iterate(self):
        if Flag_M:
            self.mutation()
        if Flag_C:
            self.crossover()
        if Flag_T:
            self.transposition()
        if Flag_I:
            self.inversion()
        if Flag_R:
            self.retrograde()
            
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
    
    # 从经过操作的扩大的population选出大小为self.populationSize的子集作为新的population
    def selection(self):
        if self.fitnessFunction == 'A':
            self.population.sort(key=lambda individual: self.Fitness_A(individual), reverse=True)
            self.population = self.population[:self.populationSize]
        else if self.fitnessFunction == 'B':
            self.population.sort(key=lambda individual: self.Fitness_B(individual), reverse=True)
            self.population = self.population[:self.populationSize]
        return
    
    def Fitness_A(self,individual):
        return
    def Fitness_B(self,individual):
        return