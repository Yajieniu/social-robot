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