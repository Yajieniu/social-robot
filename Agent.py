import random




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
	def __init__(self):


































