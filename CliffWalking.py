import numpy
import random

class CliffWorld(object):
    def __init__(self):
        self.startState = [5, 0]
        self.cliffStates = [[5, 1], [5, 2], [5, 3], [5, 4], [5, 5], [5, 6], [5, 7], [5, 8]]
        self.cliffReward = -100
        self.goalState = [5, 9]
        self.goalReward = 10
        self.accumulatedReward = 0
        self.transitionCost = -1
        self.currentPosition = self.startState
        self.terminated = False
        self.qValue = [[None for _ in range(10)] for _ in range(6)]
        self.initQvalues()
        self.alpha = 0.5

    def initQvalues(self):
        for i in range(6):
            for j in range(10):
                self.qValue[i][j] = {
                    "north" : 0,
                    "east" : 0,
                    "south" : 0,
                    "west" : 0
                }

    def e_greedy(self, position):
        directions = list(self.qValue[position[0]][position[1]].keys())
        equiprobablePolicy = [0.25, 0.25, 0.25, 0.25]
        if numpy.random.choice(10, 1)[0] == 1:
            chosenDirection = numpy.random.choice(directions, 1, p=equiprobablePolicy)[0]
            return [chosenDirection, self.qValue[position[0]][position[1]][chosenDirection]]
        else:
            return self.getOptimalQ(position)

    def getOptimalQ(self, position):
        currentBest = -10000000
        equals = []
        currentDirection = ""
        for direction, value in list(self.qValue[position[0]][position[1]].items()):
            if value > currentBest:
                currentBest = value
                currentDirection = direction
        for direction, value in list(self.qValue[position[0]][position[1]].items()):
            if value == currentBest:
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

    def printOptimalPolicy(self):
        for row in range(6):
            line_print = "["
            for column in range(10):
                currentBest = -1000000
                direction = ""
                for pair in self.qValue[row][column].items():
                    if currentBest < pair[1]:
                        currentBest = pair[1]
                        direction = pair[0]
                if currentBest == 0:
                    direction = "-"
                line_print += direction + ", "
            print(line_print + "]")

    def playEpisode(self):
        self.currentPosition = self.startState
        e_greedy_move_onwards = self.e_greedy(self.currentPosition)

        while not self.terminated:
            previousPosition = [self.currentPosition[0], self.currentPosition[1]]
            #For SARSA (updated a' from previous run)
            #direction = e_greedy_move_onwards[0]

            #For Q-Learning
            direction = self.e_greedy(self.currentPosition)[0]
            self.move(direction) # updates currentPosition!
            reward = self.transitionCost
            if self.currentPosition in self.cliffStates:
                reward = self.cliffReward
                self.terminated = True
            elif self.currentPosition == self.goalState:
                reward = self.goalReward
                self.terminated = True
            self.accumulatedReward += reward

            #Q-LEARNING
            self.qValue[previousPosition[0]][previousPosition[1]][direction] += self.alpha * (reward + self.getOptimalQ(self.currentPosition)[1] - self.qValue[previousPosition[0]][previousPosition[1]][direction])

            #SARSA
            #e_greedy_move_onwards = self.e_greedy(self.currentPosition)
            #self.qValue[previousPosition[0]][previousPosition[1]][direction] += self.alpha * (reward + e_greedy_move_onwards[1] - self.qValue[previousPosition[0]][previousPosition[1]][direction])

    def QLearning(self):
        for episode in range(5000):
            self.terminated = False
            self.accumulatedReward = 0
            self.playEpisode()


example = CliffWorld()
example.QLearning()
# Use this to print the final grid state by state
# for row in range(6):
#     for column in range(10):
#         print("[" + str(row) + ", " + str(column) + "] :" + str(example.qValue[row][column]))
example.printOptimalPolicy()