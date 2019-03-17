import random
import Utils as u
import Map as m

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
		self.x = 0
		self.y = 0
		self.loc = [self.x, self.y] 
		self.direction = u.RIGHT
		self.priority = priority
		self.clock = clock

		self.state = {}
		self.state['loc'] = self.loc
		self.state['direction'] = self.direction
		self.state['priority'] = self.priority
		self.state['clock'] = self.clock

	def updateState(self, action, clock):
		self.clock = clock

		if action == u.MOVE_FORWARD:
			if self.direction == u.RIGHT:
				self.x += 1
			elif self.direction == u.LEFT:
				self.x -= 1
			elif self.direction == u.UP:
				self.y -= 1
			elif self.direction == u.DOWN:
				self.y += 1

		elif action == u.TURN_BACK:
			if self.direction == u.RIGHT:
				self.direction = u.LEFT
			elif self.direction == u.LEFT:
				self.direction = u.RIGHT
			elif self.direction == u.UP:
				self.direction = u.DOWN
			elif self.direction == u.DOWN:
				self.direction = u.UP
				
		elif action == u.TURN_RIGHT:
			if self.direction == u.RIGHT:
				self.direction = u.DOWN
			elif self.direction == u.LEFT:
				self.direction = u.UP
			elif self.direction == u.UP:
				self.direction = u.RIGHT
			elif self.direction == u.DOWN:
				self.direction = u.LEFT

		elif action == u.TURN_LEFT:
			if self.direction == u.RIGHT:
				self.direction = u.UP
			elif self.direction == u.LEFT:
				self.direction = u.DOWN
			elif self.direction == u.UP:
				self.direction = u.LEFT
			elif self.direction == u.DOWN:
				self.direction = u.RIGHT



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
			 



































