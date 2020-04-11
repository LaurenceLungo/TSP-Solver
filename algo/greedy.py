from .plotter.plotter import Plotter

def greedy_rotate(euclideanMap, node):
    globalTourLength = 9999999
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
                neighbourLength.append(euclideanMap[currentNode][j])
            if len(neighbourLength) > 0:
                tourLength += min(neighbourLength)
                currentNode = euclideanMap[currentNode].index(min(neighbourLength))
            else:
                tourLength += euclideanMap[currentNode][0]
                currentNode = p
                tourRoute.append(currentNode)
                break
        if tourLength < globalTourLength:
            globalTourLength = tourLength
            globalTourRoute = tourRoute
    pltr = Plotter(node, globalTourLength, globalTourRoute, True)
    pltr.show()
    return globalTourLength, globalTourRoute