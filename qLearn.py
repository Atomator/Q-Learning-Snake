import numpy as np
import math 

qTable = np.random.rand(28, 4)
alpha = 0.3
discount = 0.5
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
            if self.y == self.apply:
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
            if self.y == self.apply:
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
            if self.y == self.apply:
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
            if self.y == self.apply:
                state = 22

            # In line with food
            elif self.x == self.applx:
                state = 23

        if self.x >= 380:
            state = 24
        elif self.y >= 380:
            state = 25
        elif self.x <= 20:
            state = 26
        elif self.y <= 20:
            state = 27

        return state
    def move(self):
        state = self.getState()
        action = np.argwhere(self.qTable[state,:] == np.amax(self.qTable[state,:]))
        return int(action[0])
    def getReward(self, oldx, oldy):
        distance_old = math.sqrt((oldx - self.applx)**2 + (oldy - self.apply)**2)
        distance = math.sqrt((self.x - self.applx)**2 + (self.y - self.apply)**2)
        reward = 0
        if self.x == self.applx and self.y == self.apply:
            reward = 1
        elif self.dirnx == 0 and self.dirny == 0:
            reward = -0.75
        elif self.x < 0 or self.x > 400 or self.y < 0 or self.y > 400:
            reward = -0.5
        elif distance_old <= distance:
            reward = -1
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
        return self.getReward(past_x, past_y)
        self.dirnx = past_dirnx
        self.dirny = past_dirny
        self.x = past_x
        self.y = past_y
    def updateQ(self, oldx, oldy):
        global qTable
        state = self.getState()
        action = self.move()
        qCurrent = self.qTable[state, action]
        if self.getReward(oldx, oldy) == -0.75:
            print(self.getReward(oldx, oldy))
        qTable[state, action] = qCurrent + alpha * ((self.getReward(oldx, oldy) + discount * self.future()) - qCurrent)

