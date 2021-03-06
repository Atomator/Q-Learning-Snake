
import math
import random
import pygame

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

        # Moves the snake
        self.x[0] = self.x[0] + self.dirnx * self.snakeSize
        self.y[0] = self.y[0] + self.dirny * self.snakeSize

        # Changes to position of each part of the snake
        for i in range(len(self.x)-1,0,-1):
            self.x[i] = self.x[i-1]
            self.y[i] = self.y[i-1]

    # Function to add a cube to the snake
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

# Redraws the window with the snake, apple and different scores
def redrawWindow(surface, s, a, applx, apply, snakeSize, score, higherScore, gamesPlayed, avg):
    surface.fill((255,255,255))
    s.drawSnake(surface)
    a.draw(surface, applx, apply, snakeSize, (205,92,92))
    surface.blit(score,(5,5))
    surface.blit(higherScore,(5,25))
    surface.blit(gamesPlayed,(5,45))
    surface.blit(avg,(5,65))
    pygame.display.update()

# Main function that creates base objects and loops through objects and functions
def main():

    # Initilizes pygame
    pygame.init()

    # Starts the font
    pygame.font.init()
    myfont = pygame.font.SysFont('Avenir', 25) 


    # Initial parameters
    width = 400
    snakeSize = 20
    win = pygame.display.set_mode((width , width))
    snake = snakeOb((65,105,225), (250,250), snakeSize, width)
    apple = cube()
    applx, apply = 240, 260 # createSnack(width, snakeSize, snake)
    highScore = 0
    died = False
    flag = True
    games = 0
    avgScore = 0
    totalScore = 0
    speed = 10

    # Starts the clock
    clock = pygame.time.Clock()

    # Runs game
    while flag:

        # Limits the frame rate of the application
        clock.tick(speed)

        # Moves the snake
        snake.move(win)

        # Checks to see if the snake hits a wall
        if snake.x[0] >= 400 or snake.y[0] >= 400 or snake.x[0] < 0 or snake.y[0] < 0:
            died = True

        # Checks to see if the snake has run into itself
        for i in range(len(snake.x) - 1, 2, -1):
            if snake.x[i] == snake.x[0] and snake.y[i] == snake.y[0]:
                died = True
                break

        # Resets the snake upon death
        if died:
            snake.x = [random.randint(0,(snake.width/snake.snakeSize)-1) * snake.snakeSize]
            snake.y = [random.randint(0,(snake.width/snake.snakeSize)-1) * snake.snakeSize]
            snake.dirnx = 0
            snake.dirny = 0
            games += 1
            totalScore += score 
            avgScore = totalScore / games
            score = 0
            died = False

        # Adds a cube to the snake and move the apple
        if snake.x[0] == applx and snake.y[0] == apply:
            snake.addCube()
            applx, apply = createSnack(width, snakeSize, snake)

        # Tracks the high score
        score = len(snake.x)
        if score > highScore:
            highScore = score

        # Creates the fonts for each score item
        scoreCurrent = myfont.render("Current: " + str(score), True, (20, 20, 20))
        higherScore = myfont.render("High: " + str(highScore), True, (20, 20, 20))
        avg = myfont.render("Average Score: " + str(avgScore), True, (20, 20, 20))
        gamesPlayed = myfont.render("Games: " + str(games), True, (20, 20, 20))

        # Draws the windows
        redrawWindow(win, snake, apple, applx, apply, snakeSize, scoreCurrent, higherScore, gamesPlayed, avg)

        # Makes sure game is responding to Mac
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                 sys.exit(0)

# Runs the main function
main()