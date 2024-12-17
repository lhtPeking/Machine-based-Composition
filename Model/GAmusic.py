import random

class GAmusic:
    def __init__(self,populationSize,individualLength,Flag_M,Flag_T,Flag_I,Flag_R,
                 Flag_C,mutationRatio,crossoverRatio,maxIter,fitness_Iter,fitness_Final,fitnessFunction):
        self.populationSize = populationSize
        self.individualLength = individualLength
        
        self.Flag_M = Flag_M
        self.Flag_T = Flag_T
        self.Flag_I = Flag_I
        self.Flag_R = Flag_R
        self.Flag_C = Flag_C

        self.mutationRatio = mutationRatio
        self.crossoverRatio = crossoverRatio
        self.maxIter = maxIter
        
        self.fitness_Iter = fitness_Iter
        self.fitness_Final = fitness_Final
        
        self.initialPopulation = self.random_initial_population()
        self.population = self.initial_population[:]
        
        self.fitnessFunction = fitnessFunction

    def random_initial_population(self):
        group = []
        for i in range(self.population_size):
            # F3到G5, 0作为休止符, 1-27作为音符, 28为延音符 
            group.append(random.choices(range(29),k=self.individualLength))
        return group
    
    def run(self,maxIter):
        for i in range(maxIter):
            self.iterate()
            if self.Fitness_A(self.population[0]) > self.fitness_Final: # fitness达到阈值, 提前终止
                break
    
    def iterate(self):
        # Duplication: 高于fitness_Iter的个体复制到下一代
        for n in range(self.populationSize):
            if self.Fitness_A(self.population[n]) > self.fitness_Iter:
                self.population.append(self.population[n])
        
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
    def mutation(self):
        for i in range(self.populationSize):
            if random.random() < self.mutationRatio: # 一次只突变一个音符
                self.population[i][random.randint(0,self.individualLength-1)] = random.randint(0,28)
        return
    
    def crossover(self): 
        # 以长度为8的段落为单位进行交叉(原本每个个体有32个音符)
        for i in range(self.populationSize):
            individual = self.population[i]
            segments = [individual[j:j+8] for j in range(0, self.individualLength, 8)]
            for j in range(i+1, self.populationSize): 
                if random.random() < self.crossoverRatio:
                    individual2 = self.population[j]
                    segments2 = [individual2[k:k+8] for k in range(0, self.individualLength, 8)]
                    for m in range(4): # 所有段落以50%的概率交换
                        if random.random() < 0.5:
                            segments[m],segments2[m] = segments2[m],segments[m]
                    # flatten:
                    self.population[i] = [note for segment in segments for note in segment]
                    self.population[j] = [note for segment in segments2 for note in segment]
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
