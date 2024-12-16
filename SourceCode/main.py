import argparse

def main():
    parser = argparse.ArgumentParser(description='A Genetic Algorithm for Music Composition.')
    parser.add_argument('selectionRatio', type=float, help='The selection strength during iteration.')
    parser.add_argument('mutationRatio', type=float, help='The mutation strength during iteration.')
    
    args = parser.parse_args()
    
    selectionRatio = args.selectionRatio
    mutationRatio = args.mutationRatio
    
    print('Argument passing finished.')

if __name__ == '__main__':
    main()