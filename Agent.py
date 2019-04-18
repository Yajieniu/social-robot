



# people have attitude to robot
# attitude can be neutral or negative
class People:

	# Assumption: crowd does not move
	# Can impose crowd movements later
	def __init__(self, name, x1, y1, x2, y2, number, startClock, 
					startMinute, startSecond, duration, endTime, dislike):
		self.x1 = x1
		self.x2 = x2
		self.y1 = y1
		self.y2 = y2
		self.name = name
		self.startClock = startClock
		self.startMinute = startMinute
		self.startSecond = startSecond
		self.duration = duration.  # in seconds
		self.number = number 
		self.dislike = dislike
		self.type = u.PEOPLE
		self.endTime()

	def endTime(self):
		self.endClock = self.startClock
		self.endMinute = self.startMinute
		self.endSecond = self.startSecond
		
		for i in range(self.duration):
			self.endSecond += 1
			
			if self.endSecond >= 60:
				self.endSecond -= 60
				self.endMinute += 1
			
			if self.endMinute >= 60:
				self.endMinute -= 60
				self.endClock += 1	

				

# This is a human feedback emulator
class Human:
	def __init__(self):
		pass

	def giveFeedback(self, robot, map):
		e = 0   # effectiveness feedback
		h = 0	# social feedback
