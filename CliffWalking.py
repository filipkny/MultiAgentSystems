import numpy
import random
import copy

class CliffWorld(object):
    def __init__(self):
        self.startState = [5, 0]
        self.cliffStates = [[5, 1], [5, 2], [5, 3], [5, 4], [5, 5], [5, 6], [5, 7], [5, 8]]
        self.cliffReward = -100
        self.goalState = [5, 9]
        self.goalReward = 10
        self.accumulatedReward = 0
        self.transitionCost = -1
        self.policy = [[None]*10]*6 # [row][column]
        self.currentPosition = self.startState
        self.terminated = False
        self.qValue = [[None]*10]*6
        self.initPolicyRandom()
        self.initQvalues()
        self.alpha = 0.5

    def initPolicyRandom(self):
        for i in range(6):
            for j in range(10):
                self.policy[i][j] = {
                    "north" : 0.25,
                    "east" : 0.25,
                    "south" : 0.25,
                    "west" : 0.25
                }
    def initQvalues(self):
        for i in range(6):
            for j in range(10):
                temporary = {"north" : i,
                    "east" : j,
                    "south" : 0,
                    "west" : 0}
                self.qValue[i][j] = copy.deepcopy(temporary)

    def policyMove(self):
        directions = list(self.policy[self.currentPosition[0]][self.currentPosition[1]].keys())
        probabilities = list(self.policy[self.currentPosition[0]][self.currentPosition[1]].values())
        pMove = numpy.random.choice(directions, 1, p=probabilities)
        return pMove[0]

    def getOptimalQ(self, position):
        currentBest = -10000000
        equals = []
        currentDirection = ""
        for direction, value in list(self.qValue[position[0]][position[1]].items()):
            if value >= currentBest:
                currentBest = value
                currentDirection = direction
                equals.append([direction, value])
        if len(equals) > 1:
            return random.choice(equals)
        else:
            return [currentDirection, currentBest]

    def move(self, direction):
        if direction == "north":
            if self.currentPosition[0] == 0:
                return
            self.currentPosition = [self.currentPosition[0] - 1, self.currentPosition[1]]

        elif direction == "east":
            if self.currentPosition[1] == 9:
                return
            self.currentPosition = [self.currentPosition[0], self.currentPosition[1] + 1]

        elif direction == "south":
            if self.currentPosition[0] == 5:
                return
            self.currentPosition = [self.currentPosition[0] + 1, self.currentPosition[1]]

        elif direction == "west":
            if self.currentPosition[1] == 0:
                return
            self.currentPosition = [self.currentPosition[0], self.currentPosition[1] - 1]

    def playEpisode(self):
        self.currentPosition = self.startState
        while not self.terminated:
            previousPosition = [self.currentPosition[0], self.currentPosition[1]]
            direction = self.policyMove()
            self.move(direction) # updates currentPosition!
            print(previousPosition)
            print(self.currentPosition)
            reward = -1
            if self.currentPosition in self.cliffStates:
                reward = -100
                self.terminated = True
            elif self.currentPosition == self.goalState:
                reward = 10
                self.terminated = True
            self.accumulatedReward += reward

            print(previousPosition[0])
            print(previousPosition[1])
            print(direction)

            for row in range(6):
                for column in range(10):
                    print("[" + str(row) + ", " + str(column) + "] :" + str(example.qValue[row][column]))
            print(self.qValue[3][1])
            self.qValue[3][1].update(north = 3) # Why does this update all [x][1] with north = 3?!
            #self.qValue[previousPosition[0]][previousPosition[1]][direction] = self.qValue[previousPosition[0]][previousPosition[1]][direction] +  self.alpha * (reward + self.getOptimalQ(self.currentPosition)[1] - self.qValue[previousPosition[0]][previousPosition[1]][direction])

            for row in range(6):
                for column in range(10):
                    print("[" + str(row) + ", " + str(column) + "] :" + str(example.qValue[row][column]))

    def QLearning(self):
        for episode in range(1):
            self.terminated = False
            self.accumulatedReward = 0
            self.playEpisode()


example = CliffWorld()
example.QLearning()
print("final q values")
print(example.qValue)