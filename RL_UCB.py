import numpy
import matplotlib.pyplot as plt
from operator import attrgetter

class Distribution(object):
    def __init__(self, mean, std_dev):
        self.mean = mean
        self.std_dev = std_dev
        self.history = []
        self.expectancy = 0

    def draw(self):
        result = numpy.random.normal(self.mean,self.std_dev)
        self.history.append(result)
        return result

    def update_expectancy(self):
        self.expectancy = sum(self.history)/len(self.history)

class Bandit(object):
    def __init__(self,num_arms, strat):
        self.score = 0
        self.k = num_arms
        self.slots = []
        self.strat = strat
        for i in range(self.k):
            slot = Distribution(numpy.random.randint(0,10),numpy.random.uniform())
            self.slots.append(slot)
            if self.strat == "optimistic":
                slot.history.append(1000 + numpy.random.uniform())
            else:
                slot.history.append(0)

        self.scores = []
        self.avg_rewards = []

    def play(self, e = 0.1):
        if self.strat == "e-greedy":
            if numpy.random.uniform() < e:
                slot = numpy.random.randint(0,self.k)
            else:
                slot = self.slots.index(max(self.slots,key=attrgetter("expectancy")))

        elif self.strat == "greedy" or self.strat == "optimistic":
            slot = self.slots.index(max(self.slots, key=attrgetter("expectancy")))

        self.play_slot(slot)

    def play_slot(self,slot):
        slot = self.slots[slot]
        win = slot.draw()
        self.score += win
        self.scores.append(self.score)
        self.avg_rewards.append(self.score/len(self.scores))
        slot.update_expectancy()

k = 10
greedy = Bandit(k,"greedy")
e_greedy = Bandit(k,"e-greedy")
optimistic = Bandit(k,"optimistic")

rounds = 1000
for i in range(rounds):
    greedy.play()
    e_greedy.play()
    optimistic.play()


plt.plot(range(rounds),greedy.avg_rewards,label='greedy')
plt.plot(range(rounds),e_greedy.avg_rewards, label='e_greedy')
plt.plot(range(rounds),optimistic.avg_rewards, label='optimistic')
plt.legend()
plt.show()

