# from .plotter.plotter import Plotter
from random import seed, randrange
from time import time


def two_opt(euclidean_map, init_length, route, deadline):
    seed()
    route_len = len(route)-1
    global_route = route[:route_len].copy()
    global_length = init_length

    def randpos():
        return randrange(route_len)

    def cal_length(r):
        c = 0
        for i in range(len(r)-1):
            j = i+1
            c += euclidean_map[r[i]][r[j]]
        c += euclidean_map[r[0]][r[-1]]
        return c
    while time() < deadline:
        curr_route = global_route.copy()
        i = randpos()
        j = randpos()
        temp = curr_route[i]
        curr_route[i] = curr_route[j]
        curr_route[j] = temp
        curr_length = cal_length(curr_route)
        # Plotter(node, curr_length, curr_route, True)
        if curr_length <= global_length:
            global_route = curr_route
            global_length = curr_length
    global_route.append(global_route[0])
    # Plotter(node, global_length, global_route, True)
    return global_length, global_route

