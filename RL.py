import numpy as np
import math
import random
import pickle

class QLearn:

    def __init__(self, keypoints,adj,costs,reward,mode,time_slot, goal,finalQ,start_time, epsilon=0.1, alpha=0.9, gamma=0.9):

        self.effect_q_table = {}
        self.social_q_table = {}
        self.total_q_table = {}
        self.mode = mode
        self.keypoints = keypoints
        self.adj = adj
        self.reward = reward

        #This means how many time slot we choose to have for each hour
        self.time_slot = time_slot
        self.time_len = 60/time_slot
        self.goal = goal
        self.costs = costs
        self.finalQ = finalQ
        self.initialize_q_table()
        self.gamma = gamma
        self.epsilon = epsilon
        self.alpha = alpha
        self.start_time = start_time
        self.reduceRate = 0

    def cal_alpha(self, cost):
        max_value = 7.81200003624  # max cost
        min_value = 0.75  # min cost
        const = 0.1 / (max_value - min_value)
        return 0.85 + (max_value - cost) * const

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
        #Uncomment this part to load

        if self.mode == "separate":
            self.effect_q_table = np.load("effect_q_table.data.npy")[()]
            self.social_q_table = np.load("social_q_table.data.npy")[()]
            print(self.effect_q_table)
        else:
            self.total_q_table = np.load("total_q_table.data.npy")[()]


        # for point in self.keypoints:
        #     if self.mode == "separate":
        #         self.effect_q_table[point] = np.zeros(24*self.time_slot)
        #         self.social_q_table[point] = np.zeros(24*self.time_slot)
        #     else:
        #         self.total_q_table[point] = np.zeros(24*self.time_slot)
        # if self.mode == "separate":
        #     self.effect_q_table[self.goal][:] = self.finalQ
        # else:
        #     self.total_q_table[self.goal][:] = self.finalQ


    def getReward(self,flag,feedback):

        if flag and feedback:
            return self.reward
        else:
            return 0

    def HumanFeedback(self,feedback,state):
        point = state[0]
        time = state[1]
        #print("Human Time: ",time)
        if self.mode == "separate":
            #print(feedback)
            for next_goal in feedback:
                slot = int(math.floor(time + self.costs[point][next_goal]/ self.time_len)) % 480
                effect = feedback[next_goal][0]
                social = feedback[next_goal][1]

                self.effect_q_table[next_goal][slot] += effect
                self.social_q_table[next_goal][slot] += social



        else:
            slot = int(math.floor(time / self.time_len))
            for next_goal in feedback:
                slot = int(math.floor(time / self.time_len))
                effect = feedback[next_goal][0]
                social = feedback[next_goal][1]
                self.total_q_table[next_goal][slot] += effect + social



    def learn(self, state, reward, action):
        point = state[0]
        time = state[1]+self.costs[point][action]
        slot = int(math.floor(time/self.time_len))
        if self.mode == "separate":
            effect_q = self.effect_q_table[action][slot]
            social_q = self.social_q_table[action][slot]
            cost = self.costs[point][action]
            self.updateQ(state,reward + self.gamma*effect_q,reward + self.gamma*social_q,cost)
        else:
            q = self.total_q_table[point][slot]
            cost = self.costs[point][action]
            self.update_totalQ(state,reward+self.gamma*q,cost)





    def updateQ(self,state,effect_q,social_q,cost):
        point = state[0]
        time = state[1]
        slot = int(math.floor(time / self.time_len))
        old_effect = self.effect_q_table[point][slot]
        old_social = self.social_q_table[point][slot]
        new_effect = (1 - self.cal_alpha(cost)) * old_effect + self.cal_alpha(cost) * effect_q
        new_social = (1-self.alpha)* old_social + self.alpha * social_q

        self.effect_q_table[point][slot] = new_effect
        self.social_q_table[point][slot] = new_social


#Currently using simple addition to add value
    def update_totalQ(self, state, value,cost):
        point = state[0]
        time = state[1]
        slot = int(math.floor(time / self.time_len))%(24*20)
        oldv = self.total_q_table[point][slot]
        newq = (1- self.cal_alpha(cost))* oldv + self.cal_alpha(cost) * value

        self.total_q_table[point][slot] = newq


    def chooseAction(self,state):
        point = state[0]
        time = state[1]
        if self.mode == "separate":
            if random.random() < self.epsilon:  # a small chance that action is chose randomly
                self.reduceRate += 1
                if self.epsilon > 0.01 and self.reduceRate == 50:
                    self.epsilon -= 0.001
                return random.choice(list(self.adj[point]))



            else:
                maxq = 0
                action = -1
                for end in self.adj[point]:
                    new_slot = int(math.floor(time+ self.costs[point][end] / self.time_len)) % 480
                    print(self.effect_q_table[point])
                    if self.effect_q_table[end][new_slot] + self.social_q_table[end][new_slot]>maxq:
                        action = end
                        maxq = self.effect_q_table[end][new_slot] + self.social_q_table[end][new_slot]
                if action == -1:
                    return random.choice(list(self.adj[point]))
                return action

        else:
            #Currently diabled
            if random.random() < self.epsilon:  # a small chance that action is chose randomly
                #print("Random")
                self.reduceRate += 1
                if self.epsilon > 0.01 and self.reduceRate == 50:
                    self.epsilon -= 0.001
                return random(list(self.adj[point]))
            else:
                maxq = 0
                action = -1
                for end in self.adj[point]:
                    new_slot = int(math.floor((time+ self.costs[point][end]) / self.time_len)) % 480
                    if self.total_q_table[end][new_slot]>maxq:
                        action = end
                        maxq = self.total_q_table[end][new_slot]
                if action == -1:
                    return random(list(self.adj[point]))
                return action


