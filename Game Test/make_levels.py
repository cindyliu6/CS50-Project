import pickle
import os
from game import Obstacle

WIDTH = 60
HEIGHT = 40
walls = []

vel_left = 1
vel_right = -1
vel_up = -1
vel_down = 1

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

# pickle.dump(walls, open("walls_1.dat", "wb"))

# pickle.dump(walls, open("walls_2.dat", "wb"))
print(walls)

obstacles = [[
		Obstacle(31, 11, vel_left, 0, 40, 20, 10000, -100000),
		Obstacle(32, 12, vel_left, 0, 40, 20, 10000, -100000),
		Obstacle(33, 13, vel_left, 0, 40, 20, 10000, -100000),
		Obstacle(34, 14, vel_right, 0, 40, 20, 10000, -100000),
		Obstacle(35, 15, vel_right, 0, 40, 20, 10000, -100000),
		Obstacle(36, 16, vel_right, 0, 40, 20, 10000, -100000),
	],
	[
		(31, 11),
		(32, 12),
		(33, 13),
		(34, 14),
		(35, 15),
		(36, 16)
		]
]

obstacles_2 = [[
		Obstacle(20, 9, 0, vel_down, 40, 20, 30, 9),
		Obstacle(21, 9, 0, vel_down, 40, 20, 30, 9),
		Obstacle(22, 9, 0, vel_down, 40, 20, 30, 9),
		Obstacle(23, 9, 0, vel_down, 40, 20, 30, 9),
		Obstacle(24, 9, 0, vel_down, 40, 20, 30, 9),
		Obstacle(25, 9, 0, vel_down, 40, 20, 30, 9),
        Obstacle(26, 9, 0, vel_down, 40, 20, 30, 9),
        Obstacle(27, 9, 0, vel_down, 40, 20, 30, 9),
        Obstacle(28, 9, 0, vel_down, 40, 20, 30, 9),
        Obstacle(29, 9, 0, vel_down, 40, 20, 30, 9),
        Obstacle(30, 9, 0, vel_down, 40, 20, 30, 9),
        Obstacle(31, 30, 0, vel_up, 40, 20, 30, 9),
        Obstacle(32, 30, 0, vel_up, 40, 20, 30, 9),
        Obstacle(33, 30, 0, vel_up, 40, 20, 30, 9),
        Obstacle(34, 30, 0, vel_up, 40, 20, 30, 9),
        Obstacle(35, 30, 0, vel_up, 40, 20, 30, 9),
        Obstacle(36, 30, 0, vel_up, 40, 20, 30, 9),
        Obstacle(37, 30, 0, vel_up, 40, 20, 30, 9),
        Obstacle(38, 30, 0, vel_up, 40, 20, 30, 9),
        Obstacle(39, 30, 0, vel_up, 40, 20, 30, 9),
        Obstacle(40, 30, 0, vel_up, 40, 20, 30, 9),
        Obstacle(41, 30, 0, vel_up, 40, 20, 30, 9)
	],
	[
		(20, 9),
		(21, 9),
		(22, 9),
		(23, 9),
		(24, 9),
		(25, 9),
        (26, 9),
        (27, 9),
        (28, 9),
        (29, 9),
        (30, 9),
        (31, 30),
        (32, 30),
        (33, 30),
        (34, 30),
        (35, 30),
        (36, 30),
        (37, 30),
        (38, 30),
        (39, 30),
        (40, 30),
        (41, 30)

		]
]

#pickle.dump(obstacles, open("obs_1.dat", "wb"))

pickle.dump(obstacles_2, open("obs_2.dat", "wb"))