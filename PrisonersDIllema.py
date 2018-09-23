import random

class Player(object):
    def __init__(self, id, strat = 'random'):
        self.id = id
        self.points = 0
        self.plays = ['0','1']
        self.memory_self = []
        self.memory_opponent = []
        self.game_matrix = {}
        self.strat = strat # random, adjust to previous, adjust to average

    # Matrix has format
    #   _ 0______1__
    # 0 |a,a  |  b,c|
    #   |-----------|
    # 1 |c,b  |  d,d|
    #   -------------
    def learn_game(self, a, b, c, d):
        # First play is self, second is opponent
        self.game_matrix = {
            '0': {'0': a,
                  '1': b,},
            '1': {'0': c,
                  '1': d,},
        }

    def play(self):
        play = None

        if self.strat == 'random':
            play = self.rand_play()
        elif self.strat == 'adjust_prev':
            play = self.adjust_prev()
        elif self.strat == 'adjust_avg':
            play = self.adjust_avg()
        elif self.strat == 'adjust_avg_sloppy':
            play = self.adjust_avg_sloppy()
        elif self.strat == 'optimal':
            pass

        self.remember_self_play(play)
        return play

    def remember_self_play(self, play):
        self.memory_self.append(play)

    def rand_play(self):
        play = random.choice(self.plays)
        return play

    def adjust_prev(self):
        try:
            opp_last_play = self.memory_opponent[-1]
            if self.game_matrix['0'][opp_last_play] > self.game_matrix['1'][opp_last_play]:
                return '0'
            else:
                return '1'
        except IndexError:
            return self.rand_play()

    def adjust_avg(self):
        if self.memory_opponent.count('0') > self.memory_opponent.count('1'):
            most_prob_play = '0'
        else:
            most_prob_play = '1'

        if self.game_matrix['0'][most_prob_play] > self.game_matrix['1'][most_prob_play]:
            return '0'
        else:
            return '1'

    def adjust_avg_sloppy(self):
        if random.randint(1,20) == 1:
            print("sloppy")
            return self.rand_play()
        else:
            return self.adjust_avg()

    def observe_play(self, play):
        self.memory_opponent.append(play)

    def increment_score(self, self_play, opp_play):
        win = self.game_matrix[self_play][opp_play]
        print('Player{} wins {} points'.format(self.id,win))
        self.points += win

class NFgame(object):
    def __init__(self, a, b, c, d):
        self.a = a
        self.b = b
        self.c = c
        self.d = d
        self.player1 = Player(1,'adjust_avg_sloppy')
        self.player2 = Player(2,'random')
        self.player1.learn_game(a,b,c,d)
        self.player2.learn_game(a,b,c,d)

    def play_turn(self):
        # Both players play
        p1_choice = self.player1.play()
        p2_choice = self.player2.play()

        print('P1 plays:{} , P2 plays:{}'.format(p1_choice,p2_choice))

        # Both players observe the action
        self.player1.observe_play(p2_choice)
        self.player2.observe_play(p1_choice)

        # Both players win points
        self.player1.increment_score(p1_choice,p2_choice)
        self.player2.increment_score(p2_choice, p1_choice)

        print('P1 with {} points. P2 with {} points'.format(self.player1.points, self.player2.points))

game = NFgame(10,2,25,8)
for i in range(500):
    game.play_turn()






