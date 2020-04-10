import argparse
from numpy import linalg
import pandas as pd

parser = argparse.ArgumentParser(description='Solving the TSP.')
parser.add_argument('input', metavar='i', nargs='?', default='mat-test.txt',
                    help='the path to input coordinates file')
parser.add_argument('output', metavar='o', nargs='?', default='output-tour.txt',
                    help='the path to output tour file')
parser.add_argument('time', metavar='t', type=int, nargs='?', default=180,
                    help='the maximum running time')
args = vars(parser.parse_args())


def print_map(mapp):
    for ii in mapp:
        print(ii)


node = pd.read_csv(args['input'], sep=" ", header=None, names=['idx', 'x', 'y']).set_index('idx').values
euclideanMap = [[0 for x in range(len(node))] for y in range(len(node))]
for i in range(len(node)):
    for j in range(len(node)):
        euclideanMap[i][j] = linalg.norm(node[i] - node[j])

