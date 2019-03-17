from Map import *
from Agent import *

class Game:
	def __init__(self):
		self.map = Map()
		self.priority = 1
		self.robot = Robot(self.priority)
		self.map.create_room()
		self.map.create_robot()
		self.reward_table = [self.map.width][self.map.height]

	def getReward(self):
		pass
		
	def update(self):

		r = getReward(self.robot.state)

		e, h = getHumanFeedback()

		r = updateR(e, h, r)

		ChooseAction()

		UpdateMap()

		self.robot.state = UpdateState()
			

	def startNewGame(self):
		clearEverything()
		reInit()


while True:
	game.update()
	if game.endGame:
		ans = raw_input("New Game?")

		if ans=='y':
			startNewGame()
		else:
			finalReport()
			break




