from .plotter.plotter import Plotter


def cross_path(euclideanMap, node, init_length, route):
    route_len = len(route) - 1
    global_route = route[:route_len].copy()
    global_length = init_length

    def is_intersecting(s1, e1, s2, e2):
        denominator = ((e1[0] - s1[0]) * (e2[1] - s2[1])) - ((e1[1] - s1[1]) * (e2[0] - s2[0]))
        numerator1 = ((s1[1] - s2[1]) * (e2[0] - s2[0])) - ((s1[0] - s2[0]) * (e2[1] - s2[1]))
        numerator2 = ((s1[1] - s2[1]) * (e1[0] - s1[0])) - ((s1[0] - s2[0]) * (e1[1] - s1[1]))

        if denominator == 0:
            return numerator1 == 0 and numerator2 == 0
        r = numerator1 / denominator
        s = numerator2 / denominator
        return (0 <= r <= 1) and (0 <= s <= 1)

    def cal_length(r):
        c = 0
        for i in range(len(r) - 1):
            j = i + 1
            c += euclideanMap[r[i]][r[j]]
        c += euclideanMap[r[0]][r[-1]]
        return c

    sp1 = 0
    sp2 = 0
    while sp1 < route_len:
        if sp1 == (route_len - 1):
            ep1 = 0
        else:
            ep1 = sp1 + 1
        while sp2 < (route_len - 1):
            ep2 = sp2 + 1
            spos1 = global_route[sp1]
            epos1 = global_route[ep1]
            spos2 = global_route[sp2]
            epos2 = global_route[ep2]
            # if (sp1 == sp2 and ep1 == ep2) or (ep1 == sp2) or (ep2 == sp1):
            if not len({sp1, ep1, sp2, ep2}) == 4:
                sp2 += 1
                continue
            if is_intersecting(node[spos1], node[epos1], node[spos2],
                               node[epos2]):
                temp_route = global_route.copy()
                temp = temp_route[ep1]
                temp_route[ep1] = temp_route[sp2]
                temp_route[sp2] = temp
                if cal_length(temp_route) < global_length:
                    global_route = temp_route.copy()
                    global_length = cal_length(temp_route)

                    print("(", spos1, ", ", epos1, ") (", spos2, ", ", epos2, ")")
                    temp_route.append(temp_route[0])
                    Plotter(node, cal_length(temp_route), temp_route, True)
                    del temp_route[-1]
                    sp1 = -1
                    sp2 = 0
                    break
                # print("bad (", spos1, ", ", epos1, ") (", spos2, ", ", epos2, ")")
                sp2 += 1
            else:
                sp2 += 1
        sp2 = 0
        sp1 += 1

    global_route.append(global_route[0])
    Plotter(node, global_length, global_route, True)
    return global_length, global_route
