import math
import numpy as np
import random
import time

# 1: Direction, 2: Right, Left, Inline, 3: Above, Below, Inline, 4: Wall or Not, 5: Actions
qTable = np.random.rand(4, 3, 3, 2, 4)
discount = 0.6
alpha = 0.3
chance = 5
rewardTotal = 0 

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
    ep = random.randint(0, 100)
    if ep <= chance:
        action = [random.randint(0, 3)]
    else:
        direction, rigLef, belAbo, walno = getState(x, y, dirnx, dirny, applx, apply)
        action = np.argwhere(qTable[direction, rigLef, belAbo, walno,:] == np.amax(qTable[direction, rigLef, belAbo, walno,:]))
    return action[0]

def getReward(x, y, dirnx, dirny, applx, apply, beforeX, beforeY, died):
    global chance
    distance_old = math.sqrt((applx - beforeX) ** 2 + (apply - beforeY) ** 2)
    distance = math.sqrt((applx - x) ** 2 + (apply - y) ** 2)
    if x == applx and y == apply:
        reward = 1
        chance -= 1
    elif died:
        reward = -1
    elif distance_old > distance:
        reward = 0.01
    else:
        reward = -0.1
    return reward

# Add apple shift
def getFuture(x, y, dirnx, dirny, applx, apply, timeRun):
    reward = 0 
    for i in range(timeRun):
        reward_high = 0
        reward_temp = 0
        beforeX = x
        beforeY = y
        for i in range(4):
            x_temp = beforeX
            y_temp = beforeY
            died = False

            if i == 0:
                dirnx_temp = -1
                dirny_temp = 0
            elif i == 1:
                dirnx_temp = 1
                dirny_temp = 0
            elif i == 2:
                dirnx_temp = 0
                dirny_temp = -1
            elif i == 3:
                dirnx_temp = 0
                dirny_temp = 1

            x_temp = x_temp + dirnx_temp * 20
            y_temp = y_temp + dirny_temp * 20

            if x_temp >= 400 or y_temp >= 400 or x_temp < 0 or y_temp < 0:
                died = True

            reward_temp = getReward(x_temp, y_temp, dirnx_temp, dirny_temp, applx, apply, beforeX, beforeY, died)
            # print(str(i) + ': ' + str(reward_temp))

            if reward_temp > reward_high:
                reward_high = reward_temp
                x = x_temp
                y = y_temp
                dirnx = dirnx_temp
                dirny = dirny_temp

        if died:
            x = random.randint(0,(400/20)-1) * 20
            y = random.randint(0,(400/20)-1) * 20
            dirnx = 0
            dirny = 0
            died = False

        reward += reward_high

    return reward
def getFutureState(x, y, dirnx, dirny, applx, apply, timeRun):
    state = 0 
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

        direction, rigLef, belAbo, walno = getState(x, y, dirnx, dirny, applx, apply)

        state += qTable[direction, rigLef, belAbo, walno, move]

        if died:
            x = random.randint(0,(400/20)-1) * 20
            y = random.randint(0,(400/20)-1) * 20
            dirnx = 0
            dirny = 0
            died = False

    return state

def updateQ(x, y, dirnx, dirny, applx, apply, beforeX, beforeY, died, action, beforeDirnx, beforeDirny):
    global qTable, rewardTotal
    direction, rigLef, belAbo, walno = getState(beforeX, beforeY, beforeDirnx, beforeDirny, applx, apply)
    qCurrent = qTable[direction, rigLef, belAbo, walno, action]
    # qTable[direction, rigLef, belAbo, walno, action] += (1 - alpha) * qCurrent + alpha * (getReward(x, y, dirnx, dirny, applx, apply, beforeX, beforeY, died) + discount * getFuture(x, y, dirnx, dirny, applx, apply, 3))
    qTable[direction, rigLef, belAbo, walno, action] += alpha * getReward(x, y, dirnx, dirny, applx, apply, beforeX, beforeY, died)
    rewardTotal += getReward(x, y, dirnx, dirny, applx, apply, beforeX, beforeY, died)