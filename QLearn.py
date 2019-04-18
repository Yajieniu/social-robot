import random
from Agent import *
import numpy as np


HUMAN_TRAINING = True



class QLearn:

    def __init__(self,  actions, epsilon=0.5, alpha=0.9, gamma=0.9):
        self.weight_r = 1
        self.weight_effect = 1
        self.weight_social = 1

        #self.q_tables =  np.zeros((9,16,4,24))
        self.q_tables = np.load("Q_table.txt.npy")
        self.q_tables[8,15] = 100
        self.epsilon = epsilon
        self.reduceRate = alpha
        self.alpha = alpha
        self.gamma = gamma
        self.actions = actions
        self.reward = -200

