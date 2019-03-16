import random
import Utils as u


# people have attitude to robot
# attitude can be neutral or negative
class People:

	# Assumption: crowd does not move
	# Can impose crowd movements later
	def __init__(self, name, x1, y1, number, startTime, endTime, dislike, 
				 map, x2=x1, y2=y1):

		self.loc = [x1, y1, x2, y2]
		self.name = name
		self.number = number 
		self.startTime = startTime
		self.endTime = endTime
		self.dislike = dislike
		self.map = map

# obstacle does not have attitude to robot
# robot can not get across obstacle
class Obstacle:

	def __init__(self, name, x1, y1, startTime, endTime, map, x2=x1, y2=y1):
		self.loc = [x1, y1, x2, y2]
		self.name = name
		self.startTime = startTime
		self.endTime = endTime


class Robot:
	def __init__(self, priority):
		self.actions = [u.LEFT, u.RIGHT, u.BACK, u.FORWARD]
		self.x = 0
		self.y = 0
		self.loc = [self.x, self.y] 
		self.direction = u.RIGHT
		self.priority = priority
		self.time = 0

		self.state = {}
		self.state['loc'] = self.loc
		self.state['direction'] = self.direction
		self.state['priority'] = self.priority
		self.state['time'] = self.time



































