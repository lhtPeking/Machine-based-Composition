import argparse
from GAmusic import GAmusic

def main():
    parser = argparse.ArgumentParser(description='A Genetic Algorithm for Music Composition.')
    
    parser.add_argument('populationSize', type=int, help='The size of the population.')
    parser.add_argument('individualLength', type=int, help='The length of each individual.') # 8*4=32
    
    parser.add_argument('Flag-M', type=int, help='Do mutation or not.(1 for yes, 0 for no)')
    parser.add_argument('Flag-T', type=int, help='Do transposition or not.(1 for yes, 0 for no)')
    parser.add_argument('Flag-I', type=int, help='Do inversion or not.(1 for yes, 0 for no)')
    parser.add_argument('Flag-R', type=int, help='Do retrograde or not.(1 for yes, 0 for no)')
    parser.add_argument('Flag-C', type=int, help='Do crossover or not.(1 for yes, 0 for no)')
    
    parser.add_argument('selectionRatio', type=float, help='The selection strength during iteration.')
    parser.add_argument('mutationRatio', type=float, help='The mutation strength during iteration.')
    parser.add_argument('maxIter', type=int, help='The maximum number of iterations.')
    
    parser.add_argument('fitness_Iter', type=float, help='The fitness threshold for selection process.')
    parser.add_argument('fitness_Final', type=float, help='The fitness threshold for stop.')
    
    parser.add_argument('fitnessFunction', type=str, help='The fitness function to be used.(A for A, B for B, etc.)')
    
    args = parser.parse_args()
    
    populationSize = args.populationSize
    individualLength = args.individualLength
    
    Flag_M = args.Flag_M
    Flag_T = args.Flag_T
    Flag_I = args.Flag_I
    Flag_R = args.Flag_R
    Flag_C = args.Flag_C
    
    selectionRatio = args.selectionRatio
    mutationRatio = args.mutationRatio
    maxIter = args.maxIter
    
    fitness_Iter = args.fitness_Iter
    fitness_Final = args.fitness_Final
    
    fitnessFunction = args.fitnessFunction
    
    print('Argument passing finished.')
    
    GA = GAmusic(populationSize,individualLength,Flag_M,Flag_T,Flag_I,Flag_R,
                 Flag_C,selectionRatio,mutationRatio,maxIter,fitness_Iter,fitness_Final,fitnessFunction)
    
    GA.run(maxIter)
    
if __name__ == '__main__':
    main()