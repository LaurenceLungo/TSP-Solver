from .plotter.plotter import Plotter


def greedy_rotate(euclideanMap, node):
    globalTourLength = None
    globalTourRoute = []
    for p in range(len(euclideanMap)):
        unvisitedNodes = [i for i in range(len(euclideanMap))]
        tourLength = 0
        tourRoute = []
        currentNode = p
        while unvisitedNodes:
            unvisitedNodes.remove(currentNode)
            tourRoute.append(currentNode)
            neighbourLength = []
            for j in unvisitedNodes:
                neighbourLength.append((euclideanMap[currentNode][j], j))
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
                tourLength += euclideanMap[currentNode][p]
                currentNode = p
                tourRoute.append(currentNode)
                break
        if globalTourLength is None or tourLength < globalTourLength:
            globalTourLength = tourLength
            globalTourRoute = tourRoute
    Plotter(node, globalTourLength, globalTourRoute, False)
    return globalTourLength, globalTourRoute
