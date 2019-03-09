import math
import random
import sys
import pygame

class snake(object):
    body = []
    turns = {}
    def _init_(self, color, pos):
        self.color = color
        self.head = cube(pos)
        self.body.append(self.head)
    def move(self):
        pass
    def reset(self,pos):
        pass
    def addCube(self):
        pass
    def draw(self, surface):
        pass

def redrawWindow(surface):
    global rows, width
    surface.fill((0,0,0))
    drawGrid(width, rows, surface)
    pygame.display.update()

def drawGrid(w, rowds, surface):
    sizeBtwn = w / rows

    x = 0
    y = 0

    for l in range(rowds):
        x = x + sizeBtwn
        y = y + sizeBtwn

        pygame.draw.line(surface, (255,255,255), (x,0),(x,w))
        pygame.draw.line(surface, (255,255,255), (0,y),(w,y))

def main():
    global width, rows
    width = 500
    rows = 20
    win = pygame.display.set_mode((width , width))
    s = snake((255,0,0), (10,10))
    flag = True

    clock = pygame.time.Clock()

    while flag:
        pygame.time.delay(50)
        clock.tick(10)
        redrawWindow(win)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                 sys.exit(0)

    pass

pygame.init()
main()
