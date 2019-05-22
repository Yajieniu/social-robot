import pygame as pg
import math
import numpy
import random
import time
from RL import *

def draw_dashed_line(surf, color, start_pos, end_pos, width=1, dash_length= 10):
	x1, y1 = start_pos
	x2, y2 = end_pos
	dl = dash_length
	x1 += 15
	x2 += 15
	y1 += 15
	y2 += 15

	if (x1 == x2):
		ycoords = [y for y in numpy.arange(y1, y2, dl if y1 < y2 else -dl)]
		xcoords = [x1] * len(ycoords)
	elif (y1 == y2):
		xcoords = [x for x in numpy.arange(x1, x2, dl if x1 < x2 else -dl)]
		ycoords = [y1] * len(xcoords)
	else:
		a = abs(x2 - x1)
		b = abs(y2 - y1)
		c = round(math.sqrt(a ** 2 + b ** 2))
		dx = dl * a / c
		dy = dl * b / c

		xcoords = [x for x in numpy.arange(x1, x2, dx if x1 < x2 else -dx)]
		ycoords = [y for y in numpy.arange(y1, y2, dy if y1 < y2 else -dy)]

	next_coords = list(zip(xcoords[1::2], ycoords[1::2]))
	last_coords = list(zip(xcoords[0::2], ycoords[0::2]))
	for (x1, y1), (x2, y2) in zip(next_coords, last_coords):
		start = (round(x1), round(y1))
		end = (round(x2), round(y2))
		pg.draw.line(surf, color, start, end, width)

class Human(object):
	def __init__(self,image,screen):
		self.image = image
		self.screen = screen

	def draw_human(self,position):
		self.screen.blit(self.image,position)


class Buttons(object):

	def __init__(self):
		self.button_list = {}
		self.social_score = 0
		self.effective_score = 0
	def add_button(self,name,position,image,job):
		rect = image.get_rect()
		rect.x = position[0]
		rect.y = position[1]
		self.button_list[name] = {'position':position,"job":job,"image":image,"rect":rect}

	def draw_button(self,screen):
		for name in self.button_list:
			button = self.button_list[name]
			screen.blit(button['image'], button['position'])
	def event_handler(self):
		for event in pg.event.get():
			if event.type == pg.MOUSEBUTTONDOWN:
				for name in self.button_list:
					button = self.button_list[name]
					if button['rect'].collidepoint(event.pos):
						pg.mixer.music.load('social_good.mp3')
						pg.mixer.music.play(0)
						if'social' in name:
							if button['job'] == 'good':

								self.social_score += 100
							else:
								self.social_score -= 100
						else:
							if button['job'] == 'good':
								self.effective_score += 100
							else:
								self.effective_score -= 100



