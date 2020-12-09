# Beating the World's Hardest Game - Design Document

### Gamemodes:
Gamemode 0: Player Version - try to beat the World's Hardest Game yourself!

Gamemode 1: Training Version - watch our genetic learning model in action as it learns (from scratch) to beat the game!

Gamdemode 2: Watch Version - watch a trained model beat the game!

## Recreating the World's Hardest Game using Pygame

First, we created our own version of the World's Hardest Game in Pygame. To do so, we created a generalized grid-based board which could be used for our different levels. This decision was made to simplify the movement and animations of the player, dots, and obstacles throughout the course, and reduced the amount of arithmetic that needed to be done during the process. The general class also allowed for more general reusability within the program. We also created classes for the player, obstacles, and goal which could be generalized to run each of our levels. The classes contain functions to draw and get the position of the object, as well as move and update, if necessary.

The various gamemodes and display options are implemented using a series of while loops. Within the outermost game loop, we have a homepage loop which welcomes the user and prompts them to choose between our 3 gamemodes. If the user selects Gamemode 0 (Player Version), we render a simple board with the obstacles, player, and goal for Level 1. Player movement is controlled by keyboard arrows - allowing the player to move in 4 directions (up, down, left, right) where each direction is represented by a unit vector stored in a tuple. At each position, we check for collisions with obstacles, walls, and the goal. If the player hits an obstacle, the player dot is returned to the start. If the player reaches the goal, then the next level is generated. If the user selects Gamemode 1 or 2, the levelSelect while loop allows them to select between Levels 1-3 to train or watch. The train gamemode generates a population of size 500 (population class explained in Genetic Learning Algorithm section) and the watch gamemode generates a single trained dot. 

At any point in the game in any of the gamemodes, users can press H to return to homepage, which breaks out of the gamemode-specific while loop and returns to the general homepage loop. This allows users to easily switch to a different gamemode and/or level.

To create each level, we passed in binary files defining the locations of walls and obstacles. The location of walls are specified using a list of grid pieces from the board. Obstacles were created using the general Obstacle class as well a tuple containing their starting location. We then used Python's pickle module to convert our wall and obstacle lists into binary files that the program could read when called. This was done more for style as opposed to code design, as it kept the code clearer with less need to define obstacles or walls for each level in a file such as `game.py`.

## Genetic Learning Algorithm - Reinforcement Learning

For the genetic learning algorithm, we created classes for the Brain, Dot, and Population. The Brain class contains functions to randomize movement, clone brains, and mutate brains. The Dot class contains functions to display dot movement and updates, as well as to calculate the fitness of the dot (as explained in the Pathfinding Algorithm section), and make a baby dot by cloning it using the clone function from Brain. The Population class applies the functions defined in Dot to every dot in the population. The Population class also finds the best dot in the current generation by using linear search for the index of the dot with the highest fitness. A "natural selection" function copies this best dot to the new generation as well as selects parents for the remaining dots in the population based on fitness scores. Specifically, this was designed to prefer more successful parents, with the likelihood of reproduction being directly proportional to the fitness function.

For each dot in the new generation (with the exception of the best dot), we mutuate it at a mutation rate of 0.02. Empirically, we found this to maintain most of the progress that was made between generations while also allowing for enough change to occur to stimulate new progress. We also created functions to save and upload trained data using Python's pickle module to save the direction vectors of the best dot in binary code. This is useful for gamemode 2, which allows users to load in a trained model and watch it beat the game. Dots are considered "dead" once they 1) collide with an obstacle or 2) exceed the max steps (which is increased by 20 steps every 30 generations - this allows the program to train more quickly and focus on smaller segments of the path at a time). A function in Population called allDotsDead() returns True once all dots are dead or if a dot has reached the goal, marking the end of a generation.

Our algorithm was based on https://github.com/Code-Bullet/Smart-Dots-Genetic-Algorithm-Tutorial, however included significant changes in regards to the different game environment (Pygame), different language (Python), and a completely new rewards system that is based on our path finding algorithm rather than a straight path distance. 

---

## Pathfinding Algorithm

The aforementioned pathfinding algorithm was used in the fitness function of each dot. This algorithm is based on a breadth-first search, combining algorithms described [here](https://www.educative.io/edpresso/how-to-implement-a-breadth-first-search-in-python) and [here](https://www.codementor.io/blog/basic-pathfinding-explained-with-python-5pil8767c1). In short, the algorithm takes a 2D array representing the game board. Initially, it is filled with 0s (representing empty, usable spaces) and -1s (walls). Then, the board is labelled based on distance from the start, where the start is represented by a 1, each adjacent point by a 2, and so on. This is done using a FIFO queue, where the value of 1 is set at the start point, then the starting point is added to the queue. Every time a coordinate pair exits the queue, all adjacent, not-yet-filled squares are given a value of one higher within the board, then added to the queue so that the next set of squares can be labelled. This continues until the goal is reached. Then, to return a path of tuples (positions) to the fitness function, the board is traversed in reverse, from goal to start, with each tile added to the path having a value one less than the previous. This backtracking prevents the algorithm from getting stuck in potential dead-ends within the level. The path is then reversed (to go from start to finish), then used in the fitness function.

---

A “design document” for your project in the form of a Markdown file called DESIGN.md that discusses, technically, how you implemented your project and why you made the design decisions you did. Your design document should be at least several paragraphs in length. Whereas your documentation is meant to be a user’s manual, consider your design document your opportunity to give the staff a technical tour of your project underneath its hood.
