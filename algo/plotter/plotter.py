from matplotlib import pyplot as plt
from matplotlib.animation import FuncAnimation


class Plotter:

    def __init__(self, node_map, length, route, annotate_flag=False, small_marker=False):
        self.node_map = node_map
        self.start = node_map[route[0]]
        self.route = route
        self.length = length
        self.annotate_flag = annotate_flag
        self.small_marker = small_marker
        self.annotate = []
        for i in range(len(node_map)):
            self.annotate.append(i)
        self.fig, self.ax = plt.subplots()

        X = self.node_map.T[0]
        Y = self.node_map.T[1]
        if self.small_marker:
            self.ax.scatter(X, Y, s=0.1)
        else:
            self.ax.scatter(X, Y)
        if self.annotate_flag:
            for i in range(len(self.node_map)):
                self.ax.annotate(self.annotate[i], (X[i], Y[i]))
        self.ax.plot([self.start[0]], [self.start[1]], marker='x', markersize=12, color="red")
        for i in range(len(self.route) - 1):
            j = i + 1
            p1 = self.node_map[self.route[i]]
            p2 = self.node_map[self.route[j]]
            cx = [p1[0], p2[0]]
            cy = [p1[1], p2[1]]
            self.ax.plot(cx, cy, 'k-')
        self.ax.legend([self.length])
        plt.show()

