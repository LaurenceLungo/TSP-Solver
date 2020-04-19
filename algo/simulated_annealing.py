from random import seed, randrange, random
from time import time
from math import exp

seed()


def sim_annealing(euclidean_map, init_length, route, num_iter):
    print("applying simulated annealing...")
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
            c += euclidean_map[r[i]][r[j]]
        c += euclidean_map[r[0]][r[-1]]
        return c

    init_temp = 25000
    temp = init_temp
    percent_temp = .999993

    for i in range(num_iter):
        curr_route, curr_length = two_opt(global_route)
        if curr_length < global_length:
            global_route = curr_route
            global_length = curr_length
        elif curr_length > global_length:
            probability_for_risk = exp(-(curr_length - global_length) / temp)
            take_the_risk = biased_flip(probability_for_risk)
            if take_the_risk:
                global_route = curr_route
                global_length = curr_length
        temp *= percent_temp
        if global_length < global_best_length:
            global_best_length = global_length
            global_best_route = global_route.copy()
    global_best_route.append(global_best_route[0])
    return global_best_length, global_best_route