class Map:

	def __init__(self,X,Y,start_point,goal,speed,wait_time,reward,mode,time_slot,finalQ,human_points,start_time):
		self.coords = {'r6': (32.1917800903, 115.396934509), 'i2': (48.1107788086, 105.988296509), 'i4': (17.42395401, 105.209571838), 'd1': (6.76491165161, 112.757469177), 'r13': (45.0136451721, 102.41947937), 'd20': (23.1707439423, 105.489807129), 'i6': (14.3663759232, 113.519447327), 'r2': (8.96481704712, 115.404937744), 'i3': (33.9062576294, 105.275985718), 'd3': (19.6334762573, 112.373733521), 'd7': (29.6615200043, 112.434532166), 'd21': (21.897064209, 105.102661133), 'd17': (39.4887695312, 105.35836792), 'd10': (40.969543457, 112.495727539), 'r16': (29.9390983582, 109.440086365), 'r10': (45.0729446411, 108.629150391), 'd23': (10.3303451538, 105.190734863), 'r26': (8.9367389679, 101.593757629), 'r11': (41.097858429, 108.535583496), 'd4': (21.2724895477, 112.182777405), 'd2': (7.84000778198, 112.361663818), 'd12': (44.9742736816, 112.654785156), 'r27': (9.1826210022, 108.222724915), 'r28': (39.008392334, 114.981956482), 'r4': (24.3392028809, 115.429176331), 'd15': (51.3042526245, 105.352783203), 'd22': (20.9218959808, 105.039749146), 'r3': (20.504863739, 115.55393219), 'r5': (28.5052490234, 115.402694702), 'd8': (30.8963489532, 112.769294739), 'd18': (33.4266395569, 102.005897522), 'r1': (5.29522514343, 115.758872986), 'd19': (29.7961959839, 105.645126343), 'r21': (24.374458313, 101.63004303), 'i5': (14.7835083008, 104.688957214), 'r9': (52.9659118652, 115.366699219), 'r22': (20.5140609741, 102.019271851), 'r14': (36.7606925964, 108.823013306), 'r15': (38.2078781128, 100.458351135), 'r24': (14.609085083, 108.930099487), 'd24': (32.7120475769, 111.065345764), 'd11': (43.5953216553, 112.446990967), 'd14': (48.2460250854, 112.334037781), 'r25': (14.2544584274, 116.043502808), 'r19': (32.3290367126, 101.768623352), 'r12': (54.8262786865, 106.72668457), 'd5': (21.9395313263, 112.771110535), 'r20': (27.9855327606, 101.263656616), 'r17': (24.0002746582, 108.502052307), 'd13': (45.9205169678, 112.526473999), 'r8': (47.2909011841, 115.680419922), 'r7': (43.5528831482, 115.033187866), 'd25': (27.1601924896, 111.037071228), 'i1': (10.9330873489, 112.724777222), 'd6': (23.1813697815, 112.850349426), 'd9': (39.5764350891, 112.495727539), 'r23': (15.3893146515, 102.381370544), 'd16': (41.3706283569, 104.915588379), 'r18': (18.7453746796, 109.395431519)}
		self.adj = {'d2': {'r27', 'i1', 'd1', 'r2'}, 'd19': {'r20', 'r19', 'd20', 'i3'},
			   'd23': {'r24', 'r23', 'i5', 'r27', 'r26'}, 'r23': {'i4', 'i5', 'd23'}, 'r12': {'r9', 'd15'},
			   'd17': {'r14', 'd16', 'i3'}, 'r16': {'d25', 'd24'}, 'd22': {'i4', 'd21', 'd4', 'r17'},
			   'r25': { 'd3', 'i6', 'i1'}, 'r4': {'d6'}, 'i4': {'r24', 'r23', 'i5', 'd22'},
			   'i1': {'r24', 'r27', 'i6', 'd2', 'r25'}, 'd21': {'r22', 'd22', 'd20'}, 'd6': {'d7', 'd5', 'r4'},
			   'r9': {'d14', 'r12'}, 'd16': {'i2', 'r13', 'r15', 'd17'}, 'r15': {'d16', 'd18'},
			   'd24': {'r14', 'r16', 'd25'}, 'r7': {'d12'}, 'i2': {'d16', 'd14', 'r13', 'd15'},
			   'd13': {'r8', 'd14', 'd12'}, 'r2': {'d2'}, 'd1': {'d2', 'r1'}, 'd7': {'r5', 'd8', 'd6'},
			   'd8': {'r28', 'd7', 'd9', 'r6'}, 'i6': {'r24', 'd3', 'i1', 'r25'}, 'r3': {'d5'},
			   'i3': {'r19', 'd19', 'd18', 'd17'}, 'r20': {'d19'}, 'r24': {'i4', 'i1', 'i5', 'd23', 'd3',  'i6'},
			   'r5': {'d7'}, 'd9': {'r28', 'r14', 'd8', 'd10'}, 'r11': {'d10'}, 'r22': {'d21'},
			   'd3': {'d4', 'i6', 'r18', 'r25', 'r24'}, 'r6': {'d8'}, 'r1': {'d1'}, 'r21': {'d20'},
			   'd14': {'i2', 'd13', 'r9'}, 'd11': {'r10', 'd12', 'd10'}, 'r27': {'d2', 'i1', 'd23'},
			   'r19': {'i3', 'd19', 'd18'}, 'r17': {'d4', 'd22', 'd25'}, 'r8': {'d13'}, 'r10': {'d11'},
			   'i5': {'i4', 'r23', 'd23', 'r24'}, 'd25': {'r16', 'd24', 'r17'}, 'd20': {'d19', 'd21', 'r21'},
			   'r26': {'d23'}, 'd15': {'i2', 'r12'}, 'r14': {'d24', 'd9', 'd17'}, 'd5': {'r3', 'd4', 'd6'},
			   'd4': {'d3', 'd22', 'd5', 'r17'}, 'r13': {'i2', 'd16'}, 'r28': {'d8', 'd9', 'd10'}, 'r18': {'d3'},
			   'd18': {'r19', 'r15', 'i3'}, 'd12': {'d13', 'd11', 'r7'}, 'd10': {'r28', 'r11', 'd11', 'd9'}}
		self.cost = {'r8': {'d13': 4.10700011253}, 'd9': {'r14': 3.64100003242, 'd10': 3.29799985886, 'd8': 7.46099996567, 'r28': 2.75699996948}, 'd24': {'r16': 3.73399996758, 'r14': 2.85100007057, 'd25': 5.5569999218}, 'r27': {'i1': 1.72899985313, 'd23': 4.132999897, 'd2': 3.52200007439}, 'd8': {'d7': 0.942000150681, 'r6': 4.27799987793, 'd9': 7.46099996567, 'r28': 7.81200003624}, 'r28': {'d10': 4.18099999428, 'd8': 7.81200003624, 'd9': 2.75699996948}, 'd6': {'r4': 4.1899998188, 'd7': 7.03400015831, 'd5': 2.20300006866}, 'd7': {'d6': 7.03400015831, 'r5': 3.53600001335, 'd8': 0.942000150681}, 'd4': {'r17': 4.90499997139, 'd5': 2.64700007439, 'd3': 1.57099986076, 'd22': 6.50600004196}, 'd5': {'d6': 2.20300006866, 'd4': 2.64700007439, 'r3': 2.96300005913}, 'd2': {'i1': 4.29799985886, 'r27': 3.52200007439, 'r2': 4.58299994469, 'd1': 2.3900001049}, 'd3': {'r25': 4.1360001564, 'r24': 5.03600001335, 'd4': 1.57099986076, 'r18': 3.45000004768, 'i6': 2.94499993324}, 'r21': {'d20': 4.3069999218}, 'd1': {'d2': 2.3900001049, 'r1': 3.63599991798}, 'd14': {'i2': 4.98699998856, 'r9': 2.44499993324, 'd13': 1.53499984741}, 'd15': {'i2': 3.81699991226, 'r12': 2.35400009155}, 'd16': {'r15': 4.74300003052, 'd17': 1.63700008392, 'i2': 5.57000017166, 'r13': 3.38599991798}, 'r24': {'i1': 3.60599994659, 'd23': 5.08400011063, 'i5': 3.617000103, 'i4': 5.08500003815, 'i6': 3.94299983978, 'r25': 4.875, 'd3': 5.03600001335}, 'd10': {'d9': 3.29799985886, 'r28': 4.18099999428, 'd11': 4.33200001717, 'r11': 4.74699997902}, 'd11': {'d10': 4.33200001717, 'd12': 3.10199999809, 'r10': 4.10699987411}, 'd12': {'r7': 2.40100002289, 'd11': 3.10199999809, 'd13': 4.13800001144}, 'd13': {'d14': 1.53499984741, 'r8': 4.10700011253, 'd12': 4.13800001144}, 'r23': {'d23': 3.12199997902, 'i5': 2.8100001812, 'i4': 3.52099990845}, 'd18': {'i3': 4.40499997139, 'r15': 2.69199991226, 'r19': 2.69500017166}, 'd19': {'d20': 4.86000013351, 'i3': 4.53600001335, 'r19': 3.0110001564, 'r20': 4.48300004005}, 'r22': {'d21': 3.54600000381}, 'r7': {'d12': 2.40100002289}, 'r20': {'d19': 4.48300004005}, 'r16': {'d25': 3.50899982452, 'd24': 3.73399996758}, 'r17': {'d4': 4.90499997139, 'd22': 5.17599987984, 'd25': 3.97300004959}, 'r14': {'d17': 3.66799998283, 'd24': 2.85100007057, 'd9': 3.64100003242}, 'r15': {'d16': 4.74300003052, 'd18': 2.69199991226}, 'r12': {'d15': 2.35400009155, 'r9': 6.19099998474}, 'r13': {'d16': 3.38599991798, 'i2': 3.75900006294}, 'r10': {'d11': 4.10699987411}, 'r11': {'d10': 4.74699997902}, 'i1': {'r27': 1.72899985313, 'r25': 5.59000015259, 'r24': 3.60599994659, 'd2': 4.29799985886, 'i6': 3.99799990654}, 'i3': {'d17': 3.61899995804, 'd18': 4.40499997139, 'd19': 4.53600001335, 'r19': 4.41199994087}, 'i2': {'d14': 4.98699998856, 'd15': 3.81699991226, 'd16': 5.57000017166, 'r13': 3.75900006294}, 'i5': {'d23': 2.492000103, 'r24': 3.617000103, 'r23': 2.8100001812, 'i4': 3.37199997902}, 'i4': {'i5': 3.37199997902, 'd22': 2.19499993324, 'r23': 3.52099990845, 'r24': 5.08500003815}, 'r18': {'d3': 3.45000004768}, 'r19': {'i3': 4.41199994087, 'd18': 2.69500017166, 'd19': 3.0110001564}, 'd17': {'i3': 3.61899995804, 'r14': 3.66799998283, 'd16': 1.63700008392}, 'i6': {'i1': 3.99799990654, 'r25': 3.02999997139, 'r24': 3.94299983978, 'd3': 2.94499993324}, 'r25': {'i1': 5.59000015259, 'r24': 4.875, 'd3': 4.1360001564, 'i6': 3.02999997139}, 'r4': {'d6': 4.1899998188}, 'r5': {'d7': 3.53600001335}, 'r6': {'d8': 4.27799987793}, 'r26': {'d23': 3.82299995422}, 'r1': {'d1': 3.63599991798}, 'r2': {'d2': 4.58299994469}, 'r3': {'d5': 2.96300005913}, 'd21': {'d20': 3.26300001144, 'd22': 0.75, 'r22': 3.54600000381}, 'd20': {'d21': 3.26300001144, 'd19': 4.86000013351, 'r21': 4.3069999218}, 'd23': {'r27': 4.132999897, 'r26': 3.82299995422, 'r24': 5.08400011063, 'r23': 3.12199997902, 'i5': 2.492000103}, 'd22': {'d21': 0.75, 'r17': 5.17599987984, 'd4': 6.50600004196, 'i4': 2.19499993324}, 'd25': {'r16': 3.50899982452, 'r17': 3.97300004959, 'd24': 5.5569999218}, 'r9': {'d14': 2.44499993324, 'r12': 6.19099998474}}
		self.x_interval = 49.5310535431

		self.y_interval = 15.585151673
		self.block_length = 30
		self.X = X
		self.Y = Y

		self.not_accept = 0
		self.max_x = 54.8262786865
		self.max_y = 116.043502808
		self.min_x = 5.29522514343
		self.min_y = 100.458351135
		self.first = {}
		self.realcoords = {'i2': (1314.4666099551, 334.1016387800002), 'i4': (413.86186599710004, 358.02848815999994), 'd1': (59.09059524540001, 122.757469177), 'd20': (576.2655639661, 358.02848815999994), 'i6': (302.13452339310004, 122.757469177), 'i3': (888.3309745791001, 358.02848815999994), 'd3': (440.14753341610003, 122.757469177), 'd7': (750.9888458261, 122.757469177), 'd21': (528.0551719671, 358.02848815999994), 'd17': (1045.8063316331, 358.02848815999994), 'd10': (1080.2295494071, 122.757469177), 'd23': (181.0536003111, 358.02848815999994), 'd4': (484.3179321281001, 122.757469177), 'd2': (101.3434791565, 122.757469177), 'd12': (1205.3714561451, 122.757469177), 'd15': (1410.2708244321, 358.02848815999994), 'd22': (488.8001251211, 358.02848815999994), 'd8': (798.0337142931, 122.757469177), 'd18': (893.9424324041, 443.5736083900001), 'd19': (735.0291252141, 358.02848815999994), 'i5': (314.64849472109995, 358.02848815999994), 'd24': (852.5046730041, 181.79016113), 'd11': (1139.0028953560998, 122.757469177), 'd14': (1338.5239982591, 122.757469177), 'd5': (519.3291854861, 122.757469177), 'd13': (1238.7587547310998, 122.757469177), 'd25': (685.9490203851001, 182.63839721), 'i1': (199.13586616409998, 122.757469177), 'd6': (556.5843391421, 122.757469177), 'd9': (1028.4362983701, 122.757469177), 'd16': (1112.2620964040998, 358.02848815999994), 'r6': (836.8966484061, 40.984344469999996), 'r13': (1221.5526008600998, 442.30941772999984), 'r2': (140.0877571107, 40.984344469999996), 'r16': (769.3161964431, 242.0687866), 'r10': (1208.3315849301, 242.0687866), 'r26': (139.24541473410002, 442.30941772999984), 'r11': (1104.0789985671, 242.0687866), 'r27': (146.62187576309998, 242.0687866), 'r28': (1041.3950157171, 40.984344469999996), 'r4': (601.3193321241, 40.984344469999996), 'r3': (486.2891578671001, 40.984344469999996), 'r5': (726.3007163991001, 40.984344469999996), 'r1': (30.0, 40.984344469999996), 'r21': (602.3769950871001, 442.30941772999984), 'r9': (1460.1206016530998, 40.984344469999996), 'r22': (486.5650749201001, 442.30941772999984), 'r14': (973.9640235891001, 242.0687866), 'r15': (1017.3795890811, 442.30941772999984), 'r24': (309.41579818710005, 242.0687866), 'r25': (298.7769985191, 40.984344469999996), 'r19': (811.0143470751001, 442.30941772999984), 'r12': (1455.9316062920998, 242.0687866), 'r20': (710.7092285151001, 442.30941772999984), 'r17': (591.1514854431, 242.0687866), 'r8': (1289.8702812201, 40.984344469999996), 'r7': (1177.7297401431001, 40.984344469999996), 'r23': (292.82268524209996, 442.30941772999984), 'r18': (433.5044860851001, 242.0687866)}
		self.robot_x = self.realcoords[start_point][0]
		self.robot_y = self.realcoords[start_point][1]
		self.robot_point = start_point
		self.start = start_point
		self.goal = goal
		self.speed = speed
		self.wait_time = wait_time
		self.cur_time = start_time


		#Define RL stuff
		self.reward = reward
		self.mode = mode
		self.finalQ = finalQ
		self.time_slot = time_slot
		self.RL = QLearn(self.adj.keys(),self.adj,self.cost,self.reward,self.mode,self.time_slot, self.goal,self.finalQ,start_time)

		#COLOR:
		self.white = (255, 255, 255)
		self.black = (0, 0, 0)
		self.grey = (210, 210, 210)
		self.red = (255, 0, 0)
		self.green = (0, 255, 0)
		self.blue = (0, 0, 128)

		#Define Crowd:
		self.human_points = human_points

	def update_human_feedback(self,social,effective):
		self.human_effective = effective
		self.human_social = social

	def get_human_feedback(self):
		return (self.human_effective, self.human_social)

	def draw_wall(self,screen,color):

		#Draw border
		pg.draw.line(screen,color,(0,500),(1550,500))

		#Drawing the first line wall
		#r1 wall
		point = self.realcoords['r1']
		x = point[0]
		y = point[1]

		second_y = y+140
		third_y = y + 370
		pg.draw.line(screen,color,[x+60,0],[x+60,y+60])

		pg.draw.line(screen, color, [0,y+60 ], [x + 30, y + 60])

		#Draw left border
		pg.draw.line(screen,color,[x+60,second_y],[x+60,500])

		pg.draw.line(screen,color,[0,second_y],[x+60,second_y])

		pg.draw.line(screen,color,[x+60,third_y],[x+150,third_y])


		# r2 wall
		x = self.realcoords['r2'][0]
		pg.draw.line(screen,color,[x+60,0],[x+60,y+60])

		pg.draw.line(screen, color, [x + 60, y+60], [x -20, y + 60])

		#Use R2 right wall coordinates
		pg.draw.line(screen,color,[x+60,second_y],[x+60,second_y+150])
		pg.draw.line(screen,color,[x+60,third_y],[x+60,500])

		#r25 wall
		x = self.realcoords['r25'][0]
		pg.draw.line(screen,color,[x+150,0],[x+150,y+60])
		pg.draw.line(screen, color, [x + 150, y+60], [x + 220, y + 60])

		#r3 wall
		x = self.realcoords['r3'][0]
		pg.draw.line(screen, color, [x + 60, 0], [x + 60, y + 60])

		#r4 wall
		x = self.realcoords['r4'][0]
		pg.draw.line(screen, color, [x + 60, 0], [x + 60, y + 60])
		pg.draw.line(screen, color, [x + 60, y + 60], [x -10, y + 60])
		pg.draw.line(screen, color, [x + 60, y + 60], [x +130, y + 60])

		#r5 wall
		x = self.realcoords['r5'][0]
		pg.draw.line(screen, color, [x + 60, 0], [x + 60, y + 60])

		#r6 wall
		x = self.realcoords['r6'][0]
		pg.draw.line(screen, color, [x + 100, 0], [x + 100, y + 60])
		pg.draw.line(screen, color, [x -20, y+60], [x + 100, y + 60])

		#r28 wall
		x = self.realcoords['r28'][0]
		pg.draw.line(screen, color, [x + 60, 0], [x + 60, y + 60])
		pg.draw.line(screen, color, [x +60, y+60], [x + 150, y + 60])

		#r7 wall
		x = self.realcoords['r7'][0]
		pg.draw.line(screen, color, [x + 60, 0], [x + 60, y + 60])

		#r8 wall
		x = self.realcoords['r8'][0]
		pg.draw.line(screen, color, [x + 60, 0], [x + 60, y + 60])
		pg.draw.line(screen, color, [x + -30, y + 60], [x + 60, y + 60])

		#r8 wall
		x = self.realcoords['r8'][0]
		pg.draw.line(screen, color, [x + 60, 0], [x + 60, y + 60])
		pg.draw.line(screen, color, [x + -30, y + 60], [x + 60, y + 60])

		#Draw Third
		#r24 wall
		x = self.realcoords['r24'][0]
		y = self.realcoords['r24'][1]
		pg.draw.line(screen, color, [x + 90, second_y], [x + 90, second_y+150])
		pg.draw.line(screen, color, [x + 90, second_y], [x + 130, second_y])

		#r18 wall
		pg.draw.line(screen, color, [x + 90, y + 50], [x + 170, y + 50])
		pg.draw.line(screen,color,[x+170,second_y],[x+170,second_y+150])

		#r17 wall
		x = self.realcoords['r17'][0]
		pg.draw.line(screen,color,[x-50,second_y],[x+440,second_y])
		pg.draw.line(screen,color,[x-60,second_y+150],[x+110,second_y+150])
		pg.draw.line(screen,color,[x+110,second_y+150],[x+110,second_y+40])

		#r16 wall
		pg.draw.line(screen,color,[x+110,second_y+150],[x+280,second_y+150])
		pg.draw.line(screen,color,[x+280,second_y+150],[x+280,second_y+40])

		#r14 wall
		pg.draw.line(screen,color,[x+280,second_y+150],[x+440,second_y+150])

		#r11 wall
		x = self.realcoords['r11'][0]
		pg.draw.line(screen,color,[x-30,second_y],[x-30,second_y+150])
		pg.draw.line(screen,color,[x+30,second_y],[x+30,second_y+150])
		pg.draw.line(screen,color,[x-5,second_y],[x+30,second_y])
		pg.draw.line(screen,color,[x-30,second_y+150],[x+30,second_y+150])

		#r10 wall
		pg.draw.line(screen,color,[x+30,second_y+150],[x+170,second_y+150])
		pg.draw.line(screen,color,[x+170,second_y],[x+170,second_y+150])
		pg.draw.line(screen,color,[x+170,second_y],[x+80,second_y])

		#r12 wall
		x = self.realcoords['r12'][0]
		pg.draw.line(screen,color,[x-160,second_y+150],[x-160,second_y])
		pg.draw.line(screen,color,[x-160,second_y+150],[x-100,second_y+150])
		pg.draw.line(screen,color,[x-160,third_y],[1550,third_y])
		pg.draw.line(screen, color, [x - 160, third_y], [x-160, 500])

		#r23 wall
		x = self.realcoords['r23'][0]
		pg.draw.line(screen,color,[x+130,third_y],[x+130,500])
		pg.draw.line(screen,color,[x+130,third_y],[x+190,third_y])

		#r22 wall
		x = self.realcoords['r22'][0]
		pg.draw.line(screen,color,[x+70,third_y],[x+70,500])

		#r21 wall

		x = self.realcoords['r21'][0]
		pg.draw.line(screen,color,[x+50,third_y],[x+50,500])
		pg.draw.line(screen,color,[x,third_y],[x+125,third_y])
		pg.draw.line(screen,color,[x+170,third_y],[x+170,500])

		#r19 wall
		x = self.realcoords['r19'][0]
		pg.draw.line(screen,color,[x+ 60,third_y],[x+60,third_y + 20])
		pg.draw.line(screen, color, [x + 60, third_y+75], [x + 60, 500])
		pg.draw.line(screen,color,[x+60,third_y],[x+ 260,third_y])
		pg.draw.line(screen, color, [x + 310, third_y], [x + 310, 500])

	def draw_keypoints(self,screen,color):
		font = pg.font.Font('freesansbold.ttf', 17)
		white = (255,255,255)
		black = (0,0,0)
		for point in self.coords:
			x,y = self.realcoords[point]
			rec = pg.Rect(x,y,self.block_length,self.block_length)
			pg.draw.rect(screen,color,rec)
			text = font.render(point, True, black, white)
			textRect = text.get_rect()
			textRect.center = (x+15,y+15)
			screen.blit(text,textRect)


	def draw_path(self,screen,color):
		count = []
		for point in self.adj:
			start = self.realcoords[point]
			for adj_point in self.adj[point]:
				same = True
				end = self.realcoords[adj_point]
				for check in count:
					if point in check and adj_point in check and len(check) == len(point) + len(adj_point):
						same = False
				if same:
					draw_dashed_line(screen, color, start, end)
					count.append(point+adj_point)


	def draw_feedback(self,black,white,screen):
		# Drawing Feedback Tag
		font = pg.font.Font('freesansbold.ttf', 40)
		social_text = font.render('Social:', True, black, white)
		effective_text = font.render("Effect:", True, black, white)

		social_textRect = social_text.get_rect()
		social_textRect.center = (300, 620)
		screen.blit(social_text, social_textRect)

		effective_textRect = effective_text.get_rect()
		effective_textRect.center = (800, 620)
		screen.blit(effective_text, effective_textRect)

	def draw_startendTag(self,screen,flags,black,white):
		# Draw tag on the map
		screen.blit(flags[0], (self.realcoords[self.start][0], self.realcoords[self.start][1] - 30))
		screen.blit(flags[1], (self.realcoords[self.goal][0], self.realcoords[self.goal][1] - 30))

		# Start End Tag
		font = pg.font.Font('freesansbold.ttf', 20)
		start_text = font.render('Start:', True, black, white)
		end_text = font.render("End:", True, black, white)

		start_textRect = start_text.get_rect()
		start_textRect.center = (1300, 550)
		screen.blit(start_text, start_textRect)

		end_textRect = end_text.get_rect()
		end_textRect.center = (1300, 650)
		screen.blit(end_text, end_textRect)

		screen.blit(flags[0], (1400, 520))
		screen.blit(flags[1], (1400, 620))

	def draw_time(self,screen,black,white):
		font = pg.font.Font('freesansbold.ttf', 20)
		time_tag = font.render('Time: ', True, black, white)
		time_tagRect = time_tag.get_rect()
		time_tagRect.center = (60, 550)
		screen.blit(time_tag, time_tagRect)

		time_text = font.render(str(round(self.cur_time,4)), True, black, white)
		time_textRect = time_text.get_rect()
		time_textRect.center = (200, 550)
		screen.blit(time_text, time_textRect)

	def build_default(self,screen,flags):

		screen.fill(self.white)
		self.draw_keypoints(screen, self.grey)
		self.draw_wall(screen, self.black)
		self.draw_path(screen, self.grey)
		self.draw_feedback(self.black, self.white, screen)
		self.draw_startendTag(screen, flags, self.black, self.white)
		self.draw_time(screen,self.black,self.white)

		# Draw robot
		rec = pg.Rect(self.robot_x + 10, self.robot_y + 10, 10, 10)
		pg.draw.rect(screen, self.red, rec)

	def draw_robot(self,screen,next_goal,next_goal_point,goal_x,goal_y,flags):
		clock = pg.time.Clock()
		robot_point = self.realcoords[self.robot_point]
		slope = (self.robot_y- goal_y)/(self.robot_x-next_goal_point[0])
		step_length = (goal_x-self.robot_x)/self.speed
		for i in range(self.speed):
			for event in pg.event.get():
				if event.type == pg.QUIT:
					return False
			self.robot_x += step_length
			self.robot_y += step_length * slope

			self.build_default(screen, flags)

			#Show Selected next goal
			draw_dashed_line(screen,self.red,robot_point,next_goal_point)

			clock.tick(self.speed)
		self.robot_point = next_goal

		return True

	def make_decision(self):
		state = (self.robot_point,self.cur_time)
		ifRandom = False
		if ifRandom:
		#Currently just random choice need to add RL
			next_goal = random.choice(list(self.adj[self.robot_point]))
			next_goal_point = self.realcoords[next_goal]
			goal_x = self.realcoords[next_goal][0]
			goal_y = self.realcoords[next_goal][1]
		else:
			#Update Human feedback to Q-table
			self.RL.HumanFeedback(self.score_list,state)
			action = self.RL.chooseAction(state)
			print("Action: ", action)
			self.RL.learn(state,self.reward,action)
			self.cur_time += self.cost[self.robot_point][action]
			next_goal = action
			next_goal_point = self.realcoords[next_goal]
			goal_x = self.realcoords[next_goal][0]
			goal_y = self.realcoords[next_goal][1]
		return next_goal,next_goal_point,goal_x,goal_y



	def get_next_goal(self,buttons,screen,flags,human):

		h_pos = (700,350)
		buttons.draw_button(screen)
		human.draw_human(h_pos)
		possible_choice = list(self.adj[self.robot_point])
		self.score_list = {}
		while(len(possible_choice) > 0):
			buttons.social_score = 0
			buttons.effective_score = 0
			selected = False

			timeout = time.time() + self.wait_time
			next_goal = random.choice(possible_choice)
			self.build_default(screen, flags)
			draw_dashed_line(screen, self.red, self.realcoords[self.robot_point], self.realcoords[next_goal])
			buttons.draw_button(screen)
			human.draw_human(h_pos)
			pg.display.update()
			while not selected and time.time() <= timeout:
				for event in pg.event.get():
					if event.type == pg.QUIT:
						return (0,0,0,0,False)
				buttons.event_handler()
				if buttons.social_score != 0 and buttons.effective_score != 0:
					selected = True
			self.human_social = buttons.social_score
			self.human_effective = buttons.effective_score
			self.score_list[next_goal] = [self.human_social, self.human_effective]
			possible_choice.remove(next_goal)
		next_goal,next_goal_point,goal_x,goal_y = self.make_decision()
		return (next_goal,next_goal_point, goal_x, goal_y,True)

	def start_map(self):
		pg.init()
		screen = pg.display.set_mode((self.X,self.Y))
		run = True
		good = pg.image.load("good.jpg").convert()
		socialgood = pg.transform.scale(good,(220,70))
		effectgood = pg.transform.scale(good,(220,70))
		bad = pg.image.load("bad.jpg").convert()
		socialbad = pg.transform.scale(bad, (220, 70))
		effectbad = pg.transform.scale(bad, (220, 70))

		#Define Human
		pic_one = pg.image.load("human_one.png").convert()
		pic_one_tran= pg.transform.scale(pic_one, (10, 30))
		human_one = Human(pic_one_tran,screen)


		pic_two = pg.image.load("human_one.png").convert()
		pic_two_tran = pg.transform.scale(pic_two, (220, 70))
		human_two = Human(pic_two_tran, screen)


		pic_three = pg.image.load("human_one.png").convert()
		pic_three_tran = pg.transform.scale(pic_three, (220, 70))
		human_three = Human(pic_three_tran, screen)


		start = pg.image.load("start.png").convert()
		start = pg.transform.scale(start,(30,40))

		end = pg.image.load("end.png").convert()
		end = pg.transform.scale(end,(30,40))

		flags = []
		flags.append(start)
		flags.append(end)
		button_list = Buttons()
		button_list.add_button('socialgood',(400,520),socialgood,"good")
		button_list.add_button('socialbad',(400, 620), socialbad, "bad")
		button_list.add_button('effectgood',(900,520), effectgood, "good")
		button_list.add_button('effectbad',(900, 620), effectbad, "bad")
		while run:
			pg.time.delay(100)
			for event in pg.event.get():
				if event.type == pg.QUIT:
					run = False
			if not run:
				break
			#Restart the Run
			#Need to pause and ask if continue
			if self.robot_point == self.goal:
				self.robot_point = self.start
				self.robot_x = self.realcoords[self.start][0]
				self.robot_y = self.realcoords[self.start][1]

			(next_goal,next_goal_point, goal_x, goal_y,run) = self.get_next_goal(button_list,screen,flags,human_one)
			if not run:
				break
			run = self.draw_robot(screen,next_goal,next_goal_point,goal_x,goal_y,flags)

			if not run:
				break
		pg.quit()

speed = 10
screen_resize_parameter = 1
start = 'd2'
end = 'd10'
wait_time = 30
reward = 0
mode = "separate"
time_slot =20
finalQ = 10000
human_points = [['d19','d20']]
start_time = 8*20
human_time = 9

M = Map(1550,700,start,end,speed,wait_time,reward,mode,time_slot,finalQ,human_points,start_time)

max_time = 7.81200003624
min_time = 0.75

M.start_map()