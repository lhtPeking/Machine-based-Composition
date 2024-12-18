import numpy as np
from matplotlib import pyplot as plt
import seaborn as sns
import pandas as pd
import math


class Heatmap:
    # 对进化过程中个体的fitness值进行可视化
    def __init__(self, populationRecord, fitnessFunction, individualLength, fileName):
        self.populationRecord = populationRecord
        self.fitnessFunction = fitnessFunction
        self.individualLength = individualLength
        self.fileName = fileName
        
    def draw(self):
        populationRecord = np.array(self.populationRecord)
        # dim(populationRecord) = (maxIter, populationSize, individualLength)
        fitnessMatrix = np.zeros((populationRecord.shape[0],populationRecord.shape[1]))
        # dim(fitnessMatrix) = (maxIter, populationSize)
        
        FitnessFunctions = FitnessFunctions(self.individualLength)
        
        for i in range(populationRecord.shape[0]):
            for j in range(populationRecord.shape[1]):
                if self.fitnessFunction == 'A':
                    fitnessMatrix[i][j] = FitnessFunctions.Fitness_A(populationRecord[i][j][:])
                elif self.fitnessFunction == 'B':
                    fitnessMatrix[i][j] = FitnessFunctions.Fitness_B(populationRecord[i][j][:])
                elif self.fitnessFunction == 'NormalStart':
                    fitnessMatrix[i][j] = FitnessFunctions.Fitness_NormalStart(populationRecord[i][j][:])
                elif self.fitnessFunction == 'AvoidBigInterval':
                    fitnessMatrix[i][j] = FitnessFunctions.Fitness_AvoidBigInterval(populationRecord[i][j][:])
                elif self.fitnessFunction == 'AvoidUnpreferredPitch':
                    fitnessMatrix[i][j] = FitnessFunctions.Fitness_AvoidUnpreferredPitch(populationRecord[i][j][:])
                elif self.fitnessFunction == 'AvoidBigDurationChange':
                    fitnessMatrix[i][j] = FitnessFunctions.Fitness_AvoidBigDurationChange(populationRecord[i][j][:])
                elif self.fitnessFunction == 'AvoidSyncopation':
                    fitnessMatrix[i][j] = FitnessFunctions.Fitness_AvoidSyncopation(populationRecord[i][j][:])
                elif self.fitnessFunction == 'AvoidContinueUpOrDown':
                    fitnessMatrix[i][j] = FitnessFunctions.Fitness_AvoidContinueUpOrDown(populationRecord[i][j][:])
                elif self.fitnessFunction == 'AvoidNoChange':
                    fitnessMatrix[i][j] = FitnessFunctions.Fitness_AvoidNoChange(populationRecord[i][j][:])
                elif self.fitnessFunction == 'AvoidBigFluctuation':
                    fitnessMatrix[i][j] = FitnessFunctions.Fitness_AvoidBigFluctuation(populationRecord[i][j][:])
                elif self.fitnessFunction == 'KeepInAnOctave':
                    fitnessMatrix[i][j] = FitnessFunctions.Fitness_KeepInAnOctave(populationRecord[i][j][:])
                elif self.fitnessFunction == 'LocalChange':
                    fitnessMatrix[i][j] = FitnessFunctions.Fitness_LocalChange(populationRecord[i][j][:])
                elif self.fitnessFunction == 'AvoidNoteRepetition':
                    fitnessMatrix[i][j] = FitnessFunctions.Fitness_AvoidNoteRepetition(populationRecord[i][j][:])
                elif self.fitnessFunction == 'GoodInterval':
                    fitnessMatrix[i][j] = FitnessFunctions.Fitness_GoodInterval(populationRecord[i][j][:])
                elif self.fitnessFunction == 'SimilarityBetweenBars':
                    fitnessMatrix[i][j] = FitnessFunctions.Fitness_SimilarityBetweenBars(populationRecord[i][j][:])
        
        # Plot:
        data = pd.DataFrame(fitnessMatrix)
        sns.heatmap(data)
        
        plt.xlabel("Iterations",size=20)
        plt.ylabel("Fitness",size=20,rotation=0)
        plt.title("Heatmap of Fitness of Individuals",size=20)
        
        plt.show()
        plt.savefig('../../Result/' + self.fileName + '-Heatmap' + '.png', bbox_inches='tight')
        
        
        
class DR:
    # UMAP降维分析:以12个不同的fitness函数值组成向量,观察不同fitness评价指标下完成迭代时的个体分布
    def __init__(self, Population, fileName):
        self.Population = Polulation
        self.fileName = fileName

    def analyze(self):
        Population = np.array(self.Population)
        # dim(Population) = (populationSize, individualLength)
        Vectors = np.zeros((Population.shape[0],12))
        for i in range(Population.shape[0]):
            Vectors[i][0] = FitnessFunctions.Fitness_A(Population[i][:])
            Vectors[i][1] = FitnessFunctions.Fitness_B(Population[i][:])
            Vectors[i][2] = FitnessFunctions.Fitness_NormalStart(Population[i][:])
            Vectors[i][3] = FitnessFunctions.Fitness_AvoidBigInterval(Population[i][:])
            Vectors[i][4] = FitnessFunctions.Fitness_AvoidUnpreferredPitch(Population[i][:])
            Vectors[i][5] = FitnessFunctions.Fitness_AvoidBigDurationChange(Population[i][:])
            Vectors[i][6] = FitnessFunctions.Fitness_AvoidSyncopation(Population[i][:])
            Vectors[i][7] = FitnessFunctions.Fitness_AvoidContinueUpOrDown(Population[i][:])
            Vectors[i][8] = FitnessFunctions.Fitness_AvoidNoChange(Population[i][:])
            Vectors[i][9] = FitnessFunctions.Fitness_AvoidBigFluctuation(Population[i][:])
            Vectors[i][10] = FitnessFunctions.Fitness_KeepInAnOctave(Population[i][:])
            Vectors[i][11] = FitnessFunctions.Fitness_LocalChange(Population[i][:])
        
        reducer = umap.UMAP(n_components=2, n_neighbors=10, random_state=42) # n_neighbors可以尝试调整
        embedding = reducer.fit_transform(Vectors)
        
        plt.figure(figsize=(8, 6))
        plt.scatter(embedding[:, 0], embedding[:, 1], s=30, c='blue', alpha=0.7)
        plt.title("UMAP of the Final Population",size=20)
        plt.xlabel("UMAP Dimension 1")
        plt.ylabel("UMAP Dimension 2")
        plt.grid(True)
        plt.show()
        
        plt.savefig('../../Result/' + self.fileName + '-UMAP' + '.png', bbox_inches='tight')
    
    
    
class FitnessFunctions:
    def __init__(self, individualLength):
        self.individualLength = individualLength
    
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