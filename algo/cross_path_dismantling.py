def cross_path_dismantling(euclidean_map, node, route):
    route_len = len(route) - 1
    global_route = route[:route_len].copy()

    def is_intersecting(s1, e1, s2, e2):
        if (e1[0] == s1[0] and e2[0] == s2[0]) \
                or (((e1[0] == s1[0]) and (e2[0] == s2[0])) and
                    (((e1[1] - s1[1]) / (e1[0] - s1[0])) == ((e2[1] - s2[1]) / (e2[0] - s2[0])))):
            return 0

        def is_touching(p, s, e):
            if p[0] == s[0] == e[0]:  # 3 points form a vertical line
                return True
            elif not (e[0] == p[0]) == (p[0] == s[0]):
                return False
            elif (e[0] == p[0]) and (p[0] == s[0]):
                return True
            return ((e[1] - p[1]) / (e[0] - p[0])) == ((p[1] - s[1]) / (p[0] - s[0]))

        if is_touching(s2, s1, e1) or is_touching(e2, s1, e1) or is_touching(e1, s2, e2) or is_touching(s1, s2, e2):
            return False

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
            c += euclidean_map[r[i]][r[j]]
        c += euclidean_map[r[0]][r[-1]]
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
            if not len({sp1, ep1, sp2, ep2}) == 4:
                sp2 += 1
                continue
            if is_intersecting(node[spos1], node[epos1], node[spos2],
                               node[epos2]):
                temp = global_route[ep1]
                global_route[ep1] = global_route[sp2]
                global_route[sp2] = temp
                global_route[ep1 + 1: sp2] = global_route[ep1 + 1: sp2][::-1]

                sp1 = -1
                sp2 = 0
                break
            else:
                sp2 += 1
        sp2 = 0
        sp1 += 1

    global_length = cal_length(global_route)
    global_route.append(global_route[0])
    # Plotter(node, global_length, global_route, True)
    return global_length, global_route
