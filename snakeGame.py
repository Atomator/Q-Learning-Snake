import math
import random
import sys
import pygame

# For Machine Learning
from neuralNetwork import *
import numpy as np

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
        self.NNY = 0
        self.Human = True

    # Responsible for movement of the snake
    def move(self, surface, whereMove):
        # Used to make sure the Mac thinks the program is responding

        # Checks for an event every clock tick then loops through events to see if a pygame.QUIT is called
        for event in pygame.event.get():
            # If this event is called, it quits the program
            if event.type == pygame.QUIT:
                pygame.quit()

            # This in an array that has 1s or 0s depending on whether a key was pressed
            keys = pygame.key.get_pressed()

            for key in keys:
                if keys[pygame.K_RETURN]:
                    self.Human = not self.Human

            for key in keys:
                if self.Human == True:
                    if keys[pygame.K_LEFT] and (self.dirnx != 1 or self.dirny != 0):
                        self.dirnx = -1
                        self.dirny = 0
                        self.NNY = 1
                    elif keys[pygame.K_RIGHT] and (self.dirnx != -1 or self.dirny != 0):
                        self.dirnx = 1
                        self.dirny = 0
                        self.NNY = 2
                    elif keys[pygame.K_UP] and (self.dirnx != 0 or self.dirny != 1):
                        self.dirnx = 0
                        self.dirny = -1
                        self.NNY = 3
                    elif keys[pygame.K_DOWN] and (self.dirnx != 0 or self.dirny != -1):
                        self.dirnx = 0
                        self.dirny = 1
                        self.NNY = 4
                    else:
                        self.NNY = 0
                else:
                    if whereMove == 1:
                        self.dirnx = -1
                        self.dirny = 0
                    elif whereMove == 2:
                        self.dirnx = 1
                        self.dirny = 0
                    elif whereMove == 3:
                        self.dirnx = 0
                        self.dirny = -1
                    elif whereMove == 4:
                        self.dirnx = 0
                        self.dirny = 1

        # Checks to see if the snake is off the screen, the moves it to ther other side if it is
        if self.x[0] > self.width - self.snakeSize:
            self.x[0] = 0
        elif self.y[0] > self.width - self.snakeSize:
            self.y[0] = 0
        elif self.x[0] < 0:
            self.x[0] = self.width - self.snakeSize
        elif self.y[0] < 0:
            self.y[0] = self.width - self.snakeSize
        else:
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
def redrawWindow(surface, s, a, applx, apply, snakeSize, score):
    surface.fill((0,0,0))
    s.drawSnake(surface)
    a.draw(surface, applx, apply, snakeSize, (255,0,0))
    surface.blit(score,(0,0))
    pygame.display.update()

def getVariables(snake, applx, apply):
    X = np.array([(0, 0, 0, 0, 0, 0, 0, 0)])

    if snake.dirnx == 0 and snake.dirny == 1:
        X[:,0] = 1
    elif snake.dirnx == 0 and snake.dirny == -1:
        X[:,1] = 1
    elif snake.dirnx == 1 and snake.dirny == 0:
        X[:,2] = 1
    elif snake.dirnx == -1 and snake.dirny == 0:
        X[:,3] = 1

    # Food Is Right
    if snake.x[0] < applx:
        X[:,4] = 1

    # Food Is Left
    if snake.x[0] > applx:
        X[:,5] = 1

    # Food Is Ahead
    if snake.y[0] > apply:
        X[:,6] = 1

    # Food Is Behind
    if snake.y[0] < apply:
        X[:,7] = 1

    y = snake.NNY

    return X, y

def nnTrain(time,weights1, weights2, X, y):
    output, weights1, weights2 = NN(time, X, y, weights1, weights2, 5)
    Y = np.zeros(5)
    Y[y] = 1
    print(predict(output, y))
    return weights1, weights2


def nnOuput(X, w1, w2, y):
    output, _, _, _ = feedForward(X, w1, w2)
    print(predict(output, y))
    return predict(output, y)

# Main function that creates base objects and loops through objects and functions
def main():

    # Initilizes pygame
    pygame.init()  

    pygame.font.init()
    myfont = pygame.font.SysFont('Avenir', 30) 

    # Initial parameters
    width = 400
    snakeSize = 20
    win = pygame.display.set_mode((width , width))
    snake = snakeOb((0,255,0), (250,250), snakeSize, width)
    apple = cube()
    applx, apply = createSnack(width, snakeSize, snake)
    weights1 = np.random.rand(hidden_layer_nodes, 8) * (2 * epsilon) - epsilon
    weights2 = np.random.rand(5, hidden_layer_nodes + 1) * (2 * epsilon) - epsilon
    whereMove = 0
    X = np.array([(0, 0, 0, 0, 0, 0, 0, 0)])
    y = []
    flag = True

    # Starts the clock
    clock = pygame.time.Clock()

    # Runs game
    while flag:
        # Limits the frame rate of the application
        clock.tick(10)
        # Moves the snake

        X_temp, y_temp = getVariables(snake, applx, apply)

        # if snake.Human and ((snake.dirnx == 0 and snake.dirny == 0) == False):
        #     weights1,  weights2 = nnTrain(50, weights1, weights2, X, y)
        # elif snake.Human == False:
        #     whereMove = nnOuput(X, weights1, weights2, y)

        snake.move(win, whereMove)

        score = myfont.render(str(len(snake.x)), True, (255, 255, 255))

        # Adds a cube to the snake and move the apple
        if snake.x[0] == applx and snake.y[0] == apply:
            snake.addCube()
            applx, apply = createSnack(width, snakeSize, snake)

        # Checks to see if the snake has run into itself (Needs to moved)
        for i in range(len(snake.x)-1,2,-1):
            if snake.x[i] == snake.x[0] and snake.y[i] == snake.y[0]:
                snake.x = [240]
                snake.y = [240]
                snake.dirnx = 0
                snake.dirny = 0
                break

        # Draws the window
        redrawWindow(win, snake, apple, applx, apply, snakeSize, score)

        # Makes sure game is responding to Mac
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                 sys.exit(0)

# Runs the main function
main()