import math
import numpy as np
import random

# 1: Direction, 2: Right, Left, Inline, 3: Above, Below, Inline, 4: Wall or Not, 5: Actions
qTable = np.random.rand(4, 3, 3, 2, 4)
discount = 0.9
alpha = 0.3 

# Get the state variables for the snake
def getState(x, y, dirnx, dirny, applx, apply):
    direction = 0
    rigLef = 0
    belAbo = 0
    walno = 0

    if dirnx == -1 and dirny == 0:
        direction = 0
    elif dirnx == 1 and dirny == 0:
        direction = 1
    elif dirnx == 0 and dirny == -1:
        direction = 2
    elif dirnx == 0 and dirny == 1:
        direction = 3

    if x > applx:
        rigLef = 0
    elif x < applx:
        rigLef = 1
    elif x == applx:
        rigLef = 2

    if y > apply:
        belAbo = 0
    elif y < apply:
        belAbo = 1
    elif y == apply:
        belAbo = 2

    if x == 0 or x == 380 or y == 0 or y == 380:
        walno = 1
    else:
        walno = 0

    return direction, rigLef, belAbo, walno

# Gets the movement based on qTable
def howMove(x, y, dirnx, dirny, applx, apply):
    direction, rigLef, belAbo, walno = getState(x, y, dirnx, dirny, applx, apply)
    action = np.argwhere(qTable[direction, rigLef, belAbo, walno,:] == np.amax(qTable[direction, rigLef, belAbo, walno,:]))
    return action[0]

def getReward(x, y, dirnx, dirny, applx, apply, beforeX, beforeY, died):
    distance_old = math.sqrt((applx - beforeX)**2 + (apply - beforeY)**2)
    distance = math.sqrt((applx - x)**2 + (apply - y)**2)
    # print("old: " + str(distance_old))
    # print("current: " + str(distance))
    if distance_old <= distance:
        reward = -0.2
    elif x == applx and y == apply:
        reward = 10
    elif died:
        reward = -10
    else:
        reward = -0.1
    return reward

# Add apple shift
def getFuture(x, y, dirnx, dirny, applx, apply, timeRun):
    reward = 0 
    for i in range(timeRun):

        move = howMove(x, y, dirnx, dirny, applx, apply)
        died = False

        beforeX = x
        beforeY = y

        if move == 0:
            dirnx = -1
            dirny = 0
        elif move == 1:
            dirnx = 1
            dirny = 0
        elif move == 2:
            dirnx = 0
            dirny = -1
        elif move == 3:
            dirnx = 0
            dirny = 1

        x += dirnx * 20
        y += dirny * 20

        if x >= 400 or y >= 400 or x < 0 or y < 0:
            died = True

        reward += getReward(x, y, dirnx, dirny, applx, apply, beforeX, beforeY, died) 

        if died:
            x = random.randint(0,(400/20)-1) * 20
            y = random.randint(0,(400/20)-1) * 20
            dirnx = 0
            dirny = 0
            died = False

    print(reward)
    return reward

def updateQ(x, y, dirnx, dirny, applx, apply, beforeX, beforeY, died):
    global qTable
    direction, rigLef, belAbo, walno = getState(x, y, dirnx, dirny, applx, apply)
    action = howMove(x, y, dirnx, dirny, applx, apply)
    # print(getReward(x, y, dirnx, dirny, applx, apply, beforeX, beforeY, died))
    qCurrent = qTable[direction, rigLef, belAbo, walno, action]
    qTable[direction, rigLef, belAbo, walno, action] += alpha * ((getReward(x, y, dirnx, dirny, applx, apply, beforeX, beforeY, died) + discount * getFuture(x, y, dirnx, dirny, applx, apply, 3)) - qCurrent)