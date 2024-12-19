import numpy as np
import umap
from sklearn.cluster import KMeans
from matplotlib import pyplot as plt
import seaborn as sns
import pandas as pd
import math


class Heatmap:
    # 对进化过程中个体的fitness值进行可视化
    def __init__(self, populationRecord, fitnessWeights, individualLength, fileName):
        self.populationRecord = populationRecord
        self.fitnessWeights = fitnessWeights
        self.individualLength = individualLength
        self.fileName = fileName
        
    def draw(self):
        populationRecord = np.array(self.populationRecord)
        # dim(populationRecord) = (maxIter, populationSize, individualLength)
        fitnessMatrix = np.zeros((populationRecord.shape[0],populationRecord.shape[1]))
        # dim(fitnessMatrix) = (maxIter, populationSize)
        
        FitnessFunction = FitnessFunctions(self.individualLength, self.fitnessWeights)
        
        print(populationRecord.shape)
        
        for i in range(populationRecord.shape[0]):
            for j in range(populationRecord.shape[1]):
                fitnessMatrix[i][j] = FitnessFunction.Fitness(populationRecord[i][j][:].tolist())
        
        # Plot:
        data = pd.DataFrame(fitnessMatrix)
        sns.heatmap(data)
        
        plt.xlabel("Individuals",size=20)
        plt.ylabel("Iterations",size=20,rotation=90)
        plt.title("Heatmap of Fitness of Individuals",size=20)
        
        plt.show()
        # plt.savefig('../Results/' + self.fileName + '-Heatmap', bbox_inches='tight')
        
        
        
class DR:
    # UMAP降维分析:以12个不同的fitness函数值组成向量,观察不同fitness评价指标下完成迭代时的个体分布
    def __init__(self, Population, fitnessWeights, individualLength, fileName):
        self.Population = Population
        self.fitnessWeights = fitnessWeights
        self.individualLength = individualLength
        self.fileName = fileName

    def analyze(self):
        Population = np.array(self.Population)
        # dim(Population) = (populationSize, individualLength)
        Vectors = np.zeros((Population.shape[0],13))
        
        FitnessFunction = FitnessFunctions(self.individualLength, self.fitnessWeights)
        
        for i in range(Population.shape[0]):
            Vectors[i][0] = FitnessFunction.Fitness_NormalStart(Population[i][:].tolist())
            Vectors[i][1] = FitnessFunction.Fitness_AvoidUnpreferredPitch(Population[i][:].tolist())
            Vectors[i][2] = FitnessFunction.Fitness_AvoidSyncopation(Population[i][:].tolist())
            Vectors[i][3] = FitnessFunction.Fitness_AvoidBigInterval(Population[i][:].tolist())
            Vectors[i][4] = FitnessFunction.Fitness_GoodInterval(Population[i][:].tolist())
            Vectors[i][5] = FitnessFunction.Fitness_AvoidBigFluctuation(Population[i][:].tolist())
            Vectors[i][6] = FitnessFunction.Fitness_AvoidContinueUpOrDown(Population[i][:].tolist())
            Vectors[i][7] = FitnessFunction.Fitness_AvoidNoteRepetition(Population[i][:].tolist())
            Vectors[i][8] = FitnessFunction.Fitness_AvoidNoChange(Population[i][:].tolist())
            Vectors[i][9] = FitnessFunction.Fitness_LocalChange(Population[i][:].tolist())
            Vectors[i][10] = FitnessFunction.Fitness_AvoidBigDurationChange(Population[i][:].tolist())
            Vectors[i][11] = FitnessFunction.Fitness_KeepInAnOctave(Population[i][:].tolist())
            Vectors[i][12] = FitnessFunction.Fitness_SimilarityBetweenBars(Population[i][:].tolist())
        
        reducer = umap.UMAP(n_components=2, n_neighbors=10, random_state=42) # n_neighbors可以尝试调整
        embedding = reducer.fit_transform(Vectors)
        
        n_clusters = 5
        kmeans = KMeans(n_clusters=n_clusters, random_state=42)
        labels = kmeans.fit_predict(embedding)
        
        plt.figure(figsize=(8, 6))
        scatter = plt.scatter(embedding[:, 0], embedding[:, 1], s=30, c=labels, cmap='viridis', alpha=0.7)
        plt.title("UMAP of the Final Musical Population with K-Means Clustering(K=5)", size=12)
        plt.xlabel("UMAP Dimension 1")
        plt.ylabel("UMAP Dimension 2")
        plt.grid(True)
        
        plt.colorbar(scatter, ticks=range(n_clusters), label='Cluster')
        
        plt.show()
        
        # plt.savefig('../../Result/' + self.fileName + '-UMAP' + '.png', bbox_inches='tight')
    
    
    
class FitnessFunctions:
    def __init__(self, individualLength, fitnessWeights):
        self.individualLength = individualLength
        self.fitnessWeights = fitnessWeights
    
    def Fitness(self,individual): # 加权
        return self.Fitness_NormalStart(individual) * self.fitnessWeights[0]\
                +self.Fitness_AvoidUnpreferredPitch(individual) * self.fitnessWeights[1]\
                +self.Fitness_AvoidSyncopation(individual) * self.fitnessWeights[2]\
                +self.Fitness_AvoidBigInterval(individual) * self.fitnessWeights[3]\
                +self.Fitness_GoodInterval(individual) * self.fitnessWeights[4]\
                +self.Fitness_AvoidBigFluctuation(individual) * self.fitnessWeights[5]\
                +self.Fitness_AvoidContinueUpOrDown(individual) * self.fitnessWeights[6]\
                +self.Fitness_AvoidNoteRepetition(individual) * self.fitnessWeights[7]\
                +self.Fitness_AvoidNoChange(individual) * self.fitnessWeights[8]\
                +self.Fitness_LocalChange(individual) * self.fitnessWeights[9]\
                +self.Fitness_AvoidBigDurationChange(individual) * self.fitnessWeights[10]\
                +self.Fitness_KeepInAnOctave(individual) * self.fitnessWeights[11]\
                +self.Fitness_SimilarityBetweenBars(individual) * self.fitnessWeights[12]
    
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
            bar = individual[i:i+8]
            while 0 in bar:
                bar.remove(0)
            while 28 in bar:
                bar.remove(28)
            if len(bar)>0:
                total_change = abs(bar[-1] - bar[0])
            else:
                total_change = 0
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
        return 1 - max(repetition)/n
    
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

        mean_var = np.var([mean1,mean2,mean3,mean4])
        var_var = np.var([var1,var2,var3,var4])

        return (np.exp(-mean_var) + np.exp(-var_var))/2