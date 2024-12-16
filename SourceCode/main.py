import argparse
from GAmusic import GAmusic

def main():
    parser = argparse.ArgumentParser(description='A Genetic Algorithm for Music Composition.')
    parser.add_argument('populationSize', type=int, help='The size of the population.')
    parser.add_argument('pitchSetSize', type=int, help='The size of the pitch set.')
    
    parser.add_argument('Flag-M', type=int, help='Do mutation or not.(1 for yes, 0 for no)')
    parser.add_argument('Flag-T', type=int, help='Do transposition or not.(1 for yes, 0 for no)')
    parser.add_argument('Flag-I', type=int, help='Do inversion or not.(1 for yes, 0 for no)')
    parser.add_argument('Flag-R', type=int, help='Do retrograde or not.(1 for yes, 0 for no)')
    parser.add_argument('Flag-C', type=int, help='Do crossover or not.(1 for yes, 0 for no)')
    
    parser.add_argument('selectionRatio', type=float, help='The selection strength during iteration.')
    parser.add_argument('mutationRatio', type=float, help='The mutation strength during iteration.')
    parser.add_argument('maxIter', type=int, help='The maximum number of iterations.')
    
    args = parser.parse_args()
    
    populationSize = args.populationSize
    pitchSetSize = args.pitchSetSize
    
    Flag_M = args.Flag_M
    Flag_T = args.Flag_T
    Flag_I = args.Flag_I
    Flag_R = args.Flag_R
    Flag_C = args.Flag_C
    
    selectionRatio = args.selectionRatio
    mutationRatio = args.mutationRatio
    maxIter = args.maxIter
    
    print('Argument passing finished.')
    
    GA = GAmusic(populationSize,pitchSetSize,Flag_M,Flag_T,Flag_I,Flag_R,
                 Flag_C,selectionRatio,mutationRatio,args.maxIter)
    
    GA.run(maxIter)
    
if __name__ == '__main__':
    main()