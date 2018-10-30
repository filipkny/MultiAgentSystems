from Gridworld import Agent
import random
import numpy as np
import copy
import sys
from collections import defaultdict

class Gridwall(object):
    def __init__(self,walls, treasure, snake_pit,size=8, alfa=0.1, gamma = 1):
        self.size = size
        self.walls = walls
        self.treasure = treasure
        self.snake_pit = snake_pit
        self.snake_penalty = -20
        self.treasure_reward = 10
        self.default_reward = -1
        self.alfa = alfa
        self.gamma = gamma
        self.rewards =  np.zeros((size,size))
        self.policies = [[None]*size for _ in range(size)]
        self.agent = None

    def init_agent(self):
        [start_y,start_x] = self.walls[0]
        while [start_y,start_x] in self.walls:
            start_y = random.randint(0,self.size-1)
            start_x = random.randint(0,self.size-1)

        self.agent = Agent(start_y, start_x)

    def init_policies(self):
        for y in range(self.size):
            for x in range(self.size):
                policy = {'north' : 0.25,
                          'south' : 0.25,
                          'west'  : 0.25,
                          'east'  : 0.25}

                self.policies[y][x] = copy.deepcopy(policy)

    def init_returns(self):
        self.returns = []
        for y in range(self.size):
            self.returns.append([])
            for x in range(self.size):
                self.returns[y].append([])

    def check_reward(self,current_pos, bumped):
        reward = 0

        if current_pos == self.snake_pit:
            reward = self.snake_penalty
        elif current_pos == self.treasure:
            reward = self.treasure_reward
        else:
            reward = self.default_reward

        if bumped:
            return -1
        else:
            return reward

    def init_Qmat(self):
        self.Qmat = []

        for y in range(self.size):
            self.Qmat.append([])
            for x in range(self.size):
                self.Qmat[y].append({
                    'north':0,
                    'south': 0,
                    'east': 0,
                    'west': 0,
                })

        self.Qmat[self.treasure[0]][self.treasure[1]] = {
            'north': 0,
            'south': 0,
            'east': 0,
            'west': 0,
        }

        self.Qmat[self.snake_pit[0]][self.snake_pit[1]] = {
            'north': 0,
            'south': 0,
            'east': 0,
            'west': 0,
        }

    def get_tile_in_direction(self,pos, dir):
        new_pos = copy.deepcopy(pos)

        if dir == 'north':
            new_pos[0] += -1
        elif dir == 'south':
            new_pos[0] += 1
        elif dir == 'east':
            new_pos[1] += 1
        elif dir == 'west':
            new_pos[1] += -1

        return new_pos

    def print_best_policies(self):
        best_policies = []
        sum_best_policies = []
        for y in range(self.size):
            sum_best_policies.append([])
            best_policies.append([])
            for x in range(self.size):
                choices = self.Qmat[y][x]
                max_dir = None
                max_q = -sys.maxsize
                for dir in choices.keys():
                    q = choices[dir]
                    if q > max_q:
                        max_q = q
                        max_dir = dir

                best_policies[y].append(max_dir)
                sum_best_policies[y].append(round(sum(choices.values()),2))

        best_policies = np.matrix(best_policies)

        sum_best_policies = np.matrix(sum_best_policies)

        return best_policies,sum_best_policies

    def print_final_policies(self):
        best_policies, sum_best_policies = self.print_best_policies()
        for wall in walls:
            best_policies[wall[0],wall[1]] = 'WALL'
            sum_best_policies[wall[0],wall[1]] = '-1'

        best_policies[self.snake_pit[0],self.snake_pit[1]] = 'SNAKE'
        sum_best_policies[self.snake_pit[0],self.snake_pit[1]] = -0.000

        best_policies[self.treasure[0], self.treasure[1]] = 'TREASURE'
        sum_best_policies[self.treasure[0], self.treasure[1]] = -0.000

        print(best_policies)
        print(sum_best_policies)

        return self.Qmat

    def check_bump(self, pos, walls, border = 8):
        if pos not in walls and 0 <= pos[0] < border  and 0 <= pos[1] < border:
            return False
        else:
            return True

    def generate_episode(self, algorithm = 'sarsa', printing=True):

        # Initialize s
        self.init_agent()
        # Choose a from s using policy derived from Q, e-greedy
        dir = self.agent.select_e_greedily(self.agent.current_pos, self.Qmat)

        counter = 0

        # Repeat for each step
        while True:
            counter += 1
            [current_y, current_x] = self.agent.current_pos

            s_slash = self.get_tile_in_direction(self.agent.current_pos, dir)
            if printing:
                print(" --------- NEW STEP ----------")
                print("Agent at {} with dir: {} --> {}".format(self.agent.current_pos,dir,s_slash))

            # Take action a, observe reward, s'
            bumped = self.check_bump(s_slash,self.walls)
            if bumped:
                s_slash = self.agent.current_pos
            reward = self.check_reward(s_slash,bumped)


            # Choose a' from s' using policy derived from Q, e-greedy
            new_dir = self.agent.select_e_greedily(s_slash, self.Qmat)
            [new_y, new_x] = s_slash

            if algorithm == 'sarsa':
                update_dir = new_dir
                [update_y, update_x] = [new_y, new_x]
            else:
                update_dir = self.agent.select_e_greedily(s_slash, self.Qmat, e=0)
                [update_y, update_x] = s_slash


            if printing:
                print("Recieved reward {} (bumped at {}: {})".format(reward,self.agent.current_pos,bumped))


            if printing:
                print("a_slash is {}".format(new_dir))

            # Update Q
            self.Qmat[current_y][current_x][dir] += self.alfa*\
                                              (reward + self.gamma*self.Qmat[update_y][update_x][update_dir] -
                                               self.Qmat[current_y][current_x][dir])


            if printing:
                print("After updating Q for y:{} and x:{} it looks like:{}".format(current_y,current_x,self.Qmat[current_y][current_x]))
                print("Updating with {}".format(self.alfa*\
                                              (reward + self.gamma*self.Qmat[update_y][update_x][update_dir] -
                                               self.Qmat[current_y][current_x][dir])))
            dir = new_dir
            self.agent.current_pos = s_slash

            if printing:
                print("Now at {}".format(self.agent.current_pos))

            if self.agent.current_pos == self.snake_pit or self.agent.current_pos == self.treasure:
                break

walls = [[1,2],
         [1,3],
         [1,4],
         [1,5],
         [2,5],
         [3,5],
         [4,5],
         [6,1],
         [6,2],
         [6,3]]

treasure = [7,7]
snake_pit = [5,4]

world = Gridwall(walls,treasure,snake_pit)
world.init_policies()
world.init_Qmat()
for i in range(100000):
    print("Episode {}".format(i))
    world.generate_episode(algorithm='q',printing=False)
   # world.print_best_policies()

qmat = world.print_final_policies()