from Tkinter import *
import Utils as u
import time


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
		self.occupants = [[0] * height] * width
		
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

		# udpate occupants for rooms
		for i in range(14):
			for width in range(rooms[i][0], rooms[i][2]):
				for height in range(rooms[i][1], rooms[i][3]):
					self.occupants[width][height] = u.ROOM

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
				self.occupants[width][height] = item.type

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
		x = robot.x * self.size
		y = robot.y * self.size

		if self.robot != None:
			self.canvas.delete(self.robot)
		
		p1, p2, p3 = u.robot_position(x, y, self.size, robot.direction)
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
		self.canvas.after(40)



