import pygame
from cell import *
import os
import math

width, height = 1000, 1000
size = (width, height)
black, white = (0, 0, 0), (255, 255, 255)

pygame.init()
screen = pygame.display.set_mode(size, pygame.FULLSCREEN)
clock = pygame.time.Clock()
fps = 60

closedColor = (255, 0, 0)
openColor = (0, 255, 0)

cols = 40
rows = 40
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
goalNode= grid[rows-1][cols-1]
goalNode.color = (0, 0, 255)
openSet.append(startNode)


def getDistance(a, b):
    distance = abs((a.x - b.x ) ** 2 + (a.y - b.y) ** 2)
    return math.sqrt(distance)

done = False
run = True
while run:
    clock.tick(fps)
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
                        neighbor.hCost = getDistance(neighbor,goalNode)
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
        cell.color = (0, 255, 255)
    Drawline(path, w, h, screen, black)
    pygame.display.update()

pygame.quit()
