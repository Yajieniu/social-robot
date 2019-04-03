
ROBOT_MARGIN = 5

TURN_LEFT = 0
TURN_RIGHT = 1
TURN_BACK = 2
MOVE_FORWARD = 3


LEFT = 3
RIGHT = 1
UP = 0
DOWN = 2

PEOPLE = 1
OBSTACLE = 2
ROOM = 3

def robot_get_range(x, y, size):
	x_left   = x + ROBOT_MARGIN
	y_top    = y + ROBOT_MARGIN
	x_right  = x + size - ROBOT_MARGIN
	y_bottom = y + size - ROBOT_MARGIN

	return x_left, x_right, y_top, y_bottom


def robot_position(y, x, size, direction):
	if direction == LEFT:
		#print("LEFT: ",direction, "Check : ",LEFT)
		return robot_face_left(x, y, size)
	if direction == RIGHT:
		return robot_face_right(x, y, size)		
	if direction == UP:
		return robot_face_up(x, y, size)
	if direction == DOWN:
		return robot_face_down(x, y, size)

def robot_face_left(x, y, size):
	x_left, x_right, y_top, y_bottom = robot_get_range(x, y, size)
	x_middle = int((x_left + x_right) / 2)

	point1 = [x_left, y_bottom]
	point2 = [x_right, y_bottom]
	point3 = [x_middle, y_top]

	return point1, point2, point3


def robot_face_right(x, y, size):
	x_left, x_right, y_top, y_bottom = robot_get_range(x, y, size)
	x_middle = int((x_left + x_right) / 2)

	point1 = [x_left, y_top]
	point2 = [x_right, y_top]
	point3 = [x_middle, y_bottom]

	return point1, point2, point3


def robot_face_up(x, y, size):
	x_left, x_right, y_top, y_bottom = robot_get_range(x, y, size)
	y_middle = int((y_top + y_bottom) / 2)

	point1 = [x_left, y_middle]
	point2 = [x_right, y_top]
	point3 = [x_right, y_bottom]

	return point1, point2, point3


def robot_face_down(x, y, size):
	x_left, x_right, y_top, y_bottom = robot_get_range(x, y, size)
	y_middle = int((y_top + y_bottom) / 2)

	point1 = [x_left, y_top]
	point2 = [x_left, y_bottom]
	point3 = [x_right, y_middle]

	return point1, point2, point3
