import time
import argparse
import random
import pandas as pd
from numpy import linalg, array
from statistics import mean, stdev
from algo.greedy_rotate import greedy_rotate
from algo.cross_path import cross_path
from algo.two_opt import two_opt
from algo.simulated_annealing import sim_annealing

ini_time = time.time()

# Fake Location: ff4
# Western Sahara: wi29 27603
# Djibouti: dj38 6656
# Berlin berlin52 7544
# Churritz: ch150 6528
# Qatar: qa194 9352
# Uruguay: uy734 79114
# Zimbabwe: zi929 95345
# Luxembourg: lu980 11340
# Sweden sw24978 855597
# argument parser -----------------------------------------------------------------
parser = argparse.ArgumentParser(description='Solving the TSP.')
parser.add_argument('input', metavar='i', nargs='?', default='uy734.txt',
                    help='the path to input coordinates file')
parser.add_argument('output', metavar='o', nargs='?', default='output-tour.txt',
                    help='the path to output tour file')
parser.add_argument('time', metavar='t', type=int, nargs='?', default=180,
                    help='the maximum running time')
args = vars(parser.parse_args())


# end of argument parser ----------------------------------------------------------

# helper functions ----------------------------------------------------------------
def print_map(mapp):
    for ii in mapp:
        print(ii)


def gen_node(num):
    random.seed()
    a = []
    for i in range(num):
        a.append([random.randint(0, num * 2), random.randint(0, num * 2)])
    return array(a)


# end of helper functions ---------------------------------------------------------

# data & arguments parsing --------------------------------------------------------
deadline = time.time() + args['time']

node = pd.read_csv(args['input'], sep=" ", header=None, names=['idx', 'x', 'y']).set_index('idx')[['y', 'x']].values
# node = gen_node(200)
euclideanMap = [[0 for x in range(len(node))] for y in range(len(node))]
for i in range(len(node)):
    for j in range(len(node)):
        euclideanMap[i][j] = linalg.norm(node[i] - node[j])

# end of data & arguments parsing -------------------------------------------------

# main <><><><><><><><>><><><><><><><><><><><><><><><><><><><><><><><>><><><><><><><><><><><>><><><><><><><><><><><><><>
final_length = None
final_route = None

g_length, g_route = greedy_rotate(euclideanMap, node)
print("Greedy: cost " + str(g_length) + " " + str(g_route))
print("time: ", time.time()-ini_time)

if len(node) <= 52:
    best_sa_length = None
    best_sa_route = None
    for _ in range(4):
        sa_length, sa_route = sim_annealing(euclideanMap, node, g_length, g_route, 2000000)
        print(sa_length)
        if best_sa_length is None or sa_length < best_sa_length:
            best_sa_length = sa_length
            best_sa_route = sa_route
    final_length = best_sa_length
    final_route = best_sa_route
else:
    # c_length, c_route = cross_path(euclideanMap, node, g_length, g_route)
    # print("Cross: cost " + str(c_length) + " " + str(c_route))
    # print("time: ", time.time()-ini_time)
    # t_length, t_route = two_opt(euclideanMap, node, c_length, c_route, ini_time + args["time"] - time.time())
    # final_length = t_length
    # final_route = t_route

    # t_length, t_route = two_opt(euclideanMap, node, g_length, g_route, ini_time + args["time"] - time.time())
    # print("two-opt: cost " + str(t_length) + " " + str(t_route))
    # print("time: ", time.time()-ini_time)
    # final_length = t_length
    # final_route = t_route

    s_length, s_route = sim_annealing(euclideanMap, node, g_length, g_route, 2000000)
    print("sim_ann: cost " + str(s_length) + " " + str(s_route))
    print("time: ", time.time()-ini_time)
    final_length = s_length
    final_route = s_route

print("running time: ", time.time() - ini_time)
print("optimal tour: ", final_route)
print("optimal length: ", final_length)
# end of main <><><><><><><><>><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><>><><><><><><><><><><>
