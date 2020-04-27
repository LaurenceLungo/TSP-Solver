from time import time
from random import seed, randint
from argparse import ArgumentParser
from pandas import read_csv
from numpy import linalg, array
from math import sin, cos
from visualizer.visualizer import Visualizer

from algo.greedy_rotate import greedy_rotate
from algo.cross_path_dismantling import cross_path_dismantling
from algo.two_opt import two_opt
from algo.simulated_annealing import sim_annealing

ini_time = time()  # start the timer here

# ===== List of datasets =====
# wi29 27603 Western Sahara
# dj38 6656 Djibouti
# berlin52 7544 Berlin
# ch150 6528 Churritz
# qa194 9352 Qatar
# pr264
# lin318 Lin/Kernighan
# pr439
# rat575
# rat783
# uy734 79114 Uruguay
# zi929 95345 Zimbabwe
# sw24978 855597 Sweden
# ===========================

# argument parser -----------------------------------------------------------------
parser = ArgumentParser(description='Solving the TSP.')
parser.add_argument('input', metavar='i', nargs='?',
                    help='the path to input coordinates file')
parser.add_argument('output', metavar='o', nargs='?', default='output-tour.txt',
                    help='the path to output tour file')
parser.add_argument('--time', metavar='-t', type=int, nargs='?', default=180,
                    help='the maximum number of seconds that the program should run')
parser.add_argument('--algo', metavar='-a', type=int, nargs='?', default=0,
                    help='manually select algorithm: 1 - sa; 2 - dcp - 2opt; 3 - 2-opt')
parser.add_argument('--loop', metavar='-l', type=int, nargs='?', default=1,
                    help='loop the program for a given time')
parser.add_argument('-v', action='store_true',
                    help='visualize the result at the end')
args = parser.parse_args()
args_value = vars(args)


# end of argument parser ----------------------------------------------------------

# helper functions ----------------------------------------------------------------
def gen_node(num):  # random dataset generator
    seed()
    a = []
    for _ in range(num):
        a.append([randint(0, num * 2), randint(0, num * 2)])
    return array(a)


def rotate(origin, point, angle):  # rotates a point about an origin by an angle
    ox, oy = origin
    px = point[0]
    py = point[1]

    qx = ox + cos(angle) * (px - ox) - sin(angle) * (py - oy)
    qy = oy + sin(angle) * (px - ox) + cos(angle) * (py - oy)
    return qx, qy


# end of helper functions ---------------------------------------------------------

# data & arguments parsing --------------------------------------------------------
node = read_csv(args_value['input'], sep=" ", header=None, names=['idx', 'x', 'y']).set_index('idx')[['y', 'x']].values

euclidean_map = [[0 for x in range(len(node))] for y in range(len(node))]
for i in range(len(node)):
    for j in range(len(node)):
        euclidean_map[i][j] = int(round(linalg.norm(node[i] - node[j])))

for n in node:
    n[0], n[1] = rotate([0, 0], [n[0], n[1]], 1)
# end of data & arguments parsing -------------------------------------------------

# main <><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><>><><><><><><><><><><><><><>
for _ in range(args_value["loop"]):
    deadline = time() + args_value["time"]
    final_length = None
    final_route = None

    g_length, g_route = greedy_rotate(euclidean_map)
    print("g_length:", g_length, "time cost:", time() - ini_time)

    if args_value["algo"] == 1 or (args_value["algo"] == 0 and len(node) <= 50):
        best_sa_length = None
        best_sa_route = None
        for _ in range(int(args_value["time"] / 30 - 1)):
            # worst case 30 sec per run
            sa_length, sa_route = sim_annealing(euclidean_map, g_length, g_route, 2000000)
            if best_sa_length is None or sa_length < best_sa_length:
                best_sa_length = sa_length
                best_sa_route = sa_route
        final_length = best_sa_length
        final_route = best_sa_route
    elif args_value["algo"] == 2 or (args_value["algo"] == 0 and len(node) <= 500):
        c_length, c_route = cross_path_dismantling(euclidean_map, node, g_route)
        print("c_length:", c_length, "time cost:", time() - ini_time)
        t_length, t_route = two_opt(euclidean_map, c_length, c_route, deadline)
        print("t_length:", t_length, "time cost:", time() - ini_time)
        final_length = t_length
        final_route = t_route
    else:
        t_length, t_route = two_opt(euclidean_map, g_length, g_route, deadline)
        print("t_length:", t_length, "time cost:", time() - ini_time)
        final_length = t_length
        final_route = t_route

    output_string = "tour cost: " + str(final_length) + "\n" + "tour: " + str(final_route) + "\n"
    mode = 'w'
    if args_value["loop"] > 1:
        mode = 'a+'
    out = open(args_value['output'], mode)
    out.write(output_string)
    out.close()
    print(output_string)
    print("finish")
    print("time cost:", time() - ini_time)

    if _ == args_value["loop"] - 1 and args.v:
        Visualizer(node, final_length, final_route)
# end of main <><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><>
