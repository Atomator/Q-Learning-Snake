import math
import numpy as np
import random

# Multi-Dimentional qTable
# 1: Direction, 2: Right, Left, Inline, 3: Above, Below, Inline, 4: Wall or Not, 5: Actions
qTable = np.random.rand(4, 3, 3, 2, 15, 4)

# Learning Rate
alpha = 0.3

# Get the state variables for the snake
def getState(x, y, dirnx, dirny, applx, apply):
    # Variables for each part of the state
    direction = 0
    rigLef = 0
    belAbo = 0
    walno = 0
    inFront = 0

    # Sets the direction
    if dirnx == -1 and dirny == 0:
        direction = 0
    elif dirnx == 1 and dirny == 0:
        direction = 1
    elif dirnx == 0 and dirny == -1:
        direction = 2
    elif dirnx == 0 and dirny == 1:
        direction = 3

    # Sets the X relative to the Apple
    if x[0] > applx:
        rigLef = 0
    elif x[0] < applx:
        rigLef = 1
    elif x[0] == applx:
        rigLef = 2

    # Sets the Y relative to the Apple
    if y[0] > apply:
        belAbo = 0
    elif y[0] < apply:
        belAbo = 1
    elif y[0] == apply:
        belAbo = 2

    # Tells the snake if it is close to a wall
    if x[0] == 0 or x[0] == 380 or y[0] == 0 or y[0] == 380:
        walno = 1
    else:
        walno = 0

    # If a part of the snake is near itself
    for i in range(len(x)-1, 2, -1):
        if x[i] == x[0] + 20 and y[i] == y[0] and inFront != 1:
            inFront += 1
        if y[i] == y[0] + 20 and x[i] == x[0] and inFront != 2:
            inFront += 2 
        if x[i] == x[0] - 20 and y[i] == y[0] and inFront != 4:
            inFront += 4
        if y[i] == y[0] - 20 and x[i] == x[0] and inFront != 8:
            inFront += 8


    return direction, rigLef, belAbo, walno, inFront

# Gets the movement based on qTable
def howMove(x, y, dirnx, dirny, applx, apply):
    # Gets the states
    direction, rigLef, belAbo, walno, inFront = getState(x, y, dirnx, dirny, applx, apply)

    # Finds action relative to state
    action = np.argwhere(qTable[direction, rigLef, belAbo, walno, inFront, :] == np.amax(qTable[direction, rigLef, belAbo, walno, inFront, :]))

    return action[0]

# Find the reward based on current state
def getReward(x, y, dirnx, dirny, applx, apply, beforeX, beforeY, died):
    # Sets the previous and current distance from apple
    distance_old = math.sqrt((applx - beforeX[0]) ** 2 + (apply - beforeY[0]) ** 2)
    distance = math.sqrt((applx - x[0]) ** 2 + (apply - y[0]) ** 2)

    # Eats the apple
    if x[0] == applx and y[0] == apply:
        reward = 10
    
    # Snake died
    elif died:
        reward = -10

    # Got closer to the apple
    elif distance_old <= distance:
        reward = -1

    # # When the snake is close to itself
    # elif distance_old <= distance:
    #     reward = -1
    
    # Moves
    else:
        reward = 0
    return reward

# Updates qTable
def updateQ(x, y, dirnx, dirny, applx, apply, beforeX, beforeY, died, action, beforeDirnx, beforeDirny):
    global qTable
    # Gets state before movement
    direction, rigLef, belAbo, walno, inFront = getState(beforeX, beforeY, beforeDirnx, beforeDirny, applx, apply)

    # Updates the action associtated previous state based on reward from current state
    qTable[direction, rigLef, belAbo, walno, inFront, action] += alpha * (getReward(x, y, dirnx, dirny, applx, apply, beforeX, beforeY, died))