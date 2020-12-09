import pickle
import os
from game import Obstacle

# THIS FILE STORES ALL DATA FOR FILES

# DATA FOR EVERY LEVEL
WIDTH = 60
HEIGHT = 40
walls = []

vel_left = 1
vel_right = -1
vel_up = -1
vel_down = 1

## DATA FOR WALLS OF LEVEL ONE AND TWO AND FOUR
#for x in range(WIDTH):
#	walls.append((x, 0))
#	walls.append((x, HEIGHT-1))

#for x in range(HEIGHT):
#	walls.append((0, x))
#	walls.append((WIDTH-1, x))

#for x in range(HEIGHT-10):
#	walls.append((18, x))

#for x in range(10, HEIGHT):
#	walls.append((42, x))

#for x in range(13):
#	walls.append((x, 9))
#	walls.append((x, 27))

#for x in range(6, 18):
#	walls.append((x, 18))

## SAVING WALLS 1 AND 2 AND 4

# pickle.dump(walls, open("walls_1.dat", "wb"))

# pickle.dump(walls, open("walls_2.dat", "wb"))
#pickle.dump(walls, open("walls_4.dat", "wb"))

## WALL DATA FOR LEVEL 3
#for x in range(WIDTH):
#	walls.append((x, 0))
#	walls.append((x, HEIGHT-1))

#for x in range(HEIGHT):
#	walls.append((0, x))
#	walls.append((WIDTH-1, x))

#for x in range(WIDTH - 10):
#	walls.append((x, 10))

#for x in range(10, WIDTH):
#	walls.append((x, 30))

# SAVE WALL DATA FOR LEVEL 3
#pickle.dump(walls, open("walls_3.dat", "wb"))

## WALL DATA FOR LEVEL 5

for x in range(WIDTH):
	walls.append((x, 0))
	walls.append((x, HEIGHT-1))

for x in range(HEIGHT):
	walls.append((0, x))
	walls.append((WIDTH-1, x))

for x in range(HEIGHT-20):
	walls.append((42,x))

for x in range(30, HEIGHT):
	walls.append((42, x))

for x in range(13):
	walls.append((x, 9))

for x in range(18, 42):
	walls.append((x, 9))

## SAVE WALL DATA FOR LEVEL 5
pickle.dump(walls, open("walls_5.dat", "wb"))
print(walls)
# OBSTACLE DATA FOR LEVEL 1
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

