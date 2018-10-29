from Gridworld import Agent
import random
import numpy as np
import copy
import sys
import pprint

class Gridwall(object):
    def __init__(self,walls, treasure, snake_pit,size=8, alfa=0.1, gamma = 0.9):
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
        choice = {
            'north': random.uniform(0,1),
            'south': random.uniform(0,1),
            'east': random.uniform(0,1),
            'west': random.uniform(0,1),
        }

        for y in range(self.size):
            self.Qmat.append([])
            for x in range(self.size):
                self.Qmat[y].append(copy.deepcopy(choice))

    def get_possible_new_s(self, current_pos):
        [current_y, current_x] = current_pos
        possible_s = []
        dir = None
        if current_y - 1 >= 0:
            possible_s.append(([current_y - 1,current_x],'north'))
        if current_y + 1 < self.size:
            possible_s.append(([current_y + 1,current_x],'south'))
        if current_x - 1 >= 0:
            possible_s.append(([current_y ,current_x - 1],'west'))
        if current_x + 1 < self.size:
            possible_s.append(([current_y,current_x + 1],'east'))

        return possible_s

    def select_e_greedily(self, current_pos, e = 0.5):
        rand = random.uniform(0,1)
        possible_s= self.get_possible_new_s(current_pos)
        max_dir = None

        print("Possible s {}".format(possible_s))
        if rand < e:
            print("CHOOSING RANDOMLY")
            (new_s,dir) = random.choice(possible_s)
        else:
            max_q = -sys.maxsize
            max_s = [None,None]
            for s,dir in possible_s:
                y = s[0]
                x = s[1]
                choices = self.Qmat[y][x]
                q = choices[dir]
                if q > max_q:
                    max_q = q
                    max_s = s
                    max_dir  = dir

            new_s= max_s
            dir = max_dir

        return new_s,dir

    def generate_episode(self):
        self.init_Qmat()

        # Initialize s
        self.init_agent()

        # Choose a from s using policy derived from Q, e-greedy
        new_s, dir = self.select_e_greedily(self.agent.current_pos)

        from collections import defaultdict
        positions = defaultdict(int)
        count = 0

        # Repeat for each step
        while self.agent.current_pos != self.snake_pit and self.agent.current_pos != self.treasure:
            count += 1
            positions[str(self.agent.current_pos)] += 1
            # if count == 100000:
            #     pprint.pprint(positions)
            #     quit()

            [current_x, current_y] = self.agent.current_pos

            print(" --------- NEW STEP ----------")
            print("Current q: {}".format(self.Qmat[current_y][current_x]))
            print("Agent at {} with dir: {} --> {}".format(self.agent.current_pos,dir,new_s))

            # Take action a, obesrve r,s'
            bumped,dir = self.agent.move(dir, limit=self.size, walls=self.walls)

            if bumped:
                print("We bumped into {} so we are still at {}".format(new_s,self.agent.current_pos))
                new_s = [current_x, current_y]

            reward = self.check_reward(self.agent.current_pos, bumped)

            print("Recieved reward {} and currently at {} (bumped: {})".format(reward,self.agent.current_pos,bumped))

            # Choose a' from s' using policy derived from Q, e-greedy
            new_new_s,new_dir = self.select_e_greedily(self.agent.current_pos)
            print("Next move is dir: {} to go to {}".format(new_dir,new_new_s))
            [new_y,new_x] = new_new_s


            # Update Q
            self.Qmat[current_y][current_x][dir] += self.alfa*\
                                              (reward + self.gamma*self.Qmat[new_y][new_x][new_dir] -
                                               self.Qmat[current_y][current_x][dir])

            print("After updating Q for y:{} and x:{} it looks like:{}".format(current_y,current_x,self.Qmat[current_y][current_x]))
            dir = new_dir
            new_s = new_new_s

walls = [[1,1],
         [1,2],
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
for i in range(100):
    world.generate_episode()
