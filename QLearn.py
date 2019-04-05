import random
from Agent import *
import numpy as np
REWARD = 0
EFFECTIVENESS = 1
SOCIAL = 2

def check_time():
    return 0


class QLearn:

    def __init__(self,  actions, epsilon=0.5, alpha=0.9, gamma=0.9):
        self.weight_r = 1
        self.weight_effect = 1
        self.weight_social = 1
        self.weights = {REWARD: self.weight_r,
						EFFECTIVENESS: self.weight_effect,
						SOCIAL: self.weight_social}
        #self.q_tables =  np.zeros((9,16,4,24))
        self.q_tables = np.load("Q_table.txt.npy")
        self.q_tables[8,15] = 100
        self.epsilon = epsilon
        self.reduceRate = alpha
        self.alpha = alpha
        self.gamma = gamma
        self.actions = actions
        self.reward = -200

    def getReward(self,flag,feedback):
        if flag and feedback:
            return self.reward

        else:
            return 0

    def learn(self,state, reward,action,direction):
        if action == u.MOVE_FORWARD:
            temp_y = state['y']
            temp_x = state['x']
            if state['direction'] == u.RIGHT:
                temp_y += 1
            elif state['direction'] == u.LEFT:
                temp_y -= 1
            elif state['direction'] == u.UP:
                temp_x -= 1
            elif state['direction'] == u.DOWN:
                temp_x += 1
        else:
            temp_x = state['x']
            temp_y = state['y']


        maxqnew = self.q_tables[temp_x,temp_y,direction,state['clock']]
        if (temp_x == 8 and temp_y == 0) or (temp_x == 0 and temp_y == 15):
            print("Check corner case: ", self.q_tables[temp_x,temp_y,:,8])
        self.updateQ(state, reward + self.gamma*maxqnew)



    def updateQ(self, state, value):

        oldv = self.q_tables[state['x'],state['y'],state['direction'],state['clock']]
        newq = (1-self.alpha)* oldv + self.alpha * value
        if abs(newq) < 0.0001:
            newq = 0
        self.q_tables[state['x'],state['y'],state['direction'],state['clock']] = newq
        if newq != 0:
            print("Check New Q", newq)
            print("Reach here: ", self.q_tables[state['x'],state['y'],state['direction'],state['clock']])
    #Find the max q value for next possible state
    def check_q(self,state,rooms):
        temp_x = state['x']
        temp_y = state['y']
        action_space = []
        action_space.append((temp_x + 1,temp_y))
        action_space.append((temp_x - 1,temp_y))
        action_space.append((temp_x,temp_y + 1))
        action_space.append((temp_x,temp_y - 1))
        max_q = -1
        direction_list = []
        #print("Check State: ",state['x'] ," Y: ", state['y']," direction: ",state['direction'])
        #print("Check action: ", action_space)
        for i in range(4):
            next_loc = action_space[i]
            if next_loc[0] >= 0 and next_loc[0] < 9 and next_loc[1] >= 0 and next_loc[1] < 16 and not self.check_room_q(rooms,next_loc[0],next_loc[1]):
                current_q = -1
                for j in range(4):
                    temp = self.q_tables[next_loc[0], next_loc[1], j, state['clock']]
                    if current_q <= temp:
                        current_q = temp
                if max_q <= current_q:
                    direction_list.append(i)
                    max_q = current_q
        if len(direction_list) > 1:
            direction = random.choice(direction_list)
        else:
            direction = direction_list[0]
        #print("Pre-Change: ",direction)
        if direction == 0:
            direction = u.DOWN
        elif direction == 1:
            direction = u.UP
        elif direction == 2:
            direction = u.RIGHT
        else:
            direction = u.LEFT
        return max_q,direction

    def make_turn(self,direction,state):

        if direction == u.UP:
            if state['direction'] == u.RIGHT:
                action = u.TURN_LEFT
            elif state['direction'] == u.LEFT:
                action = u.TURN_RIGHT
            else:
                action = u.TURN_BACK
        elif direction == u.LEFT:
            if state['direction'] == u.RIGHT:
                action = u.TURN_BACK
            elif state['direction'] == u.UP:
                action = u.TURN_LEFT
            else:
                action = u.TURN_RIGHT
        elif direction == u.RIGHT:
            if state['direction'] == u.DOWN:
                action = u.TURN_LEFT
            elif state['direction'] == u.UP:
                action = u.TURN_RIGHT
            else:
                action = u.TURN_BACK
        else:
            if state['direction'] == u.RIGHT:
                action = u.TURN_RIGHT
            elif state['direction'] == u.LEFT:
                action = u.TURN_LEFT
            else:
                action = u.TURN_BACK
        return action

    def check_room_q(self,rooms,temp_x,temp_y):
        for room in rooms:
            if temp_x >= room[0] and temp_x < room[2] and temp_y >= room[1] and temp_y < room[3]:
                return True
        return False
    def check_room(self,rooms,state):
        temp_x = state['x']
        temp_y = state['y']
        if state['direction'] == u.DOWN:
            temp_x += 1
        elif state['direction'] == u.UP:
            temp_x -= 1
        elif state['direction'] == u.LEFT:
            temp_y -= 1
        elif state['direction'] == u.RIGHT:
            temp_y += 1
        if temp_y < 0 or temp_y >= 16 or temp_x < 0 or temp_x >= 9:
            return True
        for room in rooms:
            if temp_x >= room[0] and temp_x < room[2] and temp_y >= room[1] and temp_y < room[3]:
                return True
        return False

    def find_correct_move(self,actions,state,rooms):
        wrong_move = True
        while (wrong_move):
            action = random.choice(actions)
            if action == u.MOVE_FORWARD and self.check_room(state, rooms):
                wrong_move = True
            else:
                wrong_move = False
        return action
    def chooseAction(self, state, actions,rooms):
        # print('choose action')

        if random.random() > self.epsilon:  # a small chance that action is chose randomly
            #print("Random")
            self.reduceRate += 1
            if self.epsilon > 0.01 and self.reduceRate == 50:
                self.epsilon -= 0.001
                self.reduceRate = 0
            action = self.find_correct_move(actions,rooms,state)

        else:
            #print("Not Random")
            maxq,direction = self.check_q(state,rooms)

            if state['direction'] == direction:
                action = u.MOVE_FORWARD
            else:
                action = self.make_turn(direction,state)
            print("Check Direction: ",direction)
            print("Check Current Direction", direction)
            print("Check Action: ", action)
        return action,direction
















