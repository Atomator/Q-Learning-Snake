import math
import random
import sys
import pygame

from qLearn_multi import *

class snakeOb(object):

    # Sets inital perameters
    def __init__(self, color, pos, snakeSize, width):
        self.color = color
        self.width = width
        self.snakeSize = snakeSize
        self.dirnx = 0
        self.dirny = 0
        self.cube = cube()
        self.x = [240] # [self.width/2]
        self.y = [240] # [self.width/2]

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

        self.x[0] = self.x[0] + self.dirnx * self.snakeSize
        self.y[0] = self.y[0] + self.dirny * self.snakeSize

        # Changes to position of each part of the snake
        for i in range(len(self.x)-1,0,-1):
            self.x[i] = self.x[i-1]
            self.y[i] = self.y[i-1]

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
    applx, apply = 240, 260 # createSnack(width, snakeSize, snake)
    highScore = 0
    move = 0
    died = False
    flag = True

    # Starts the clock
    clock = pygame.time.Clock()

    # Runs game
    while flag:
        # Limits the frame rate of the application
        clock.tick(60)

        move = howMove(snake.x[0], snake.y[0], snake.dirnx, snake.dirny, applx, apply)

        beforeX, beforeY, beforeDirnx, beforeDirny = snake.x, snake.y, snake.dirnx, snake.dirny

        # Moves the snake
        snake.move(win, move)

        newX = [random.randint(0,(snake.width/snake.snakeSize)-1) * snake.snakeSize]
        newY = [random.randint(0,(snake.width/snake.snakeSize)-1) * snake.snakeSize]

        # Checks to see if the snake hits a wall
        if snake.x[0] >= 400 or snake.y[0] >= 400 or snake.x[0] < 0 or snake.y[0] < 0:
            died = True

        # Checks to see if the snake has run into itself (Needs to moved)
        for i in range(len(snake.x)-1,2,-1):
            if snake.x[i] == snake.x[0] and snake.y[i] == snake.y[0]:
                died = True
                break

        updateQ(snake.x[0], snake.y[0], snake.dirnx, snake.dirny, applx, apply, beforeX[0], beforeY[0], died, move, beforeDirnx, beforeDirny)

        if died:
            snake.x = newX
            snake.y = newY
            snake.dirnx = 0
            snake.dirny = 0
            died = False

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
            print(highScore, end='\r')

        # Makes sure game is responding to Mac
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                 sys.exit(0)

# Initilizes pygame
pygame.init()

# Runs the main function
main()