# OBSTACLE DATA FOR LEVEL 2
obstacles_2 = [[
		Obstacle(20, 9, 0, vel_down, 40, 20, 38, 2),
		Obstacle(21, 9, 0, vel_down, 40, 20, 38, 2),
		Obstacle(22, 9, 0, vel_down, 40, 20, 38, 2),
		Obstacle(23, 9, 0, vel_down, 40, 20, 38, 2),
		Obstacle(24, 9, 0, vel_down, 40, 20, 38, 2),
		Obstacle(25, 9, 0, vel_down, 40, 20, 38, 2),
        Obstacle(26, 9, 0, vel_down, 40, 20, 38, 2),
        Obstacle(27, 9, 0, vel_down, 40, 20, 38, 2),
        Obstacle(28, 9, 0, vel_down, 40, 20, 38, 2),
        Obstacle(29, 9, 0, vel_down, 40, 20, 38, 2),
        Obstacle(30, 9, 0, vel_down, 40, 20, 38, 2),
        Obstacle(31, 30, 0, vel_up, 40, 20, 38, 2),
        Obstacle(32, 30, 0, vel_up, 40, 20, 38, 2),
        Obstacle(33, 30, 0, vel_up, 40, 20, 38, 2),
        Obstacle(34, 30, 0, vel_up, 40, 20, 38, 2),
        Obstacle(35, 30, 0, vel_up, 40, 20, 38, 2),
        Obstacle(36, 30, 0, vel_up, 40, 20, 38, 2),
        Obstacle(37, 30, 0, vel_up, 40, 20, 38, 2),
        Obstacle(38, 30, 0, vel_up, 40, 20, 38, 2),
        Obstacle(39, 30, 0, vel_up, 40, 20, 38, 2),
        Obstacle(40, 30, 0, vel_up, 40, 20, 38, 2),
        Obstacle(41, 30, 0, vel_up, 40, 20, 38, 2)
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

# OBSTACLE DATA FOR LEVEL 3
obstacles_3 = [[

		Obstacle(47, 11, 0, vel_down, 40, 20, 28, 12),
		Obstacle(46, 11, 0, vel_down, 40, 20, 28, 12),
		Obstacle(45, 11, 0, vel_down, 40, 20, 28, 12),
		Obstacle(44, 11, 0, vel_down, 40, 20, 28, 12),
		Obstacle(43, 11, 0, vel_down, 40, 20, 28, 12),
		Obstacle(42, 11, 0, vel_down, 40, 20, 28, 12),
		Obstacle(41, 11, 0, vel_down, 40, 20, 28, 12),
		Obstacle(40, 11, 0, vel_down, 40, 20, 28, 12),
		Obstacle(35, 28, 0, vel_up, 40, 20, 28, 12),
		Obstacle(34, 28, 0, vel_up, 40, 20, 28, 12),
		Obstacle(33, 28, 0, vel_up, 40, 20, 28, 12),
		Obstacle(32, 28, 0, vel_up, 40, 20, 28, 12),
		Obstacle(31, 28, 0, vel_up, 40, 20, 28, 12),
		Obstacle(30, 28, 0, vel_up, 40, 20, 28, 12),
		Obstacle(10, 12, vel_right, vel_down, 26, 10, 28, 12),
		Obstacle(2, 30, vel_right, 0, 8, 2, 40, 0),
		Obstacle(3, 30, vel_right, 0, 8, 2, 40, 0),
		Obstacle(53, 10, vel_right, 0, 57, 51, 40, 0),
		Obstacle(54, 10, vel_right, 0, 57, 51, 40, 0)

	],
	[
		(47, 11),
		(46, 11),
		(45, 11),
		(44, 11),
		(43, 11),
		(42, 11),
		(41, 11),
		(40, 11),
		(35, 28),
		(34, 28),
		(33, 28),
		(32, 28),
		(31, 28),
		(30, 28),
		(10, 12),
		(2, 30),
		(3, 30),
		(53, 10),
		(54, 10)
		]
]
obstacles_4 = [[

		Obstacle(38, 11, vel_left, 0, 40, 20, 10000, -100000),
		Obstacle(37, 12, vel_left, 0, 40, 20, 10000, -100000),
		Obstacle(36, 13, vel_left, 0, 40, 20, 10000, -100000),
		Obstacle(35, 14, vel_left, 0, 40, 20, 10000, -100000),
		Obstacle(34, 15, vel_left, 0, 40, 20, 10000, -100000),
		Obstacle(33, 16, vel_left, 0, 40, 20, 10000, -100000),
		Obstacle(32, 17, vel_left, 0, 40, 20, 10000, -100000),
		Obstacle(31, 18, vel_left, 0, 40, 20, 10000, -100000),
		Obstacle(30, 19, vel_left, 0, 40, 20, 10000, -100000),
		Obstacle(29, 20, vel_left, 0, 40, 20, 10000, -100000),
		Obstacle(28, 21, vel_left, 0, 40, 20, 10000, -100000),
		Obstacle(27, 22, vel_left, 0, 40, 20, 10000, -100000),
	],
	[
		(38, 11),
		(37, 12),
		(36, 13),
		(35, 14),
		(34, 15),
		(33, 16),
		(32, 17),
		(31, 18),
		(30, 19),
		(29, 20),
		(28, 21),
		(27, 22)
		]
]
obstacles_5 = [[

		Obstacle(37, 11, 0, vel_down, 40, 20, 37, 11),
		Obstacle(36, 11, 0, vel_down, 40, 20, 37, 11),
		Obstacle(35, 11, 0, vel_down, 40, 20, 37, 11),
		Obstacle(34, 11, 0, vel_down, 40, 20, 37, 11),
		Obstacle(33, 11, 0, vel_down, 40, 20, 37, 11),
		Obstacle(32, 11, 0, vel_down, 40, 20, 37, 11),
		Obstacle(27, 20, 0, vel_up, 40, 20, 37, 11),
		Obstacle(26, 20, 0, vel_up, 40, 20, 37, 11),
		Obstacle(25, 20, 0, vel_up, 40, 20, 37, 11),
		Obstacle(24, 20, 0, vel_up, 40, 20, 37, 11),
		Obstacle(23, 20, 0, vel_up, 40, 20, 37, 11),
		Obstacle(22, 20, 0, vel_up, 40, 20, 37, 11),
		Obstacle(45, 30, vel_left, 0, 57, 44, 100, -100),
		Obstacle(46, 30, vel_left, 0, 57, 44, 100, -100),
		Obstacle(42, 23, 0, vel_up, 40, 20, 28, 21),
		Obstacle(42, 22, 0, vel_up, 40, 20, 28, 21)
	],
	[
		(37, 11),
		(36, 11),
		(35, 11),
		(34, 11),
		(33, 11),
		(32, 11),
		(27, 20),
		(26, 20),
		(25, 20),
		(24, 20),
		(23, 20),
		(22, 20),
		(45, 30),
		(46, 30),
		(42, 23),
		(42, 22)

		]
]


## SAVING DATA FOR OBSTACLES

#pickle.dump(obstacles, open("obs_1.dat", "wb"))
#pickle.dump(obstacles_2, open("obs_2.dat", "wb"))
#pickle.dump(obstacles_3, open("obs_3.dat", "wb"))
#pickle.dump(obstacles_4, open("obs_4.dat", "wb"))
pickle.dump(obstacles_5, open("obs_5.dat", "wb"))
