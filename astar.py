import pygame
from cell import *
import os
import math

width, height = 1920, 1080
size = (width, height)
black, white = (38, 38, 38), (251, 255, 194)

pygame.init()
screen = pygame.display.set_mode(size, pygame.FULLSCREEN)
clock = pygame.time.Clock()
fps = 60

closedColor = (22, 142, 98)
openColor = (45, 183, 250)

cols = 54
rows = 96
w = width//rows
h = height//cols

grid = [[Cell(j, i) for i in range(cols)] for j in range(rows)]
path = []

closedSet = []
openSet = []

for x in range(rows):
    for y in range(cols):
        grid[x][y].updateNeighbors(grid)

startNode = grid[0][0]
startNode.itsObstacle = False
goalNode= grid[rows-1][cols-1]
goalNode.itsObstacle = False
goalNode.color = (0, 0, 255)
openSet.append(startNode)

# get the Heuristic distance
def euclideanDistance(a, b):
    distance = abs((a.x - b.x ) ** 2 + (a.y - b.y) ** 2)
    return math.sqrt(distance)

def manhattanDistance(a, b):
    distance = abs((a.x - b.x) + (a.y - b.y))
    return distance

def octileDistance(a, b):
    deltaX = abs(a.x - b.x)
    deltaY = abs(a.y - b.y)
    octile = 1.414 * min(deltaX, deltaY) + abs(deltaX - deltaY)
    return octile

def ChebyshevDistance(a, b):
    distance = max(abs(a.x - b.x), abs(a.y - b.y))
    return distance


done = False
run = True
while run:
    clock.tick(fps)
    goalNode.color = (0, 0, 255)
    screen.fill(black)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False


    if len(openSet) > 0 and done != True:
        #index here is the index of the node with the lowest fCost
        index = 0
        for i in range(len(openSet)):
            # print(openSet[i].fCost)
            if int(openSet[i].fCost) < int(openSet[index].fCost):
                index = i
        currentNode = openSet[index]
        if currentNode == goalNode:
            done = True
        if done == False:
            closedSet.append(currentNode)
            if currentNode in openSet:
                openSet.remove(currentNode)

            for neighbor in currentNode.neighbors:
                if neighbor not in closedSet and neighbor.itsObstacle == False:
                    cost = currentNode.gCost + 1
                    checkPath = False
                    if neighbor in openSet:
                        if cost < neighbor.gCost:
                            neighbor.gCost = cost
                            checkPath = True
                    else:
                        neighbor.gCost = cost
                        checkPath = True
                        openSet.append(neighbor)
                    if checkPath:
                        neighbor.hCost = manhattanDistance(neighbor,goalNode)
                        neighbor.fCost = neighbor.gCost + neighbor.hCost
                        neighbor.previous = currentNode
    else:
        pass

    for x in range(rows):
        for y in range(cols):
            grid[x][y].Display(screen, w, h)

    path = []
    temp = currentNode
    path.append(temp)
    while temp.previous != None:
        path.append(temp.previous)
        temp = temp.previous


    for cell in openSet:
        cell.color = openColor

    for cell in closedSet:
        cell.color = closedColor

    for cell in path:
        cell.color = (254, 210, 1)
    Drawline(path, w, h, screen)
    pygame.display.update()

pygame.quit()
