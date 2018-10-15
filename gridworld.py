import numpy
import copy
import time
import operator
import sys

class Agent(object):
    def __init__(self,init_y,init_x):
        self.current_pos = [init_y,init_x]
        self.reward = 0
        self.moves = {'north': [-1,0],
                      'south': [1,0],
                      'west' : [0,-1],
                      'east' : [0,1]}

    def move(self,dir):
        bump = False

        if dir == 'north':
            self.current_pos[0] += -1
        elif dir == 'south':
            self.current_pos[0] += 1
        elif dir == 'east':
            self.current_pos[1] += 1
        elif dir == 'west':
            self.current_pos[1] += -1

        if self.current_pos[0] == -1:
            self.current_pos[0] = 0
            bump = True

        if self.current_pos[0] == 5:
            self.current_pos[0] = 4
            bump = True

        if self.current_pos[1] == -1:
            self.current_pos[1] = 0
            bump = True

        if self.current_pos[1] == 5:
            self.current_pos[1] = 4
            bump = True

        return bump

    def rand_move(self):
        choice = numpy.random.choice(['north','west','east','south'])
        self.move(choice)

    def policy_move(self,policy):
        moves = list(policy.keys())
        probs = list(policy.values())
        chosen_move = numpy.random.choice(moves,1,p=probs)
        return self.move(chosen_move)

class Grid(object):
    def __init__(self,m = 5,n = 5,A = [0,1],B=[0,3],resetA=[4,1],resetB=[2,3],policy='random',gamma=1, alfa = 0.1):
        self.m = m
        self.n = n
        self.rewards = numpy.zeros((m,n))
        self.policies = [[None]*m for _ in range(n)]
        self.A = A
        self.rewardA = 10
        self.resetA = resetA
        self.B = B
        self.rewardB = 5
        self.resetB = resetB
        self.policy = policy
        self.gamma = gamma
        self.alfa = alfa
        self.agent = Agent(0,0)

    def init_policies(self):
        for y in range(self.m):
            for x in range(self.n):
                policy = {'north' : 0.25,
                          'south' : 0.25,
                          'west'  : 0.25,
                          'east'  : 0.25}

                self.policies[y][x] = copy.deepcopy(policy)

    def check_reward(self):
        if self.agent.current_pos[0] < 0:
            self.agent.reward -= 1
            self.agent.current_pos[0] = 0

        elif self.agent.current_pos[1] < 0:
            self.agent.reward -= 1
            self.agent.current_pos[1] = 0

        elif self.agent.current_pos == A:
            self.agent.reward += self.rewardA
            self.agent.current_pos = self.resetA

        elif self.agent.current_pos == B:
            self.agent.reward += self.rewardB
            self.agent.current_pos = self.resetB

    def play(self):
        if selfpolicy == 'random':
            self.agent.rand_move()

    def evaluate_policy(self):
        # Policy evaluation
        theta = 0.00000001
        delta = 1
        while delta > theta:
            for y in range(self.m):
                for x in range(self.n):
                    v = self.rewards[y][x]
                    sum = 0
                    for dir, prob in self.policies[y][x].items():
                        new_x = x + self.agent.moves[dir][1]
                        new_y = y + self.agent.moves[dir][0]
                        if [y,x] == self.A:
                            sum += prob*(self.rewardA+self.gamma*self.rewards[self.resetA[0]][self.resetA[1]])
                        elif [y,x] == self.B:
                            sum += prob*(self.rewardB+self.gamma*self.rewards[self.resetB[0]][self.resetB[1]])
                        elif 0 <= new_x < 5 and 0 <= new_y < 5:
                            sum += prob*(0 + self.gamma*self.rewards[new_y][new_x])
                        else:
                            sum += prob*(-1 + self.gamma*self.rewards[y][x])

                    self.rewards[y][x] = sum

                    delta = min(delta, abs(v - self.rewards[y][x]))

    def improve_policy(self):
        stable = False
        for y in range(self.m):
            for x in range(self.n):
                b = self.policies[y][x]
                current_policy_value = self.rewards[y][x]
                new_rewards = {}
                if [y,x] == self.A or [y,x] == self.B:
                    continue

                for dir, prob in self.policies[y][x].items():
                    new_x = x + self.agent.moves[dir][1]
                    new_y = y + self.agent.moves[dir][0]
                    if [new_y, new_x] == self.A:
                        new_reward = self.rewardA + self.gamma*self.rewards[new_y][new_x]
                    elif [new_y, new_x] == self.B:
                        new_reward = self.rewardB + self.gamma*self.rewards[new_y][new_x]
                    elif 0 <= new_x < 5 and 0 <= new_y < 5:
                        new_reward = self.gamma*self.rewards[new_y][new_x]
                    else:
                        new_reward = self.gamma*self.rewards[y][x] - 1

                    new_rewards[dir] = new_reward

                new_rewards["current"] = current_policy_value

                best_reward = -sys.maxsize
                best_dir = None
                for dir,reward in new_rewards.items():
                    if reward >= best_reward:
                        best_reward = reward
                        best_dir = dir

                #print("Best direction is {} with reward {} at x: {}  y: {}".format(best_dir, best_reward, x, y))

                new_policy = {}
                for possible_move in ['south','north','east','west']:
                    if possible_move == best_dir:
                        new_policy[possible_move] = 1
                    else:
                        new_policy[possible_move] = 0

                if new_policy != self.policies[y][x]:
                    stable = False
                    self.policies[y][x] = new_policy
                else:
                    stable = True

        if stable:
            return
        else:
            self.evaluate_policy()


    def print_policies(self):
        for i in range(len(grid.policies)):
            for j in range(len(grid.policies[0])):
                print(self.policies[i][j])

    def generate_episode(self):
        self.init_policies()
        start_x = numpy.random.choice(range(5),1)[0]
        start_y = numpy.random.choice(range(5),1)[0]
        self.agent = Agent(start_y,start_x)

        while self.agent.current_pos != self.A and self.agent.current_pos != self.B:

            [current_y,current_x ]= self.agent.current_pos
            current_policy = self.policies[current_y][current_x]

            bump = self.agent.policy_move(current_policy)
            [new_y, new_x] = self.agent.current_pos

            # if self.agent.current_pos == self.A or self.agent.current_pos == self.B:
            #     break

            reward = 0.

            if bump:
                reward = -1.

            self.rewards[current_y][current_x] += self.alfa*(reward + self.gamma*self.rewards[new_y][new_x] - self.rewards[current_y][current_x])

        if self.agent.current_pos == self.A:
            self.rewards[self.A[0]][self.A[1]] += self.alfa*(10 + self.gamma*self.rewards[self.resetA[0]][self.resetA[1]] - self.rewards[self.A[0]][self.A[1]])

        if self.agent.current_pos == self.B:
            self.rewards[self.B[0]][self.B[1]] += self.alfa*(5 + self.gamma*self.rewards[self.resetB[0]][self.resetB[1]] - self.rewards[self.B[0]][self.B[1]])



grid_policy_iteration = Grid()
# grid.init_policies()
# grid.evaluate_policy()
# print(grid.rewards)
# for i in range(100):
#     grid.improve_policy()
#
# grid.print_policies()
# print(grid.rewards)
grid_episodes= Grid()
for i in range(1000):
    grid_episodes.generate_episode()

print(grid_episodes.rewards)
