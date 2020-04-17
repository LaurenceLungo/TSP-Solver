from .plotter.plotter import Plotter


def greedy_rotate(euclidean_map, node):
    globalTourLength = None
    globalTourRoute = []
    for p in range(len(euclidean_map)):
        unvisitedNodes = [i for i in range(len(euclidean_map))]
        tourLength = 0
        tourRoute = []
        currentNode = p
        while unvisitedNodes:
            unvisitedNodes.remove(currentNode)
            tourRoute.append(currentNode)
            neighbourLength = []
            for j in unvisitedNodes:
                neighbourLength.append((euclidean_map[currentNode][j], j))
            if len(neighbourLength) > 0:
                minNeighbourLength = neighbourLength[0][0]
                minNeighbour = neighbourLength[0][1]
                for i in neighbourLength:
                    if i[0] < minNeighbourLength:
                        minNeighbourLength = i[0]
                        minNeighbour = i[1]
                tourLength += minNeighbourLength
                currentNode = minNeighbour
            else:
                tourLength += euclidean_map[currentNode][p]
                currentNode = p
                tourRoute.append(currentNode)
                break
        if globalTourLength is None or tourLength < globalTourLength:
            globalTourLength = tourLength
            globalTourRoute = tourRoute
    # Plotter(node, globalTourLength, globalTourRoute, True)
    return globalTourLength, globalTourRoute
