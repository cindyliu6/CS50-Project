import pickle
import os
from game import Obstacle

WIDTH = 60
HEIGHT = 40
walls = []

vel_left = 1
vel_right = -1

for x in range(WIDTH):
	walls.append((x, 0))
	walls.append((x, HEIGHT-1))

for x in range(HEIGHT):
	walls.append((0, x))
	walls.append((WIDTH-1, x))

for x in range(HEIGHT-10):
	walls.append((18, x))

for x in range(10, HEIGHT):
	walls.append((42, x))

pickle.dump(walls, open("walls_1.dat", "wb"))
print(walls)

obstacles = [[
			Obstacle(31, 11, vel_left),
			Obstacle(32, 12, vel_left),
			Obstacle(33, 13, vel_left),
			Obstacle(34, 14, vel_right),
			Obstacle(35, 15, vel_right),
			Obstacle(36, 16, vel_right)
		],
		[
			(31, 11),
			(32,12),
			(33,13),
			(34,14),
			(35,15),
			(36,16)
			]
	]

pickle.dump(obstacles, open("obs_1.dat", "wb"))