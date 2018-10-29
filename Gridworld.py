import numpy
import copy

class Agent(object):
    def __init__(self,init_y,init_x):
        self.current_pos = [init_y,init_x]
        self.reward = 0
        self.moves = {'north': [-1,0],
                      'south': [1,0],
                      'west' : [0,-1],
                      'east' : [0,1]}

    def move(self,dir, limit = 5, walls = []):
        bump = False
        [start_y,start_x] = self.current_pos

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

        if self.current_pos[0] == limit:
            self.current_pos[0] = limit - 1
            bump = True

        if self.current_pos[1] == -1:
            self.current_pos[1] = 0
            bump = True

        if self.current_pos[1] == limit:
            self.current_pos[1] = limit - 1
            bump = True

        if self.current_pos in walls:
            self.current_pos = [start_y,start_x]
            bump = True

        # print("Moved from {} to {}".format([start_y,start_x],self.current_pos))
        return bump,dir

    def rand_move(self):
        choice = numpy.random.choice(['north','west','east','south'])
        self.move(choice)

    def policy_move(self,policy):
        moves = list(policy.keys())
        probs = list(policy.values())
        chosen_move = numpy.random.choice(moves,1,p=probs)
        return self.move(chosen_move)

class Grid(object):
    def __init__(self,m = 5,n = 5,A = [0,1],B=[0,3],resetA=[4,1],resetB=[2,3],policy='random',gamma=0.9, alfa = 0.2):
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

    def round_values(self):
        for y in range(self.m):
            for x in range(self.n):
                self.rewards[y][x] = round(self.rewards[y][x],1)

    def improve_policy(self):
        print("evaluating new policy")
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

                #new_rewards["current"] = current_policy_value

                best_reward = max(list(new_rewards.values()))
                best_dir = []
                for dir,reward in new_rewards.items():
                    if reward >= best_reward:
                        best_reward = reward
                        best_dir.append(dir)

                print("Best direction is {} with reward {} at x: {}  y: {}".format(best_dir, best_reward, x, y))

                new_policy = {}
                for possible_move in ['south','north','east','west']:
                    if possible_move in best_dir:
                        new_policy[possible_move] = 1./len(best_dir)
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
        for i in range(len(self.policies)):
            for j in range(len(self.policies[0])):
                print(self.policies[i][j])

    def init_returns(self):
        self.returns = []
        for y in range(self.m):
            self.returns.append([])
            for x in range(self.n):
                self.returns[y].append([])

    def generate_episodes(self,n):
        self.init_policies()
        self.init_returns()
        for i in range(n):
            start_x = numpy.random.choice(range(5),1)[0]
            start_y = numpy.random.choice(range(5),1)[0]
            self.agent = Agent(start_y,start_x)
            g = 0

            states = []
            actions = []
            rewards = []

            while self.agent.current_pos != self.A and self.agent.current_pos != self.B:
                states.append(tuple(self.agent.current_pos))

                [current_y,current_x ]= self.agent.current_pos
                current_policy = self.policies[current_y][current_x]

                bump, dir = self.agent.policy_move(current_policy)
                actions.append(dir)

                [new_y, new_x] = self.agent.current_pos

                if bump:
                    reward = -1.
                elif [current_y, current_x] == self.A:
                    reward = self.rewardA
                elif [current_y, current_x] == self.B:
                    reward = self.rewardB
                else:
                    reward = 0

                rewards.append(reward)

            states.append(tuple(self.agent.current_pos))

            if self.agent.current_pos == self.A:
                rewards.append(self.rewardA)
            if self.agent.current_pos == self.B:
                rewards.append(self.rewardB)

            g = 0
            for i in range(len(rewards)-1,0,-1):
                g += rewards[i]
                y = states[i][0]
                x = states[i][1]
                self.returns[y][x].append(g)
                returns = self.returns[y][x]
                self.rewards[y][x] = sum(returns)/len(returns)

# grid_policy_iteration = Grid()
# grid_policy_iteration.init_policies()
# grid_policy_iteration.evaluate_policy()
# grid_policy_iteration.round_values()
# print(grid_policy_iteration.rewards)
# for i in range(3):
#     grid_policy_iteration.improve_policy()
#     grid_policy_iteration.print_policies()
#     print(grid_policy_iteration.rewards)

# for i in range(1000):
#     grid_policy_iteration.improve_policy()
#     grid_policy_iteration.evaluate_policy()
#     print(i)
#     print(grid_policy_iteration.rewards)
#
# print(grid_policy_iteration.print_policies())

# grid_episodes= Grid()
# grid_episodes.generate_episodes(1000)
# print(grid_episodes.rewards)
# for i in range(30):
#     grid_episodes.improve_policy()
#     print("calculating new rewards")
#     grid_episodes.generate_episodes(1000)
#     print(grid_episodes.rewards)
#
#

# grid_episodes.improve_policy()
# grid_episodes.init_returns()
# print(grid_episodes.returns)