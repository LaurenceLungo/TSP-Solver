from time import time
from random import seed, randint
from argparse import ArgumentParser
from pandas import read_csv
from numpy import linalg, array
from algo.greedy_rotate import greedy_rotate
from algo.cross_path import cross_path
from algo.two_opt import two_opt
from algo.simulated_annealing import sim_annealing
import math

ini_time = time()

# ff4 Fake Location
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
# pla7397_783
# uy734 79114 Uruguay
# zi929 95345 Zimbabwe
# lu980 11340 Luxembourg
# pla7397_980
# sw24978 855597 Sweden
# argument parser -----------------------------------------------------------------
parser = ArgumentParser(description='Solving the TSP.')
parser.add_argument('input', metavar='i', nargs='?', default='pr439.txt',
                    help='the path to input coordinates file')
parser.add_argument('output', metavar='o', nargs='?', default='output-tour.txt',
                    help='the path to output tour file')
parser.add_argument('time', metavar='t', type=int, nargs='?', default=180,
                    help='the maximum running time')
args = vars(parser.parse_args())


# end of argument parser ----------------------------------------------------------

# helper functions ----------------------------------------------------------------
def gen_node(num):
    seed()
    a = []
    for i in range(num):
        a.append([randint(0, num * 2), randint(0, num * 2)])
    return array(a)


def rotate(origin, point, angle):
    """
    Rotate a point counterclockwise by a given angle around a given origin.

    The angle should be given in radians.
    """
    ox, oy = origin
    px = point[0]
    py = point[1]

    qx = ox + math.cos(angle) * (px - ox) - math.sin(angle) * (py - oy)
    qy = oy + math.sin(angle) * (px - ox) + math.cos(angle) * (py - oy)
    return qx, qy
# end of helper functions ---------------------------------------------------------

# data & arguments parsing --------------------------------------------------------
deadline = time() + args['time']

node = read_csv(args['input'], sep=" ", header=None, names=['idx', 'x', 'y']).set_index('idx')[['y', 'x']].values

euclideanMap = [[0 for x in range(len(node))] for y in range(len(node))]
for i in range(len(node)):
    for j in range(len(node)):
        euclideanMap[i][j] = round(linalg.norm(node[i] - node[j]))

for n in node:
    n[0], n[1] = rotate([0, 0], [n[0], n[1]], 1)
# end of data & arguments parsing -------------------------------------------------

# main <><><><><><><><>><><><><><><><><><><><><><><><><><><><><><><><>><><><><><><><><><><><>><><><><><><><><><><><><><>
duration = args["time"]
final_length = None
final_route = None

g_length, g_route = greedy_rotate(euclideanMap, node)
print("Greedy: " + str(g_length) + " " + str(g_route))
print("time: ", time()-ini_time)
duration -= (time()-ini_time)
print(duration)

if len(node) <= 0: #52
    best_sa_length = None
    best_sa_route = None
    for _ in range(4):
        # worst case 30 sec per run
        sa_length, sa_route = sim_annealing(euclideanMap, node, g_length, g_route, 2000000)
        print(sa_length)
        if best_sa_length is None or sa_length < best_sa_length:
            best_sa_length = sa_length
            best_sa_route = sa_route
    final_length = best_sa_length
    final_route = best_sa_route
elif len(node) >= 0: #929
    t_length, t_route = two_opt(euclideanMap, node, g_length, g_route, 0)
    print("two-opt: <<" + str(t_length) + ">> " + str(t_route))
    print("time: ", time() - ini_time)
    print()
    # final_length = t_length
    # final_route = t_route

    ini_time = time()
    c_length, c_route = cross_path(euclideanMap, node, g_length, g_route)
    print("Cross: " + str(c_length) + " " + str(c_route))
    print("time: ", time()-ini_time)
    t_length, t_route = two_opt(euclideanMap, node, c_length, c_route, duration)
    print("two-opt: <<" + str(t_length) + ">> " + str(t_route))
    print("time: ", time() - ini_time)
    print()
    # final_length = t_length
    # final_route = t_route

    # s_length, s_route = sim_annealing(euclideanMap, node, g_length, g_route, 2000000)
    # print("sim_ann: cost " + str(s_length) + " " + str(s_route))
    # print("time: ", time()-ini_time)
    # final_length = s_length
    # final_route = s_route
    # print()

# print("running time: ", time() - ini_time)
# print("optimal tour: ", final_route)
# print("optimal length: ", final_length)
# end of main <><><><><><><><>><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><>><><><><><><><><><><>
