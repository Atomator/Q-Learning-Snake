import math
import random
import sys
import pygame

class apple(object):
    def __init__(self, a):
        self.applx = 60
        self.apply = 200
        self.a = a

    def makeLocation(self):
        self.applx = random.randint(0,(width/20)-1) * 20
        self.apply = random.randint(0,(width/20)-1) * 20

    def draw(self, surface):
        pygame.draw.rect(surface, (255, 0, 0), (self.applx, self.apply, 20, 20))

class snake(object):
    def __init__(self, color, pos):
        self.color = color
        self.dirnx = 0
        self.dirny = 0
        self.cube = cube(pos)
        self.apple = apple(True)
        self.x = [240]
        self.y = [240]

        # self.body.append(self.head)
    def move(self, surface):
        # Used to make sure the Mac thinks the program is responding

        # Checks for an event every clock tick then loops through events to see if a pygame.QUIT is called
        for event in pygame.event.get():
            # If this event is called, it quits the program
            if event.type == pygame.QUIT:
                pygame.quit()

            # This in an array that has 1s or 0s depending on whether a key was pressed
            keys = pygame.key.get_pressed()

            for key in keys:
                if keys[pygame.K_LEFT] and (self.dirnx != 1 or self.dirny != 0):
                    self.dirnx = -1
                    self.dirny = 0
                elif keys[pygame.K_RIGHT] and (self.dirnx != -1 or self.dirny != 0):
                    self.dirnx = 1
                    self.dirny = 0
                elif keys[pygame.K_UP] and (self.dirnx != 0 or self.dirny != 1):
                    self.dirnx = 0
                    self.dirny = -1
                elif keys[pygame.K_DOWN] and (self.dirnx != 0 or self.dirny != -1):
                    self.dirnx = 0
                    self.dirny = 1

        # Creates a array with each the updated values from the set function above
        if self.x[0] > 480: self.x[0] = 0
        elif self.y[0] > 480: self.y[0] = 0
        elif self.x[0] < 0: self.x[0] = 480
        elif self.y[0] < 0: self.y[0] = 480
        else:
             self.x[0] = self.x[0] + self.dirnx * 20
             self.y[0] = self.y[0] + self.dirny * 20

        if self.x[0] == self.apple.applx and self.y[0] == self.apple.apply:
            self.apple.makeLocation()
            self.x.append(self.x[len(self.x)-1])
            self.y.append(self.y[len(self.y)-1])

        for i in range(len(self.x)-1,0,-1):
            self.x[i] = self.x[i-1]
            self.y[i] = self.y[i-1]

        for i in range(len(self.x)-1,2,-1):
            if self.x[i] == self.x[0] and self.y[i] == self.y[0]:
                self.x = [240]
                self.y = [240]
                self.dirnx = 0
                self.dirny = 0
                break

    def reset(self, pos):
        pass
    def addCube(self):
        pass
    def draw(self, surface):
        self.apple.draw(surface)
        for i in range(len(self.x)):
            self.cube.draw(surface, self.x[i], self.y[i])


class cube (object):
    def __init__ (self, pos):
        self.pos = pos

    def draw (self, surface, x, y):
        pygame.draw.rect(surface, (0, 255, 0), (x, y, 20, 20))

def redrawWindow(surface):
    global width
    surface.fill((0,0,0))
    s.draw(surface)
    pygame.display.update()

def main():
    global width, s, speed, a
    width = 500
    win = pygame.display.set_mode((width , width))
    s = snake((255,0,0), (250,250))
    a = apple(True)
    flag = True

    clock = pygame.time.Clock()

    while flag:
        clock.tick(15)
        redrawWindow(win)
        s.move(win)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                 sys.exit(0)

pygame.init()
main()
