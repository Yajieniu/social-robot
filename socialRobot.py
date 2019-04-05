from Map import *
from Agent import *
from Utils import *
from QLearn import *
import numpy as np
class Game:
	def __init__(self):
		self.mapWidth = 16
		self.mapHeight = 9
		self.rooms = 0
		self.actions = [u.MOVE_FORWARD,u.DOWN, u.LEFT,  u.RIGHT]
		self.newGame()

	def newGame(self):
		# self.priority = raw_input("Please give job priority [1-5]:")
		self.priority = 1
		self.objects = {}
		self.clock = 8
		self.minutes = 0
		self.seconds = 0
		self.endGame = False
		self.map = Map()
		self.rooms = self.map.create_room()
		self.robot = Robot(self.priority, self.clock)
		self.map.draw_robot(self.robot)
		self.flag = False
		self.create_objects()
		self.critical_section = [(4,4)]
		self.count = 0
	# pre-defined now
	def create_objects(self):
		p1 = People('p1', 7, 0, 8, 1, 2, 9, 10, True)
		p2 = People('p2', 4, 3, 5, 4, 2, 8, 9, False)
		p3 = People('p3', 8, 6, 9, 7, 2, 10, 11, False)
		self.objects['p1'] = p1
		self.objects['p2'] = p2	
		self.objects['p3'] = p3

	def updateTime(self, action):
		if self.map.occupants[self.robot.state['x']][self.robot.state['y']] == u.PEOPLE:
			self.seconds += 100
		elif action == u.TURN_BACK:
			self.seconds += 50
		else:
			self.seconds += 50

		# make sure time format is correct
		if self.seconds >= 60:
			self.minutes += 1
			self.seconds -= 60

		if self.minutes >= 60:
			self.clock += 1
			self.minutes -= 60

	def updateMap(self):
		# update objects
		for name in self.objects:
			obj = self.objects[name]
			if self.clock == obj.startClock and self.minutes == 0:
				self.map.create_object(obj)
			if self.clock == obj.endClock and self.minutes == 0:
				self.map.remove_object(obj)

		# update robot
		self.map.draw_robot(self.robot)
		self.map.update()

#Ask for feedback
	def ask_feedback(self,action):
		# TURN_LEFT = 0
		# TURN_RIGHT = 1
		# TURN_BACK = 2
		# MOVE_FORWARD = 3
		if action == 0:
			text = "TURN_LEFT"
		elif action == 1:
			text = "TURN_RIGHT"
		elif action == 2:
			text = "TURN_BACK"
		else:
			text = "MOVE_FORWARD"
		prompt = "The robot is trying to perform this action: "+ text +  " Please enter y or f for feedback"
		feedback = input(prompt)
		if feedback == 'y':
			feedback = False
		else:
			feedback = True

		return feedback
	def update(self):

		action,direction = self.robot.ai.chooseAction(self.robot.state, self.actions,self.rooms)
		feedback = False
		#Just set one critical point for testing purpose
		if self.robot.state['x'] == 4 and self.robot.state['y'] == 4 and self.flag:
			feedback = self.ask_feedback(action)
		self.robot.ai.learn(self.robot.state, self.robot.ai.getReward(self.flag,feedback),action,direction)
		self.updateTime(action)
		self.robot.updateState(action, self.clock)
		self.updateMap()
		self.printTime()
		if self.robot.state['x'] == 8 and self.robot.state['y'] == 15:
			# print(
			# 	self.robot.ai.q_tables[3, 4, self.robot.state['direction'],
			# 						   self.robot.state['clock']])
			# print(
			# 	self.robot.ai.q_tables[4, 3, self.robot.state['direction'],
			# 						   self.robot.state['clock']])
			# print(self.robot.ai.q_tables[self.robot.state['x'], self.robot.state['y']-1, self.robot.state['direction'],
			# 	  self.robot.state['clock']])
			# print(
			# 	self.robot.ai.q_tables[self.robot.state['x']-1, self.robot.state['y'], self.robot.state['direction'],
			# 						   self.robot.state['clock']])

			self.robot.state['x'] = 0
			self.robot.state['y'] = 0
			self.robot.state['direction'] = u.RIGHT
			self.count += 1


	def printTime(self):
		clock = str(self.clock)
		minutes = str(self.minutes)
		seconds = str(self.seconds)

		# make sure time format is correct
		if len(clock) == 1:
			clock = '0' + clock

		if len(minutes) == 1:
			minutes = '0' + minutes

		if len(seconds) == 1:
			seconds = '0' + seconds

		#print("Time: " + clock + ":" + minutes + ":" + seconds)

	def finalReport(self):
		pass


game = Game()

while True:
	game.update()
	if game.count > 5:
		np.save("Q_table.txt", game.robot.ai.q_tables)
		break




