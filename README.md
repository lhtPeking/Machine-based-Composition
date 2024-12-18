  

# Genetic-Algorithm-Based Stochasitic Composition

  

## Introduction 👋

**Genetic Algorithm (GA)** is applied in machine composition by simulating the process of **natural selection and biological evolution** to automatically generate works that conform to specific musical rules. It encodes music segments as individuals, evaluates their quality using a **fitness function**, and performs evolution through selection, crossover, and mutation operations. After several generations of iteration, the algorithm generates harmonious and creative melodies, harmonies, and rhythms that meet various style and emotional requirements. The global search capability and flexibility of genetic algorithms make them powerful tools in music composition, widely used in melody generation, harmony creation, and rhythm design.

  

## Usage 🖥️
Clone the repository:
``` bash
git clone git@github.com:lhtPeking/Machine-based-Composition.git
```
Switch to the directory where our model is located:
``` bash
cd Model
```
The format for entering commands:
``` bash
python main.py [populationSize] [individualLength] [Flag_M] [Flag_T] [Flag_I] [Flag_R] [Flag_C] [mutationRatio] [crossoverRatio] [maxIter] [fitness_Iter] [fitness_Final] [fitnessFunction] [fileName]
```

Example:```(base) haotianli@bogon Model % python main.py 20 28 1 1 1 1 1 0.2 0.2 30 0.8 0.9 A output1```

  

## Methods ✍️

### 1 Generation of Initial Population

We use a random simulation approach to generate 27 pitch sequences (from $F_3$ to $G_5$ in the musical scale). We use digital encoding (0 as a rest, 1-27 as notes, and 28 as a sustain note). The specific generation function is located in the ```random_initial_population(self)``` function in ```GAmusic.py```.

### 2 Transformations in Each Iteration

We define five transformation methods: ```mutation()```, ```transposition()```, ```inversion()```, ```retrograde()```, and ```crossover()``` (see the corresponding functions in ```GAmusic.py```). A flag parameter is used to decide whether to apply these transformations during the iteration process.

### 3 Natural Selection and Fitness Function

We calculate the fitness of each individual according to the defined fitness function and select individuals from the population using a **probability-weighted** method based on their fitness, to avoid getting stuck in local minima. The iteration stops when either the predefined maximum number of iterations is reached or when an individual’s fitness reaches a threshold.

### 4 From Digital Encoding to Musical Notation

### 5 Visualization

We use **Heatmaps** to represent the fitness values of the population throughout the iteration process, providing an intuitive analysis of how different **hyperparameter selections** affect the iteration. Additionally, we apply **UMAP** dimensionality reduction to represent each individual as a vector defined by 12 fitness function values and perform clustering analysis.

  
  
  

## Results 📋

  

## References 📜
  

