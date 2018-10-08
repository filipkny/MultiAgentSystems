import numpy
import matplotlib.pyplot as plt
from operator import attrgetter
import copy

class Distribution(object):
    def __init__(self, mean, std_dev):
        self.mean = mean
        self.std_dev = std_dev
        self.history = []
        self.times_chosen = 0
        self.expectancy = 0
        self.ucb_score = 0

    def __str__(self):
        return "slot with mean: {}, std dev: {} and expectancy: {}".format(self.mean, self.std_dev,self.expectancy)

    def draw(self):
        result = numpy.random.normal(self.mean,self.std_dev)
        self.history.append(result)
        self.times_chosen += 1
        return result

    def update_expectancy(self):
        self.expectancy = sum(self.history)/len(self.history)

    def update_ucb(self,c,t):
        self.update_expectancy()
        self.ucb_score = self.expectancy + c*numpy.sqrt(numpy.log(t)/(2*self.times_chosen))


class Bandit(object):
    def __init__(self,num_arms, strat, slots , e = 0.1):
        self.score = 0
        self.k = num_arms
        self.slots = slots
        self.e = e
        for slot in self.slots:
            if strat == "optimistic":
                slot.history.append(20 + numpy.random.uniform())
            else:
                slot.history.append(0)

            slot.update_expectancy()

            print("Creating " + str(slot))

        self.strat = strat
        self.scores = []
        self.avg_rewards = []

    def play(self):
        if self.strat == "e-greedy" or self.strat=="greedy":
            if numpy.random.uniform() < self.e:
                print("playing randomly")
                slot = numpy.random.randint(0,self.k)
            else:
                slot = self.slots.index(max(self.slots,key=attrgetter("expectancy")))

        elif self.strat == "optimistic":
            best_slot = max(self.slots, key=attrgetter("expectancy"))
            slot = self.slots.index(best_slot)

        elif self.strat == "UCB":
            best_slot = max(self.slots, key=attrgetter("ucb_score"))
            slot = self.slots.index(best_slot)

        print("Playing " + str(self.slots[slot]))

        self.play_slot(slot)
        self.update_ucb_scores()

    def update_ucb_scores(self, c = 2):
        for slot in self.slots:
            slot.update_ucb(c,len(self.avg_rewards))

    def play_slot(self,slot):
        slot = self.slots[slot]
        win = slot.draw()
        self.score += win
        self.scores.append(self.score)
        self.avg_rewards.append(self.score/len(self.scores))
        slot.update_expectancy()

def make_slots( k):
    slots = []
    for i in range(k):
        slot = Distribution(numpy.random.randint(0, 10), numpy.random.uniform())
        slots.append(slot)

    return slots

k = 20
slots = make_slots(k)
greedy = Bandit(k,"e-greedy", copy.deepcopy(slots), e = 0)
e_greedy = Bandit(k,"e-greedy",copy.deepcopy(slots))
optimistic = Bandit(k,"optimistic",copy.deepcopy(slots))
ucb = Bandit(k,"UCB",copy.deepcopy(slots))

rounds = 500
for i in range(rounds):
    greedy.play()
    ucb.play()
    e_greedy.play()
    optimistic.play()


plt.plot(range(rounds),greedy.avg_rewards, label = "greedy")
plt.plot(range(rounds),e_greedy.avg_rewards, label='e_greedy')
plt.plot(range(rounds),optimistic.avg_rewards, label='optimistic')
plt.plot(range(rounds),ucb.avg_rewards, label='ucb')
plt.legend()
plt.grid()
plt.show()

