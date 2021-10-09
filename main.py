import pygame
from cell import *
import math
from constants import *
from UI.setup import *
from utils import *

pygame.init()
pygame.font.init()
screen = pygame.display.set_mode(size)
clock = pygame.time.Clock()
fps = 30
hue = 0



grid = [[Cell(j, i) for i in range(cols)] for j in range(rows)]
path = []

closedSet = []
openSet = []
diagonalToggle = True

for x in range(rows):
    for y in range(cols):
        grid[x][y].diagonal = diagonalToggle
        grid[x][y].updateNeighbors(grid)


startNode   = grid[3][cols//2]
startNode.itsObstacle = False
startNode.itsStart = True
goalNode    = grid[rows-3][cols//2]
goalNode.itsObstacle = False
goalNode.color = (0, 0, 255)
goalNode.itsDestination = True
openSet.append(startNode)




toggles = [EuclideanDistanceToggle, ManhattanDistanceToggle, OctileDistanceToggle, ChebyshevDistanceToggle]
Heuristic = [euclideanDistance, manhattanDistance, octileDistance, ChebyshevDistance]
distBooleans = [False, True, False, False]

def NegateOther(_index):
    for i in range(len(distBooleans)):
        if i != _index:
            distBooleans[i] = False
            toggles[i].state = False

_cellSize = 5

currentNode = Cell()

showUI  = False
showCost= False
done    = False
pause   = True
reset   = False

mouseClicked = False
instantiateObstacles = True
currentIndex = distBooleans.index(True)

run     = True

while run:
    clock.tick(fps)
    goalNode.color = (0, 0, 255)
    screen.fill(black)
    mouseClicked = False

    # Handle Events
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                run = False
            if event.key == pygame.K_RETURN or event.key == pygame.K_p:
                showUI = not showUI
            if event.key == pygame.K_SPACE:
                pause = not pause
            if event.key == pygame.K_r:
                reset = True
            if event.key == pygame.K_w:
                instantiateObstacles = not instantiateObstacles
            if event.key == pygame.K_s:
                showCost = not showCost
        if event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:
                mouseClicked = True
    # make walls
    if pygame.mouse.get_pressed()[0]:
        if instantiateObstacles == True:
            mx, my = pygame.mouse.get_pos()
            _x, _y = int(mx/cell_size), int(my/cell_size)
            if _x <= rows and _y <= cols:
                grid[_x][_y].itsObstacle = True
    elif pygame.mouse.get_pressed()[2]:
        mx, my = pygame.mouse.get_pos()
        _x, _y = int(mx/cell_size), int(my/cell_size)
        if _x <= rows and _y <= cols:
            grid[_x][_y].itsObstacle = False

    # Astar Algorithm
    if pause == False:
        if len(openSet) > 0 and done != True:
            if done == False and len(openSet) > 0:
                winner = 0
                for i in range(len(openSet)):
                    # set the Winner as the one with the least f Cost
                    if openSet[i].fCost < openSet[winner].fCost:
                        winner = i
                    # In case of a Tie of fCost
                    if openSet[i].fCost == openSet[winner].fCost:
                        # compare the gcost
                        if openSet[i].gCost > openSet[winner].gCost:
                            winner = i
                    if diagonalToggle == False:
                        if openSet[i].gCost == openSet[winner].gCost and openSet[i].euclidDist == openSet[winner].euclidDist:
                            winner = i
                currentNode = openSet[winner]
                previousNode = currentNode

                # check if we're done
                if currentNode == goalNode:
                    done = True
                # remove currentNode from openset
                openSet.remove(currentNode)
                closedSet.append(currentNode)

                neighbors = currentNode.updateNeighbors(grid)
                # neighbors = currentNode.neighbors
                # check the neighbor nodes
                for neighbor in neighbors:
                    if neighbor not in closedSet and neighbor.itsObstacle == False:
                        cost = currentNode.gCost + Heuristic[currentIndex](neighbor, currentNode)
                        checkPath = False
                        # check if it's better than the routes before
                        if neighbor not in openSet:
                            openSet.append(neighbor)
                        elif cost >= neighbor.gCost:
                            continue

                        neighbor.gCost = cost
                        neighbor.hCost = Heuristic[currentIndex](neighbor, goalNode, diagonalToggle)

                        if diagonalToggle == False:
                            neighbor.euclidDist = Heuristic[currentIndex](neighbor, goalNode, diagonalToggle)

                        neighbor.fCost = neighbor.gCost + neighbor.hCost
                        neighbor.previous = currentNode
                        neighbor.previous.color = (80, 80, 200)

    for x in range(rows):
        for y in range(cols):
            grid[x][y].Display(screen, cell_size, cell_size,_cellSize, showCost)

    path = []
    temp = currentNode
    path.append(temp)

    while temp.previous != None:
        path.append(temp.previous)
        temp = temp.previous

    for cell in openSet:
        cell.color = openColor

    for _i, cell in enumerate(closedSet):
        c = pygame.Color(0, 0, 0)
        c.hsva = ((cell.x + cell.y) + 5%360, 100, 100, 100)
        _color = c
        cell.color = _color
        # cell.color = closedColor

    for _i, cell in enumerate(path):
        cell.color = pathColor
    if done and showCost == False:
        Drawline(path, cell_size, cell_size, screen)

    # display ui
    if showUI == True:
        panel.Render(screen)

        DiagonalText.Render(screen)
        manhattanDistanceText.Render(screen)
        euclideanDistanceText.Render(screen)
        octileDistanceText.Render(screen)
        ChebyshevDistanceText.Render(screen)

        diagonalToggle = DiagonalToggle.Render(screen, mouseClicked)

        distBooleans[0] = EuclideanDistanceToggle.Render(screen, mouseClicked)
        distBooleans[1] = ManhattanDistanceToggle.Render(screen, mouseClicked)
        distBooleans[2] = OctileDistanceToggle.Render(screen, mouseClicked)
        distBooleans[3] = ChebyshevDistanceToggle.Render(screen, mouseClicked)

        for i in range(len(distBooleans)):
            if distBooleans[i] == True and i != currentIndex:
                NegateOther(i)
        currentIndex = distBooleans.index(True)

        ResetButton.Render(screen, mouseClicked)
        PauseButton.Render(screen, mouseClicked)

        if ResetButton.state == True:
            reset = ResetButton.state
        if mouseClicked == True:
            pause = PauseButton.state
            reset = ResetButton.state

        if pause:
            PauseButton.text = "Resume"
        else:
            PauseButton.text = "Pause"
    if reset:
        done = False
        grid = [[Cell(j, i) for i in range(cols)] for j in range(rows)]
        path.clear()

        closedSet.clear()
        openSet.clear()

        for x in range(rows):
            for y in range(cols):
                grid[x][y].diagonal = diagonalToggle
                grid[x][y].updateNeighbors(grid)

        startNode   = grid[3][cols//2]
        startNode.itsObstacle = False
        startNode.itsStart = True
        goalNode    = grid[rows-3][cols//2]
        goalNode.itsObstacle = False
        goalNode.color = (0, 0, 255)
        goalNode.itsDestination = True

        openSet.append(startNode)
        pause = True
        PauseButton.state = True
        reset = False
        ResetButton.state = False
    pygame.display.flip()

    if _cellSize >= cell_size:
        _cellSize = cell_size-1
    _cellSize += 1
pygame.quit()
