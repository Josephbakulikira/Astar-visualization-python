import pygame
import random

class Cell:
    def __init__(self, x, y, gcost = 0, hcost = 0, fcost = 0):
        self.x = x
        self.y = y
        self.gCost = gcost
        self.hCost = hcost
        self.fCost = fcost
        self.itsObstacle = False
        self.neighbors = []
        self.color = (255, 255,255)
        self.previous = None;
        # if random.randint(0, 10) == 1:
        #     self.itsObstacle = True

    def updateNeighbors(self, nodes):
        x, y = self.x, self.y

        #right
        if x + 1 < len(nodes):
            self.neighbors.append(nodes[x+1][y])
        #left
        if x - 1 >= 0:
            self.neighbors.append(nodes[x-1][y])
        #bottom
        if y + 1 < len(nodes[0]):
            self.neighbors.append(nodes[x][y+1])
        #top
        if y - 1 >= 0:
            self.neighbors.append(nodes[x][y-1])

        #bottom-right
        if x + 1 < len(nodes) and y+1 < len(nodes[0]):
            self.neighbors.append(nodes[x + 1][y + 1])
        #top-right
        if x + 1 < len(nodes) and y-1 >= 0:
            self.neighbors.append(nodes[x + 1][y - 1])
        #bottom-left
        if x - 1 >= 0 and y + 1 <len(nodes[0]):
            self.neighbors.append(nodes[x - 1][y + 1])
        #top-left
        if x - 1 >= 0 and y - 1 >= 0:
            self.neighbors.append(nodes[x - 1][y - 1])


    def Display(self, screen, w, h):
        if self.itsObstacle:
            pygame.draw.rect(screen, (0, 0, 0), pygame.Rect(self.x * w, self.y*h, w-1, h-1))
        else:
            pygame.draw.rect(screen, self.color, pygame.Rect(self.x * w, self.y*h, w-1, h-1))

def Drawline(cells,w, h, screen, color=(255, 0, 255)):
    for i in range(len(cells)):
        if i + 1 < len(cells):
            pygame.draw.line(screen, color, (int(cells[i].x * w), int(cells[i].y * h)), (int(cells[i+1].x * w), int(cells[i+1].y * h)), 10)
