from Utils import *
import random




class Game:
	def __init__(self):
		self.newGame()

	def newGame(self):
		self.priority = 1
		self.keypoints = Utils.obj
		self.starting_time()
		self.endGame = False

	def starting_time(self):
		self.clock = random.randint(8, 16)
		self.minute = random.randint(0, 59)
		self.second = random.randint(0, 59)

	
