from .plotter.plotter import Plotter
from random import seed, randrange, random
import time, math
import numpy as np


def sim_annealing(euclideanMap, node, init_length, route, num_iter):
    st = time.time()
    seed()
    route_len = len(route) - 1
    global_route = route[:route_len].copy()
    global_length = init_length

    def randpos():
        return randrange(route_len)

    def biased_flip(p):
        return True if random() < p else False

    def gen_new_route(existing_route):
        new_route = existing_route.copy()
        randpos1 = randpos()
        randpos2 = randpos()
        t = new_route[randpos1]
        new_route[randpos1] = new_route[randpos2]
        new_route[randpos2] = t
        new_length = cal_length(new_route)
        return new_route, new_length

    def cal_length(r):
        c = 0
        for i in range(len(r) - 1):
            j = i + 1
            c += euclideanMap[r[i]][r[j]]
        c += euclideanMap[r[0]][r[-1]]
        return c

    T = cal_length(global_route) == init_length
    timeout = time.time()
    init_time = time.time()
    temp = 1000
    abs_zero = 0
    delta_temp = (temp - abs_zero)/num_iter
    prob_graph = []
    for i in range(num_iter):
        curr_route, curr_length = gen_new_route(global_route)
        if curr_length < global_length:
            global_route = curr_route
            global_length = curr_length
            # print(str(global_length) + " time: " + str(time.time() - st) + " iter:" + str(iter_counter))
        elif curr_length > global_length:
            probability_for_risk = math.exp(-(curr_length - global_length)/temp)
            fuck_it = biased_flip(probability_for_risk)
            prob_graph.append([i, probability_for_risk])
            if fuck_it:
                global_route = curr_route
                global_length = curr_length
                # print("*" + str(global_length) + " time: " + str(time.time() - st) + " iter:" + str(iter_counter))
        temp -= delta_temp
    print("running time: " + str(time.time() - init_time))
    Plotter(np.array(prob_graph), 0, [0], False, True)
    global_route.append(global_route[0])
    Plotter(node, global_length, global_route, False)
    return global_length, global_route
