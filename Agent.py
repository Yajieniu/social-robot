import random
import Utils as u
import Map as m
from QLearn import *
import numpy as np

# people have attitude to robot
# attitude can be neutral or negative
class People:

	# Assumption: crowd does not move
	# Can impose crowd movements later
	def __init__(self, name, x1, y1, x2, y2, number, startTime, endTime, dislike):
		self.x1 = x1
		self.x2 = x2
		self.y1 = y1
		self.y2 = y2
		self.name = name
		self.startClock = startTime
		self.endClock = endTime
		self.number = number 
		self.dislike = dislike
		self.type = u.PEOPLE

# obstacle does not have attitude to robot
# robot can not get across obstacle
class Obstacle:
	def __init__(self, name, x1, y1, x2, y2, startTime, endTime):
		self.x1 = x1
		self.x2 = x2
		self.y1 = y1
		self.y2 = y2
		self.name = name
		self.startClock = startTime
		self.endClock = endTime
		self.type = u.OBSTACLE


class Robot:
	def __init__(self, priority, clock):

		#Represent in state as 0,1,2,3
		self.actions = [u.MOVE_FORWARD, u.RIGHT, u.DOWN, u.LEFT]

		self.state = {}
		self.state['x'] = 0
		self.state['y'] = 0
		self.state['direction'] = u.RIGHT
		self.state['actions'] = 0
		self.state['priority'] = priority
		self.state['clock'] = clock
		self.ai = QLearn(self.actions)

	def updateState(self, action, clock):
		self.clock = clock

		if action == u.MOVE_FORWARD:
			self.state['actions'] = 0
			if self.state['direction'] == u.RIGHT:
				self.state['y'] += 1
			elif self.state['direction'] == u.LEFT:
				self.state['y'] -= 1
			elif self.state['direction'] == u.UP:
				self.state['x'] -= 1
			elif self.state['direction'] == u.DOWN:
				self.state['x'] += 1

		elif action == u.TURN_BACK:
			self.state['actions'] = 2
			if self.state['direction'] == u.RIGHT:
				self.state['direction'] = u.LEFT
			elif self.state['direction'] == u.LEFT:
				self.state['direction'] = u.RIGHT
			elif self.state['direction'] == u.UP:
				self.state['direction'] = u.DOWN
			elif self.state['direction'] == u.DOWN:
				self.state['direction'] = u.UP
				
		elif action == u.TURN_RIGHT:
			self.state['actions'] = 1
			if self.state['direction'] == u.RIGHT:
				self.state['direction'] = u.DOWN
			elif self.state['direction'] == u.LEFT:
				self.state['direction'] = u.UP
			elif self.state['direction'] == u.UP:
				self.state['direction'] = u.RIGHT
			elif self.state['direction'] == u.DOWN:
				self.state['direction'] = u.LEFT

		elif action == u.TURN_LEFT:
			self.state['actions'] = 3
			if self.state['direction'] == u.RIGHT:
				self.state['direction'] = u.UP
			elif self.state['direction'] == u.LEFT:
				self.state['direction'] = u.DOWN
			elif self.state['direction'] == u.UP:
				self.state['direction'] = u.LEFT
			elif self.state['direction'] == u.DOWN:
				self.state['direction'] = u.RIGHT


# This is a human feedback emulator
class Human:
	def __init__(self):
		pass

	def giveFeedback(self, robot, map):
		e = 0   # effectiveness feedback
		h = 0	# social feedback

		# if robot hits people
		if map.occupants[robot.x][robot.y] == u.PEOPLE:
			e = -10   # negative effectiveness feedback
			 



































