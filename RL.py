import numpy as np
import math
import random

class QLearn:

    def __init__(self, keypoints,adj,costs,reward,mode,time_slot, goal,finalQ, epsilon=0.5, alpha=0.9, gamma=0.9):

        self.effect_q_table = {}
        self.social_q_table = {}
        self.total_q_table = {}
        self.keypoints = keypoints
        self.adj = adj
        self.initialize_q_table()
        self.reward = reward
        self.mode = mode
        #This means how many time slot we choose to have for each hour
        self.time_slot = time_slot
        self.time_len = 60/time_slot
        self.goal = goal
        self.costs = costs
        self.finalQ = finalQ


    #Help to create a rule to form q_table key with two keypoints r in front of d and smaller number in front of big number.
    def naming(self,key1,key2):

        if key1[0] == key2[0]:
            if int(key1[1:]) < (key2[1:]):
                return key1+key2
            else:
                return key2 + key1
        elif key1[0] == 'r':
            return key1+key2
        else:
            return key2 + key1


    def initialize_q_table(self):
        for point in self.keypoints:
            if self.mode == "separate":
                self.effect_q_table[point] = np.zeros(24*self.time_slot)
                self.social_q_table[point] = np.zeros(24*self.time_slot)
            else:
                self.total_q_table[point] = np.zeros(24*self.time_slot)
        if self.mode == "separate":
            self.effect_q_table[self.goal] = self.finalQ
        else:
            self.total_q_table[self.goal] = self.finalQ

    def getReward(self,flag,feedback):

        if flag and feedback:
            return self.reward
        else:
            return 0

    def learn(self, state, reward, action,cost):
        point = state[0]
        time = state[1]+cost
        slot = int(math.floor(time/self.time_len))
        if self.mode == "separate":
            effect_q = self.effect_q_table[action][slot]
            social_q = self.social_q_table[action][slot]
            self.updateQ(state,reward + self.gamma*effect_q,reward + self.gamma*social_q)
        else:
            q = self.total_q_table[point][slot]
            self.update_totalQ(state,reward+self.gamma*q)

    def updateQ(self,state,effect_q,social_q):
        point = state[0]
        time = state[1]
        slot = int(math.floor(time / self.time_len))
        old_effect = self.effect_q_table[point][slot]
        old_social = self.social_q_table[point][slot]
        new_effect = (1 - self.alpha) * old_effect + self.alpha * effect_q
        new_social = (1-self.alpha)* old_social + self.alpha * social_q

        self.effect_q_table[point][slot] = new_effect
        self.social_q_table[point][slot] = new_social


    def update_totalQ(self, state, value):
        point = state[0]
        time = state[1]
        slot = int(math.floor(time / self.time_len))
        oldv = self.total_q_table[point][slot]
        newq = (1-self.alpha)* oldv + self.alpha * value

        self.total_q_table[point][slot] = newq


    def chooseAction(self,state):
        point = state[0]
        time = state[1]
        slot = int(math.floor(time / self.time_len))
        if self.mode == "separate":
            #Currently diabled
            if random.random() > 1000000000:  # a small chance that action is chose randomly
                #print("Random")
                self.reduceRate += 1
                if self.epsilon > 0.01 and self.reduceRate == 50:
                    self.epsilon -= 0.001
                return random(list(self.adj[point]))
            else:
                maxq = 0
                action = -1
                for end in self.adj[point]:
                    new_slot = int(math.floor((time+ self.costs[point][end]) / self.time_len))
                    if self.effect_q_table[end][new_slot] + self.social_q_table[end][new_slot]>maxq:
                        action = end
                        maxq = self.effect_q_table[end][new_slot] + self.social_q_table[end][new_slot]
                return action

        else:
            #Currently diabled
            if random.random() > 1000000000:  # a small chance that action is chose randomly
                #print("Random")
                self.reduceRate += 1
                if self.epsilon > 0.01 and self.reduceRate == 50:
                    self.epsilon -= 0.001
                return random(list(self.adj[point]))
            else:
                maxq = 0
                action = -1
                for end in self.adj[point]:
                    new_slot = int(math.floor((time+ self.costs[point][end]) / self.time_len))
                    if self.total_q_table[end][new_slot]>maxq:
                        action = end
                        maxq = self.total_q_table[end][new_slot]
                return action


