from .plotter.plotter import Plotter
from random import seed, randrange, random
import time, math
import numpy as np

seed()


def sim_annealing(euclideanMap, node, init_length, route, num_iter):
    st = time.time()
    route_len = len(route) - 1
    global_route = route[:route_len].copy()
    global_length = init_length
    global_best_route = global_route
    global_best_length = global_length

    def randpos():
        return randrange(route_len)

    def biased_flip(p):
        return True if random() < p else False

    def two_opt(existing_route):
        new_route = existing_route.copy()
        randpos1 = randpos()
        randpos2 = randpos()
        t = new_route[randpos1]
        new_route[randpos1] = new_route[randpos2]
        new_route[randpos2] = t

        new_length = cal_length(new_route)
        return new_route, new_length

    def three_opt(existing_route):
        new_route = existing_route.copy()
        randpos1 = randpos()
        randpos2 = randpos()
        randpos3 = randpos()
        t = new_route[randpos1]
        new_route[randpos1] = new_route[randpos2]
        new_route[randpos2] = t
        t = new_route[randpos2]
        new_route[randpos2] = new_route[randpos3]
        new_route[randpos3] = t

        new_length = cal_length(new_route)
        return new_route, new_length

    def cal_length(r):
        c = 0
        for i in range(len(r) - 1):
            j = i + 1
            c += euclideanMap[r[i]][r[j]]
        c += euclideanMap[r[0]][r[-1]]
        return c

    init_temp = 25000
    temp = init_temp
    amb_temp = 0.00
    k = .0000125 / 1.4
    delta_temp = (init_temp - amb_temp) / num_iter
    percent_temp = .999993
    prob_graph = []
    temp_graph = []
    chkpt = []
    y = 16
    z = 10
    for f in range(z, y):
        chkpt.append(int(num_iter * f / y))

    for i in range(num_iter):
        curr_route, curr_length = two_opt(global_route)
        if curr_length < global_length:
            global_route = curr_route
            global_length = curr_length
            # print(str(global_length))  # + " time: " + str(time.time() - st) + " iter:" + str(i))
        elif curr_length > global_length:
            probability_for_risk = math.exp(-(curr_length - global_length) / temp)
            fuck_it = biased_flip(probability_for_risk)
            prob_graph.append([i, probability_for_risk])
            temp_graph.append([i, temp])
            if fuck_it:
                global_route = curr_route
                global_length = curr_length
                # print("*" + str(global_length))  # + " time: " + str(time.time() - st) + " iter:" + str(i))
        #     temp += (temp / 2)
        # temp -= delta_temp
        temp *= percent_temp
        # temp = amb_temp + (temp - amb_temp)*math.exp(-k*i)
        if global_length < global_best_length:
            global_best_length = global_length
            global_best_route = global_route.copy()
    Plotter(np.array(prob_graph), 0, [0], False, True)
    # Plotter(np.array(temp_graph), 0, [0], False, True)
    global_best_route.append(global_best_route[0])
    # Plotter(node, global_best_length, global_best_route, False)
    return global_best_length, global_best_route
