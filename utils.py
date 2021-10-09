from constants import *
from math import sqrt, ceil
# get the Heuristic distance
def euclideanDistance(a, b, diagonalCheck=False):
    dist = (a.x - b.x )*(a.x - b.x ) + (a.y - b.y)*(a.y - b.y)
    return sqrt(dist)

def SimpleDistance(a, b):
    return (a.x - b.x )*(a.x - b.x ) + (a.y - b.y)*(a.y - b.y)

def manhattanDistance(a, b, diagonalCheck=False):
    distX = abs(a.x - b.x)
    distY = abs(a.y - b.y)
    # if diagonalCheck == True:
    #     if AreDiagonal(a, b):
    #         return SimpleDistance(a, b)

    return distX + distY

def octileDistance(a, b, diagonalCheck=False):
    deltaX = abs(a.x - b.x)
    deltaY = abs(a.y - b.y)
    octile = 1.414 * min(deltaX, deltaY) + abs(deltaX - deltaY)
    return octile

def ChebyshevDistance(a, b, diagonalCheck=False):
    dist = max(abs(a.x - b.x), abs(a.y - b.y))
    return dist

def AreDiagonal(a, b, diagonalCheck=False):
    #bottom-right
    if a.x + 1 == b.x and a.y+1 == b.y:

        return True
    #top-right
    elif a.x + 1 == b.x and a.y-1 == b.y:
        return True
    #bottom-left
    elif a.x - 1 == b.x and a.y + 1 == b.y:
        return True
    #top-left
    elif a.x - 1 == b.x and a.y - 1 == b.y:
        return True
    else:
        return False
