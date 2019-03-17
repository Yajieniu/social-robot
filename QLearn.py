import random
from Agent import *
import pickle

REWARD = 0
EFFECTIVENESS = 1
SOCIAL = 2

class QLearn:
	def __init__(self, game, actions, epsilon=0.5, alpha=0.2, gamma=0.9):
		self.game = game
		self.weight_r = 1
		self.weight_effect = 1
		self.weight_social = 1
		self.weights = {REWARD: self.weight_r,
						EFFECTIVENESS: self.weight_effect,
						SOCIAL: self.weight_social}

		self.epsilon = epsilon
		self.reduceRate = 0
        self.alpha = alpha
        self.gamma = gamma
        self.actions = actions

    # get a single q value from 
    def getQ(self, states, action):
    	q = 0
    	for state in states:
    		key = (state[0], action)
    		q += self.q_tables.get(key, 0.0)
    	return q

    def getQSingle(self, state, action, agent):
        if not state:
            key = ((),action)
        else:
            key = (state[0], action)
        q = self.q_tables[agent].get(key, 0.0)
        # print('getQsingle', q)
        return q

    def learn(self):
        maxqnew = max([self.getQSingle(state, a) for a in self.actions])
        self.updateQ(mstate1, action, reward, reward + self.gamma*maxqnew)


    def updateQ(self, state, action, reward, value, agent):
        # print('updateQ', state)
        if not state:
            key = ((), action)
        else:
            # state = state[0]
            key = (state, action)

        oldv = self.q_tables[agent].get(key, None)
        if oldv is None:
            self.q_tables[agent][key] = reward
        else:
            newq = oldv + self.alpha * (value - oldv)
            if newq < 0.0001:
                newq = 0
            self.q_tables[agent][key] = newq


    def chooseAction(self, state, actions):
        # print('choose action')
        if random.random() < self.epsilon:  # a small chance that action is chose randomly
            self.reduceRate += 1
            if self.epsilon > 0.01 and self.reduceRate == 50:
                self.epsilon -= 0.001
                self.reduceRate = 0
            action = random.choice(actions)
        else:
            q = [self.getQ(state, a) for a in actions] 
            # print(q, actions)

            maxQ = max(q)
            count = q.count(maxQ)
            if count > 1:
                best = [i for i in range(len(actions)) if q[i] == maxQ]
                i = random.choice(best)
            else:
                i = q.index(maxQ)

            action = actions[i]
        return action
















