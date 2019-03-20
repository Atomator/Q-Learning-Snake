import numpy as np

# 1: Direction, 2: Right, Left, Inline, 3: Above, Below, Inline, 4: Wall or Not, 5: Actions
qTable = np.random.rand(4, 3, 3, 2, 4)
discount = 0.9
alpha = 0.1 

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

    if x <= 0 or x >= 380 or y <= 0 or y >= 380:
        walno = 1
    else:
        walno = 0

    return direction, rigLef, belAbo, walno

# Gets the movement based on qTable
def howMove(x, y, dirnx, dirny, applx, apply):
    direction, rigLef, belAbo, walno = getState(x, y, dirnx, dirny, applx, apply)
    action = np.argwhere(qTable[direction, rigLef, belAbo, walno,:] == np.amax(qTable[direction, rigLef, belAbo, walno,:]))
    return action[0]

def getReward(x, y, dirnx, dirny, applx, apply):
    if x == applx and y == apply:
        reward = 1
    elif dirnx == 0 and dirny == 0:
        reward = -1
    else:
        reward = 0.1
    return reward

# Add apple shift
def getFuture(x, y, dirnx, dirny, applx, apply):
    move = 0
    move = howMove(x, y, dirnx, dirny, applx, apply)
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
    return getReward(x, y, dirnx, dirny, applx, apply)

def updateQ(x, y, dirnx, dirny, applx, apply):
    global qTable
    direction, rigLef, belAbo, walno = getState(x, y, dirnx, dirny, applx, apply)
    action = howMove(x, y, dirnx, dirny, applx, apply)
    qCurrent = qTable[direction, rigLef, belAbo, walno, action]
    qTable[direction, rigLef, belAbo, walno, action] += alpha * ((getReward(x, y, dirnx, dirny, applx, apply) + discount * getFuture(x, y, dirnx, dirny, applx, apply)) - qCurrent)