import pygame
from cell import *
import math
from constants import *
from UI.setup import *

pygame.init()
screen = pygame.display.set_mode(size)
clock = pygame.time.Clock()
fps = 30
hue = 0

cell_size = 40

cols = Height//cell_size
rows = Width//cell_size

grid = [[Cell(j, i) for i in range(cols)] for j in range(rows)]
path = []

closedSet = []
openSet = []
diagonalToggle = True

for x in range(rows):
    for y in range(cols):
        grid[x][y].diagonal = diagonalToggle
        grid[x][y].updateNeighbors(grid)


startNode   = grid[0][0]
startNode.itsObstacle = False
goalNode    = grid[rows-1][cols-1]
goalNode.itsObstacle = False
goalNode.color = (0, 0, 255)

openSet.append(startNode)

# get the Heuristic distance
def euclideanDistance(a, b):
    dist = (a.x - b.x )*(a.x - b.x ) + (a.y - b.y)*(a.y - b.y)
    return math.sqrt(dist)

def manhattanDistance(a, b):
    dist = abs(a.x - b.x) + abs(a.y-b.y)
    return dist

def octileDistance(a, b):
    deltaX = abs(a.x - b.x)
    deltaY = abs(a.y - b.y)
    octile = 1.414 * min(deltaX, deltaY) + abs(deltaX - deltaY)
    return octile

def ChebyshevDistance(a, b):
    dist = max(abs(a.x - b.x), abs(a.y - b.y))
    return dist


toggles = [EuclideanDistanceToggle, ManhattanDistanceToggle, OctileDistanceToggle, ChebyshevDistanceToggle]
Heuristic = [euclideanDistance, manhattanDistance, octileDistance, ChebyshevDistance]
distBooleans = [False, True, False, False]

def NegateOther(_index):
    for i in range(len(distBooleans)):
        if i != _index:
            distBooleans[i] = False
            toggles[i].state = False


showUI  = False
done    = False
pause   = False
reset   = False
mouseClicked = False
instantiateObstacles = False
run     = True

while run:
    clock.tick(fps)
    goalNode.color = (0, 0, 255)
    screen.fill(black)
    mouseClicked = False

    currentIndex = distBooleans.index(True)

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
    # algorithm
    if pause == False:
        if len(openSet) > 0 and done != True:
            index = 0
            # find the current node
            for i in range(len(openSet)):
                if int(openSet[i].fCost) < int(openSet[index].fCost):
                    index = i
            currentNode = openSet[index]
            # check if it's done
            if currentNode == goalNode:
                done = True

            # add current node to closedSet and remove it from openset
            if done == False:
                closedSet.append(currentNode)
                if currentNode in openSet:
                    openSet.remove(currentNode)
                # check the neighbor nodes
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
                            neighbor.hCost = Heuristic[currentIndex](neighbor,goalNode)
                            neighbor.fCost = neighbor.gCost + neighbor.hCost
                            neighbor.previous = currentNode

    for x in range(rows):
        for y in range(cols):
            grid[x][y].Display(screen, cell_size, cell_size)

    path = []
    temp = currentNode
    path.append(temp)

    while temp.previous != None:
        path.append(temp.previous)
        temp = temp.previous

    for cell in openSet:
        cell.color = openColor

    for _i, cell in enumerate(closedSet):
        # c = pygame.Color(0, 0, 0)
        # c.hsva = (_i%360, 100, 100, 100)
        # _color = c
        # cell.color = _color
        cell.color = closedColor

    for _i, cell in enumerate(path):
        c = pygame.Color(0, 0, 0)
        c.hsva = (_i+10%360, 100, 100, 100)
        _color = c
        cell.color = _color
        #cell.color = (254, 210, 1)
    if done:
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

        startNode   = grid[0][0]
        startNode.itsObstacle = False
        goalNode    = grid[rows-1][cols-1]
        goalNode.itsObstacle = False
        goalNode.color = (0, 0, 255)

        openSet.append(startNode)
        pause = True
        PauseButton.state = True
        reset = False
        ResetButton.state = False
    pygame.display.flip()

pygame.quit()
