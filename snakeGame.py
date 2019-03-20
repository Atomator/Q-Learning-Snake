import math
import random
import sys
import pygame

from qLearn import *

class snakeOb(object):

    # Sets inital perameters
    def __init__(self, color, pos, snakeSize, width):
        self.color = color
        self.width = width
        self.snakeSize = snakeSize
        self.dirnx = 0
        self.dirny = 0
        self.cube = cube()
        self.x = [self.width/2]
        self.y = [self.width/2]

    # Responsible for movement of the snake
    def move(self, surface, move):
        if move == 0 and (self.dirnx != 1 or self.dirny != 0):
            self.dirnx = -1
            self.dirny = 0
        elif move == 1 and (self.dirnx != -1 or self.dirny != 0):
            self.dirnx = 1
            self.dirny = 0
        elif move == 2 and (self.dirnx != 0 or self.dirny != 1):
            self.dirnx = 0
            self.dirny = -1
        elif move == 3 and (self.dirnx != 0 or self.dirny != -1):
            self.dirnx = 0
            self.dirny = 1



        # Checks to see if the snake is off the screen, the moves it to ther other side if it is
        if self.x[0] > 400:
            self.x = [random.randint(0,(self.width/self.snakeSize)-1) * self.snakeSize]
            self.y = [random.randint(0,(self.width/self.snakeSize)-1) * self.snakeSize]
            self.dirnx = 0
            self.dirny = 0
        elif self.y[0] > 400:
            self.x = [random.randint(0,(self.width/self.snakeSize)-1) * self.snakeSize]
            self.y = [random.randint(0,(self.width/self.snakeSize)-1) * self.snakeSize]
            self.dirnx = 0
            self.dirny = 0
        elif self.x[0] < 0:
            self.x = [random.randint(0,(self.width/self.snakeSize)-1) * self.snakeSize]
            self.y = [random.randint(0,(self.width/self.snakeSize)-1) * self.snakeSize]
            self.dirnx = 0
            self.dirny = 0
        elif self.y[0] < 0:
            self.x = [random.randint(0,(self.width/self.snakeSize)-1) * self.snakeSize]
            self.y = [random.randint(0,(self.width/self.snakeSize)-1) * self.snakeSize]
            self.dirnx = 0
            self.dirny = 0
        else:
             self.x[0] = self.x[0] + self.dirnx * self.snakeSize
             self.y[0] = self.y[0] + self.dirny * self.snakeSize

        # Changes to position of each part of the snake
        for i in range(len(self.x)-1,0,-1):
            self.x[i] = self.x[i-1]
            self.y[i] = self.y[i-1]

        # Checks to see if the snake has run into itself (Needs to moved)
        for i in range(len(self.x)-1,2,-1):
            if self.x[i] == self.x[0] and self.y[i] == self.y[0]:
                self.x = [random.randint(0,(self.width/self.snakeSize)-1) * self.snakeSize]
                self.y = [random.randint(0,(self.width/self.snakeSize)-1) * self.snakeSize]
                self.dirnx = 0
                self.dirny = 0
                break

    # Adds a cube to the snake
    def addCube(self):
        self.x.append(self.x[len(self.x)-1])
        self.y.append(self.y[len(self.y)-1])

    # Draws each part of the snake
    def drawSnake(self, surface):
        for i in range(len(self.x)):
            self.cube.draw(surface, self.x[i], self.y[i], self.snakeSize, self.color)

# Object used to draw different cubes
class cube (object):

    # Init's the object
    def __init__ (self):
        pass

    # Draws the cube
    def draw (self, surface, x, y, snakeSize, color):
        pygame.draw.rect(surface, color, (x, y, snakeSize, snakeSize))

# Function used in order to create the snake
def createSnack(width, snakeSize, snake):
    # Makes sure cube is not drawn in location of snake
    while True:
        # Generates location
        x = random.randint(0,(width/snakeSize)-1) * snakeSize
        y = random.randint(0,(width/snakeSize)-1) * snakeSize
        # Checks to see if the snake is there, if it is continue the loop
        if len(list(filter(lambda z : z == x, snake.x))) > 0 and len(list(filter(lambda z : z == y, snake.y))) > 0:
            continue
        # If not, break
        else:
            break
    # Returns the variables needed to create the snack
    return (x,y)

# Redraws the window with the snake
def redrawWindow(surface, s, a, applx, apply, snakeSize):
    surface.fill((0,0,0))
    s.drawSnake(surface)
    a.draw(surface, applx, apply, snakeSize, (255,0,0))
    pygame.display.update()

# Main function that creates base objects and loops through objects and functions
def main():
    # Initial parameters
    width = 400
    snakeSize = 20
    win = pygame.display.set_mode((width , width))
    snake = snakeOb((0,255,0), (250,250), snakeSize, width)
    apple = cube()
    applx, apply = createSnack(width, snakeSize, snake)
    highScore = 0
    timeOut = 0
    flag = True

    # Starts the clock
    clock = pygame.time.Clock()

    # Runs game
    while flag:
        # Limits the frame rate of the application
        clock.tick(120)

        ql = qLearn(snake.dirnx, snake.dirny, applx, apply, snake.x[0], snake.y[0])


        oldx = snake.x[0]
        oldy = snake.y[0]

        # Moves the snake
        snake.move(win, ql.move())

        ql = qLearn(snake.dirnx, snake.dirny, applx, apply, snake.x[0], snake.y[0])

        ql.updateQ(oldx, oldy)

        # Adds a cube to the snake and move the apple
        if int(snake.x[0]) == applx and int(snake.y[0]) == apply:
            snake.addCube()
            applx, apply = createSnack(width, snakeSize, snake)
        
        # Draws the window
        if highScore > 0:
            redrawWindow(win, snake, apple, applx, apply, snakeSize)

        score = len(snake.x)
        if score > highScore:
            highScore = score
            print(highScore)

        # Makes sure game is responding to Mac
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                 sys.exit(0)

# Initilizes pygame
pygame.init()

# Runs the main function
main()
