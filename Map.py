from tkinter import *
import Utils as u
import time
import copy as cp


ENABLE_DASH = True

NEUTRAL_COLOR = 'bisque'
DISLIKE_COLOR = 'deepskyblue2'
OBSTACLE_COLOR = 'snow4'
ROBOT_COLOR = 'tomato'

class Map:
	def __init__(self, width=16, height=9):
		self.agentGUI = None
		self.object_dict = {}
		self.size = 5
		self.size *= u.ROBOT_MARGIN
		self.width = width * self.size
		self.height = height * self.size

		self.robot = None
		self.occupants = [[0] * width] * height
		self.root = Tk()
		self.root.title("Social Robot Simulator")
		self.canvas = Canvas(self.root, width=self.width, height=self.height)
		self.canvas.pack()

	def create_room(self):

		# Define borders of rectangles (~rooms)
		# x1, y1, x2, y2
		numRoom = 14
		rooms = [[0] * 4] * numRoom
		rooms[0] = [1, 1, 3, 4]
		rooms[1] = [1, 5, 2, 9]
		rooms[2] = [1, 10, 2, 11]
		rooms[3] = [1, 12, 2, 13]
		rooms[4] = [1, 14, 5, 15]
		rooms[5] = [3, 5, 4, 7]
		rooms[6] = [3, 8, 4, 13]
		rooms[7] = [5, 1, 8, 4]
		rooms[8] = [5, 5, 8, 8]
		rooms[9] = [5, 9, 6, 11]
		rooms[10] = [7, 9, 8, 11]
		rooms[11] = [5, 12, 6, 13]
		rooms[12] = [3, 3, 4, 4]
		rooms[13] = [6, 12, 8, 15]
		copy_room = cp.deepcopy((rooms))
		# udpate occupants for rooms
		for i in range(14):
			for height in range(rooms[i][0], rooms[i][2]):
				for width in range(rooms[i][1], rooms[i][3]):
					self.occupants[height][width] = u.ROOM

		# Draw rooms
		for i in range(numRoom):
			rooms[i] = [rooms[i][j] * self.size for j in range(4)]
			self.canvas.create_rectangle(rooms[i][1], rooms[i][0], rooms[i][3], rooms[i][2], fill='gray', outline="")

		# Draw dash lines
		if ENABLE_DASH:
			for i in range(0, self.width, self.size):
				self.canvas.create_line(i, 0, i, self.height, fill="gray", dash=(1, 4))

			for j in range(0, self.height, self.size):
				self.canvas.create_line(0, j, self.width, j, fill="gray", dash=(1, 4))
		return copy_room


	def create_object(self, item):

		# if this object is already created
		if item.name in self.object_dict:
			return

		x1 = item.x1 * self.size
		x2 = item.x2 * self.size
		y1 = item.y1 * self.size
		y2 = item.y2 * self.size

		# udpate occupants for people or obstacle
		for width in range(item.x1, item.x2):
			for height in range(item.y1, item.y2):
				self.occupants[height][width] = item.type

		if item.type == u.PEOPLE:
			if item.dislike:
				self.object_dict[item.name] = self.canvas.create_oval(x1, y1, x2, y2, fill=DISLIKE_COLOR)
			else:
				self.object_dict[item.name] = self.canvas.create_oval(x1, y1, x2, y2, fill=NEUTRAL_COLOR)
		elif item.type == u.OBSTACLE:
			self.object_dict[item.name] = self.canvas.create_oval(x1, y1, x2, y2, fill=OBSTACLE_COLOR)
		else:
			raise ValueError('Create object: wrong object type.')

	def draw_robot(self, robot):
		x = robot.state['x'] * self.size
		y = robot.state['y'] * self.size

		if self.robot != None:
			self.canvas.delete(self.robot)

		p1, p2, p3 = u.robot_position(x,y, self.size, robot.state['direction'])

		self.robot = self.canvas.create_polygon(p1[0], p1[1],
												p2[0], p2[1],
												p3[0], p3[1],
												fill=ROBOT_COLOR)

	# remove people or obstacle from the map
	def remove_object(self, item):
		if item.name in self.object_dict:
			self.canvas.delete(self.object_dict[item.name])
			del self.object_dict[item.name]

	def update(self):
		self.canvas.update()
		self.canvas.after(5)



