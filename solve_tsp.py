from time import time
from random import seed, randint
from argparse import ArgumentParser
from pandas import read_csv
from numpy import linalg, array
from math import sin, cos

from algo.greedy_rotate import greedy_rotate
from algo.cross_path import cross_path
from algo.two_opt import two_opt
from algo.simulated_annealing import sim_annealing

ini_time = time()  # start the timer here

# ===== List of datasets =====
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
# pr1002_600
# rat783
# pla7397_783
# uy734 79114 Uruguay
# zi929 95345 Zimbabwe
# -- lu980 11340 Luxembourg
# pla7397_980
# sw24978 855597 Sweden
# ===========================

# argument parser -----------------------------------------------------------------
parser = ArgumentParser(description='Solving the TSP.')
parser.add_argument('input', metavar='i', nargs='?', default='wi29.txt',
                    help='the path to input coordinates file')
parser.add_argument('output', metavar='o', nargs='?', default='output-tour.txt',
                    help='the path to output tour file')
parser.add_argument('time', metavar='t', type=int, nargs='?', default=180,
                    help='the maximum running time')
args = vars(parser.parse_args())


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
node = read_csv(args['input'], sep=" ", header=None, names=['idx', 'x', 'y']).set_index('idx')[['y', 'x']].values

euclidean_map = [[0 for x in range(len(node))] for y in range(len(node))]
for i in range(len(node)):
    for j in range(len(node)):
        euclidean_map[i][j] = int(round(linalg.norm(node[i] - node[j])))

for n in node:
    n[0], n[1] = rotate([0, 0], [n[0], n[1]], 1)
# end of data & arguments parsing -------------------------------------------------

# main <><><><><><><><>><><><><><><><><><><><><><><><><><><><><><><><>><><><><><><><><><><><>><><><><><><><><><><><><><>
duration = args["time"]
deadline = time() + duration
final_length = None
final_route = None

g_length, g_route = greedy_rotate(euclidean_map, node)
print("Greedy: " + str(g_length) + " " + str(g_route))
print("time: ", time() - ini_time)
duration -= (time() - ini_time)

if len(node) <= 52:
    best_sa_length = None
    best_sa_route = None
    for _ in range(int(args["time"]/30 - 1)):
        # worst case 30 sec per run
        sa_length, sa_route = sim_annealing(euclidean_map, node, g_length, g_route, 2000000)
        print(sa_length)
        if best_sa_length is None or sa_length < best_sa_length:
            best_sa_length = sa_length
            best_sa_route = sa_route
    final_length = best_sa_length
    final_route = best_sa_route
elif len(node) <= 600:  # 575
    c_length, c_route = cross_path(euclidean_map, node, g_length, g_route, deadline)
    print("Cross: " + str(c_length) + " " + str(c_route))
    print("time: ", time() - ini_time)
    t_length, t_route = two_opt(euclidean_map, c_length, c_route, deadline)
    print("two-opt: <<" + str(t_length) + ">> " + str(t_route))
    print("time: ", time() - ini_time)
    final_length = t_length
    final_route = t_route
else:
    t_length, t_route = two_opt(euclidean_map, g_length, g_route, deadline)
    print("two-opt: <<" + str(t_length) + ">> " + str(t_route))
    print("time: ", time() - ini_time)
    final_length = t_length
    final_route = t_route

print()
print("running time: ", time() - ini_time)
print("optimal tour: ", final_route)
print("optimal length: ", final_length)

output_string = "tour cost: " + str(final_length) + "\n" + "tour: " + str(final_route)
out = open(args['output'], 'w')
out.write(output_string)
out.close()
# end of main <><><><><><><><>><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><>><><><><><><><><><><>
