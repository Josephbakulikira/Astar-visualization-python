import pygame
import random
from constants import *
pygame.init()
pygame.font.init()
textColor   = (255, 255, 255)
# textFont    = pg.font.Font("freesansbold.ttf", size)
textFont    = pygame.font.SysFont("Arial", cell_size//5)
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
        self.previous = None
        self.diagonal = False
        # if random.randint(0, 25) == 1:
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

        if self.diagonal:
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


    def Display(self, screen, w, h, showText=False):
        if self.itsObstacle:
            pygame.draw.rect(screen, (0, 0, 0), pygame.Rect(self.x * w, self.y*h, w-1, h-1))
        else:
            pygame.draw.rect(screen, self.color, pygame.Rect(self.x * w, self.y*h, w-1, h-1))
        if showText and self.fCost > 0:
            textSurfaceFcost = textFont.render(str(self.fCost), True, textColor)
            textSurfaceGcost = textFont.render(str(self.gCost), True, textColor)
            textSurfaceHcost = textFont.render(str(self.hCost), True, textColor)
            text_rect1 = textSurfaceFcost.get_rect(center=(self.x * w + w/2, self.y * h + h/2))
            text_rect2 = textSurfaceGcost.get_rect(center=(self.x * w + w/5 , self.y * h + h/5 ))
            text_rect3 = textSurfaceHcost.get_rect(center=(self.x * w + w/1.2, self.y * h + h/1.2))
            screen.blit(textSurfaceFcost, text_rect1)
            screen.blit(textSurfaceGcost, text_rect2)
            screen.blit(textSurfaceHcost, text_rect3)


def Drawline(cells,w, h, screen, color=(17, 70, 245)):
    for i in range(len(cells)):
        if i + 1 < len(cells):
            pygame.draw.line(screen, color, (int(cells[i].x * w) + w//2 , int(cells[i].y * h) + h//2), (int(cells[i+1].x * w) + w//2, int(cells[i+1].y * h) + h//2), 2)
