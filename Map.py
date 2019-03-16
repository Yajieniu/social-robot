from tkinter import *
import Utils
import time


ENABLE_DASH = True

NEUTRAL_COLOR = 'bisque'
DISLIKE_COLOR = 'deepskyblue2'
OBSTACLE_COLOR = 'snow4'
ROBOT_COLOR = 'tomato'

class Map:
	def __init__(self, width=16, height=9):
		self.agentGUI = None
		self.people_dict = {}
		self.obstacle_dict = {}
		self.size = 5
		self.size *= Utils.ROBOT_MARGIN
		self.width = width * self.size
		self.height = height * self.size
		self.root = Tk()
		self.root.title("Social Robot Simulator")
		self.canvas = Canvas(self.root, width=self.width, height=self.height)
		self.canvas.pack()

	def create_room(self):

		# Define borders of rectangles (~rooms)
		# x1, y1, x2, y2
		numRoom = 14
		rooms = [[0] * 4] * numRoom
		rooms[0] = [1, 1, 4, 3]
		rooms[1] = [5, 1, 9, 2]
		rooms[2] = [10, 1, 11, 2]
		rooms[3] = [12, 1, 13, 2]
		rooms[4] = [14, 1, 15, 5]
		rooms[5] = [5, 3, 7, 4]
		rooms[6] = [8, 3, 13, 4]
		rooms[7] = [1, 5, 4, 8]
		rooms[8] = [5, 5, 8, 8]
		rooms[9] = [9, 5, 11, 6]
		rooms[10] = [9, 7, 11, 8]
		rooms[11] = [12, 5, 13, 6]
		rooms[12] = [3, 3, 4, 4]
		rooms[13] = [12, 6, 15, 8]

		# Draw rooms 
		for i in range(numRoom):
			rooms[i] = [rooms[i][j] * self.size for j in range(4)]
			self.canvas.create_rectangle(rooms[i][0], rooms[i][1], rooms[i][2], rooms[i][3], fill='gray', outline="")

		# Draw dash lines
		if ENABLE_DASH:
			for i in range(0, self.width, self.size):
				self.canvas.create_line(i, 0, i, self.height, fill="gray", dash=(1, 4))	

			for j in range(0, self.height, self.size):
				self.canvas.create_line(0, j, self.width, j, fill="gray", dash=(1, 4))	


	def create_people(self, people):
		x1 = people.x1 * self.size
		x2 = people.x2 * self.size
		y1 = people.y1 * self.size
		y2 = people.y2 * self.size

		if people.dislike:
			self.people_dict[people.name] = self.canvas.create_oval(x1, y1, x2, y2, fill=DISLIKE_COLOR)
		else:
			self.people_dict[people.name] = self.canvas.create_oval(x1, y1, x2, y2, fill=NEUTRAL_COLOR)

	def create_obstacle(self, obstacle):
		x1 = obstacle.x1 * self.size
		x2 = obstacle.x2 * self.size
		y1 = obstacle.y1 * self.size
		y2 = obstacle.y2 * self.size

		self.obstacle_dict[obstacle.name] = self.canvas.create_oval(x1, y1, x2, y2, fill=OBSTACLE_COLOR)


	def create_robot(self, robot):
		x = robot.x * self.size
		y = robot.y * self.size

		p1, p2, p3 = robot_face_right(x, y, self.size)
		self.robot = self.canvas.create_polygon(p1[0], p1[1],
												p2[0], p2[1],
												p3[0], p3[1],
												fill=ROBOT_COLOR)


	def update(self):
		self.canvas.update()
		self.canvas.after(30)


m = Map()
m.create_room()
while True:
	m.update()

