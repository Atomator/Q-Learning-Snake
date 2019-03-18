import numpy as np
import math 

qTable = np.random.rand(24, 4)
alpha = 0.3
discount = 1
distance = 0

class qLearn(object):
    def __init__(self, dirnx, dirny, applx, apply, x, y):
        self.dirnx = dirnx
        self.dirny = dirny
        self.applx = applx
        self.apply = apply
        self.x = x
        self.y = y
        self.qTable = qTable
    def getState(self):
        state = 0
        if self.dirnx == 0 and self.dirny == 1:
            # Food is Right
            if self.x < self.applx and self.y > self.apply:
                state = 0

            # Food Is Left
            elif self.x > self.applx and self.y > self.apply:
                state = 1

            # Food Is Ahead
            elif self.y > self.apply and self.x > self.applx:
                state = 2

            # Food Is Behind
            elif self.y < self.apply and self.x > self.applx:
                state = 3
            
            # In line with food
            elif self.y == self.apply:
                state = 4

            # In line with food
            elif self.x == self.applx:
                state = 5
        elif self.dirnx == 0 and self.dirny == -1:
            # Food is Right
            if self.x < self.applx and self.y > self.apply:
                state = 6

            # Food Is Left
            elif self.x > self.applx and self.y > self.apply:
                state = 7

            # Food Is Ahead
            elif self.y > self.apply and self.x > self.applx:
                state = 8

            # Food Is Behind
            elif self.y < self.apply and self.x > self.applx:
                state = 9
            
            # In line with food
            elif self.y == self.apply:
                state = 10

            # In line with food
            elif self.x == self.applx:
                state = 11
        elif self.dirnx == -1 and self.dirny == 0:
            # Food is Right
            if self.x < self.applx and self.y > self.apply:
                state = 12

            # Food Is Left
            elif self.x > self.applx and self.y > self.apply:
                state = 13

            # Food Is Ahead
            elif self.y > self.apply and self.x > self.applx:
                state = 14

            # Food Is Behind
            elif self.y < self.apply and self.x > self.applx:
                state = 15
            
            # In line with food
            elif self.y == self.apply:
                state = 16

            # In line with food
            elif self.x == self.applx:
                state = 17
        elif self.dirnx == 1 and self.dirny == 0:
            # Food is Right
            if self.x < self.applx and self.y > self.apply:
                state = 18

            # Food Is Left
            elif self.x > self.applx and self.y > self.apply:
                state = 19

            # Food Is Ahead
            elif self.y > self.apply and self.x > self.applx:
                state = 20

            # Food Is Behind
            elif self.y < self.apply and self.x > self.applx:
                state = 21
            
            # In line with food
            elif self.y == self.apply:
                state = 22

            # In line with food
            elif self.x == self.applx:
                state = 23
        return state
    def move(self):
        state = self.getState()
        action = np.argwhere(self.qTable[state,:] == np.amax(self.qTable[state,:]))
        return action
    def getReward(self, oldx, oldy):
        distance_old = math.sqrt((oldx - self.applx)**2 + (oldy - self.apply)**2)
        distance = math.sqrt((self.x - self.applx)**2 + (self.y - self.apply)**2)
        if self.x == self.applx and self.y == self.apply:
            reward = 1
            print("got it")
        elif distance < distance_old:
            reward = 0.5
            print("less")
        else:
            reward = -1
            print("more")
        return reward
    def future(self):
        move = self.move()
        past_dirnx = self.dirnx
        past_dirny = self.dirny
        past_x = self.x
        past_y = self.y
        if move == 0:
            self.dirnx = -1
            self.dirny = 0
        elif move == 1:
            self.dirnx = 1
            self.dirny = 0
        elif move == 2:
            self.dirnx = 0
            self.dirny = -1
        elif move == 3:
            self.dirnx = 0
            self.dirny = 1
        self.x += self.dirnx
        self.y += self.dirny
        fut_state = self.getState()
        fut_action = self.move()

        self.dirnx = past_dirnx
        self.dirny = past_dirny
        self.x = past_x
        self.y = past_y
        return fut_state, fut_action
    def updateQ(self, oldx, oldy):
        global qTable
        fut_state, fut_action = self.future()
        state = self.getState()
        action = self.move()
        qCurrent = self.qTable[state, action]
        qTable[state, action] = qCurrent + alpha * (self.getReward(oldx, oldy) + discount * qTable[fut_state, fut_action] - qCurrent)

