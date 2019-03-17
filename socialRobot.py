from Map import *
from Agent import *

class Game:
	def __init__(self):
		self.mapWidth = 16
		self.mapHeight = 9
		self.reward_table = [[0] * self.mapHeight] * self.mapWidth
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
		self.map.create_room()
		self.robot = Robot(self.priority, self.clock)
		self.map.draw_robot(self.robot)

		self.create_objects()
		

	# pre-defined now
	def create_objects(self):
		p1 = People('p1', 7, 0, 8, 1, 2, 9, 10, True)
		p2 = People('p2', 4, 3, 5, 4, 2, 8, 9, False)
		p3 = People('p3', 8, 6, 9, 7, 2, 10, 11, False)
		self.objects['p1'] = p1
		self.objects['p2'] = p2	
		self.objects['p3'] = p3

	def chooseAction(self):
		x = self.robot.x
		y = self.robot.y
		direction = self.robot.direction
		actions = [u.TURN_LEFT, u.TURN_RIGHT, u.TURN_BACK, u.MOVE_FORWARD]

		# robot cannot move forward at some states
		if direction == u.LEFT:
			if x == 0 or self.map.occupants[x-1][y] == u.ROOM:
				actions.remove(u.MOVE_FORWARD)
		elif direction == u.RIGHT:
			if x == self.mapWidth-1 or self.map.occupants[x+1][y] == u.ROOM:
				actions.remove(u.MOVE_FORWARD)
		elif direction == u.UP:
			if y == 0 or self.map.occupants[x][y-1] == u.ROOM:
				actions.remove(u.MOVE_FORWARD)
		elif direction == u.RIGHT:
			if y == self.mapHeight-1 or self.map.occupants[x][y+1] == u.ROOM:
				actions.remove(u.MOVE_FORWARD)

		action = u.MOVE_FORWARD

		if [x,y] == [0, 0] and self.robot.direction == u.UP:
			action = u.TURN_RIGHT
		if [x,y] == [self.mapWidth-1, 0] and self.robot.direction == u.RIGHT:
			action = u.TURN_RIGHT
		if [x,y] == [self.mapWidth-1, self.mapHeight-1	] and self.robot.direction == u.DOWN:
			action = u.TURN_RIGHT
		if [x,y] == [0, self.mapHeight-1] and self.robot.direction == u.LEFT:
			action = u.TURN_RIGHT

		return action

	def updateTime(self, action):
		if self.map.occupants[self.robot.x][self.robot.y] == u.PEOPLE:
			self.seconds += 50
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
				print("!!!!!!!!!!!!!!!")
			if self.clock == obj.endClock and self.minutes == 0:
				self.map.remove_object(obj)

		# update robot
		self.map.draw_robot(self.robot)
		self.map.update()


	def getReward(self):
		return 0

	def update(self):
		r = self.getReward()

		action = self.chooseAction()

		self.updateTime(action)
		self.robot.updateState(action, self.clock)
		self.updateMap()
		self.finalReport()

		if self.robot.x == self.mapWidth and self.robot.y == self.mapHeight:
			self.endGame = True

	def finalReport(self):
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

		print("Time: " + clock + ":" + minutes + ":" + seconds)


game = Game()

while True:
	game.update()
	if game.endGame:
		ans = raw_input("Start a new game? Input 'y' or 'n':")

		if ans=='y':
			game.newGame()
		else:
			game.finalReport()
			break




