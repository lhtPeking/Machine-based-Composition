import random
import math
import numpy as np
from utils import Mapping, Heatmap, DR

class GAmusic:
    def __init__(self,populationSize,individualLength,Flag_M,Flag_T,Flag_I,Flag_R,Flag_C,
                 mutationRatio,crossoverRatio,maxIter,fitness_Iter,fitness_Final,fitnessFunction,fileName):
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
        self.population = self.initialPopulation[:]
        
        self.populationRecord = {}
        self.populationRecord[0] = [self.population[:]]
        
        self.fitnessFunction = fitnessFunction        
        
        self.fileName = fileName

    def random_initial_population(self):
        group = []
        for i in range(self.populationSize):
            # F3到G5, 0作为休止符, 1-27作为音符, 28为延音符 
            group.append(random.choices(range(29),k=self.individualLength))
        return group
    
    def run(self,maxIter):
        iterationCount = 0
        for i in range(maxIter):
            self.iterate()
            iterationCount += 1
            if self.Fitness_A(self.population[0]) > self.fitness_Final: # fitness达到阈值, 提前终止
                break
        
        Mapping = Mapping(self, self.population[0], self.fileName)
        Mapping.generate()
        
        # 这里只针对选中的fitnessFunction进行Heatmap可视化, 但是降维的时候要考虑所有的fitnessFunction
        Heatmap = Heatmap(self, self.populationRecord, self.fitnessFunction, self.individualLength, self.fileName) 
        Heatmap.draw()
        
        DR = DR(self, self.population[:], self.fileName)
        DR.analyze()
        
        print('Iteration finished, the final fitness is: ', self.Fitness_A(self.population[0]))
        print('The final iteration count is: ', iterationCount)
    
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
        self.populationRecord.append(self.population[:])
    
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
        elif self.fitnessFunction == 'B':
            self.population.sort(key=lambda individual: self.Fitness_B(individual), reverse=True)
            self.population = self.population[:self.populationSize]
        return
    
    ############################## Fitness Functions ##############################
    def Fitness_A(self,individual): # 加权
        return self.Fitness_AvoidBigDurationChange(individual)\
                +self.Fitness_AvoidBigFluctuation(individual)\
                +self.Fitness_AvoidBigInterval(individual)\
                +self.Fitness_AvoidContinueUpOrDown(individual)\
                +self.Fitness_AvoidNoChange(individual)\
                +self.Fitness_AvoidNoteRepetition(individual)\
                +self.Fitness_AvoidSyncopation(individual)\
                +self.Fitness_AvoidUnpreferredPitch(individual)\
                +self.Fitness_GoodInterval(individual)\
                +self.Fitness_KeepInAnOctave(individual)\
                +self.Fitness_LocalChange(individual)\
                +self.Fitness_SimilarityBetweenBars(individual)\
                +self.Fitness_NormalStart(individual)
    
    def Fitness_B(self,individual):
        return self.Fitness_AvoidBigDurationChange(individual)\
                +self.Fitness_AvoidBigFluctuation(individual)\
                +self.Fitness_AvoidBigInterval(individual)\
                +self.Fitness_AvoidContinueUpOrDown(individual)\
                +self.Fitness_AvoidNoChange(individual)\
                +self.Fitness_AvoidNoteRepetition(individual)\
                +self.Fitness_AvoidSyncopation(individual)\
                +self.Fitness_AvoidUnpreferredPitch(individual)\
                +self.Fitness_GoodInterval(individual)\
                +self.Fitness_KeepInAnOctave(individual)\
                +self.Fitness_LocalChange(individual)\
                +self.Fitness_SimilarityBetweenBars(individual)\
                +self.Fitness_NormalStart(individual)
    
    def Fitness_NormalStart(self,individual):
        if individual[0] in [0,28]:
            return 0
        else:
            return 1

    def Fitness_AvoidBigInterval(self,individual):
        n = self.individualLength
        score = 0
        intervals = []
        last_one = 100
        for i in range(n):
            if individual[i] not in [0,28,last_one]:
                intervals.append(abs(individual[i]-last_one))
                last_one = individual[i]
        for interval in intervals:
            if interval <= 12:
                score +=1
        return score/len(intervals)
    
    def Fitness_AvoidUnpreferredPitch(self,individual):
        n = self.individualLength
        preferred_pitches = []
        score = 0
        for i in range(n):
            if individual[i] in preferred_pitches:
                score += 1
            else:
                score -= 1
        return score/n
    
    def Fitness_AvoidBigDurationChange(self,individual):
        n = self.individualLength
        score = 0
        total = 0
        durations = []
        for i in range(n):
            if individual[i] != 28:
                durations.append(1)
            elif durations:
                durations[-1] += 1
        for j in range(len(durations)-1):
            change = abs(durations[j+1] - durations[j])
            total += 1
            if change < 4:
                score += 1
        return score/total
    
    def Fitness_AvoidSyncopation(self,individual):
        score = 0
        for i in [4,8,12,16,20,24,28]:
            if individual[i] in [0,28]:
                score -= 1
            else:
                score += 1
        return score/7
    
    def Fitness_AvoidContinueUpOrDown(self,individual):
        n = self.individualLength
        score = 0
        for i in [0,8,16,24]:
            a=i
            b=i+7
            while individual[a] in [0,28]:
                a += 1
            if a >= b:
                total_change = 0
            else:
                while individual[b] in [0,28]:
                    b -= 1
                total_change = abs(individual[i+7] - individual[i])
            if total_change < 8:
                score += 1
        return score/4
    
    def Fitness_AvoidNoChange(self,individual):
        n = self.individualLength
        unchanged = [1]
        pitches_and_durations = []
        for i in range(n):
            if individual[i] != 28:
                pitches_and_durations.append([individual[i],1])
            elif pitches_and_durations:
                pitches_and_durations[-1][1] += 1
        for j in range(len(pitches_and_durations)-1):
            if pitches_and_durations[j] == pitches_and_durations[j+1]:
                unchanged[-1] += 1
            else:
                unchanged.append(1)
        if max(unchanged) < 4:
            return 1
        else:
            return 0
        
    def Fitness_AvoidBigFluctuation(self,individual):
        n = self.individualLength
        intervals = []
        last_one = 100
        for i in range(n):
            if individual[i] not in [0,28,last_one]:
                intervals.append(individual[i]-last_one)
                last_one = individual[i]
        average_interval = abs(sum(intervals))/len(intervals)
        fluctuation = 0
        for interval in intervals:
            fluctuation += (abs(interval)-average_interval)**2
        fluctuation = math.sqrt(fluctuation/len(intervals))
        if fluctuation < 1:
            return 1
        else:
            return 0
    
    def Fitness_KeepInAnOctave(self,individual):
        n = self.individualLength
        octaves = [0 for i in range(15)]
        total = 0
        for i in range(n):
            if individual[i] >= 1 and individual[i] <= 27:
                total += 1
                for j in range(max(1,individual[i]-12),min(15,individual[i])+1):
                    octaves[j-1] += 1
        return max(octaves)/total
    
    def Fitness_LocalChange(self,individual):
        score = 0
        individual_copy = individual[:]
        while 0 in individual_copy:
            individual_copy.remove(0)
        while 28 in individual_copy:
            individual_copy.remove(28)
        for i in range(len(individual_copy)-2):
            if individual[i] > individual[i+1] and individual[i+1] > individual[i+2]:
                score += 1
            elif individual[i] < individual[i+1] and individual[i+1] < individual[i+2]:
                score += 1
        return score/(len(individual_copy)-2)
    
    def Fitness_AvoidNoteRepetition(self,individual):
        n = self.individualLength
        repetition = []
        last_one = 100
        for i in range(n):
            if individual[i] == 28 and repetition:
                repetition[-1] += 1
            elif individual[i] == last_one:
                repetition[-1] += 1
            elif individual[i] != 0:
                last_one = individual[i]
                repetition.append(1)
        return -max(repetition)/n
    
    def Fitness_GoodInterval(self,individual):
        n = self.individualLength
        intervals = []
        last_one = 100
        for i in range(n):
            if individual[i] not in [0,28,last_one]:
                intervals.append(abs(individual[i]-last_one))
                last_one = individual[i]
        score = 0
        for interval in intervals:
            if interval in [12,5,7]:
                score += 1
            elif interval in [3,4,8,9]:
                score += 0.5
        return score/len(intervals)

    def Fitness_SimilarityBetweenBars(self,individual):
        bar1 = individual[0:8]
        bar2 = individual[8:16]
        bar3 = individual[16:24]
        bar4 = individual[24:32]

        intervals1 = []
        last_one = 100
        for i in range(self.individualLength//4):
            if bar1[i] not in [0,28,last_one]:
                intervals1.append(abs(bar1[i]-last_one))
                last_one = bar1[i]
        mean1 = np.mean(intervals1)
        var1 = np.var(intervals1)

        intervals2 = []
        last_one = 100
        for i in range(self.individualLength//4):
            if bar2[i] not in [0,28,last_one]:
                intervals2.append(abs(bar2[i]-last_one))
                last_one = bar2[i]
        mean2 = np.mean(intervals2)
        var2 = np.var(intervals2)

        intervals3 = []
        last_one = 100
        for i in range(self.individualLength//4):
            if bar3[i] not in [0,28,last_one]:
                intervals3.append(abs(bar3[i]-last_one))
                last_one = bar3[i]
        mean3 = np.mean(intervals3)
        var3 = np.var(intervals3)

        intervals4 = []
        last_one = 100
        for i in range(self.individualLength//4):
            if bar4[i] not in [0,28,last_one]:
                intervals4.append(abs(bar4[i]-last_one))
                last_one = bar4[i]
        mean4 = np.mean(intervals4)
        var4 = np.var(intervals4)

        mean_std = np.std([mean1,mean2,mean3,mean4])
        var_std = np.std([var1,var2,var3,var4])
        return - mean_std - var_std
