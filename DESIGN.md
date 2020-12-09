# Beating the World's Hardest Game - Design Document

### Gamemodes:
Gamemode 0: Player Version - try to beat the World's Hardest Game yourself!
Gamemode 1: Training Version - watch our genetic learning model in action as it learns (from scratch) to beat the game
Gamdemode 2: Watch Version - watch a trained model beat the game!

## Recreating the World's Hardest Game using Pygame

First, we created our own version of the World's Hardest Game in Pygame. To do so, we created a generalized grid-based board which could be used for our different levels. We also created classes for the player, obstacles, and goal which could be generalized to run each of our levels. 

The various gamemodes and display options are implemented using a series of while loops - within the outermost game loop, we have a homepage loop which welcomes the user and prompts them to choose between our 3 gamemodes. If the user selects Gamemode 0 (Player Version), we render a simple board with the obstacles, player, and goal for Level 1. Player movement is controlled by keyboard arrows - allowing the player to move in 4 directions (up, down, left, right) where each direction is represented by a unit vector stored in a tuple. At each position, we check for collisions with obstacles, walls, and the goal. If the player hits an obstacle, the player dot is returned to the start. If the player reaches the goal, then the next level is generated. If the user selects Gamemode 1 or 2, the levelSelect while loop allows them to select between Levels 1-3 to either train or watch. The train gamemode generates a population of size 500 (population class explained in Genetic Learning Algorithm section) and the watch gamemode generates a single trained dot. 

At any point in the game in any of the gamemodes, users can press H to return to homepage, which breaks out of the gamemode-specific while loop and returns to the general gamemode loop. This allows users to easily switch to a different gamemode and/or level.

talk about making new levels (walls and obstacles)

## Pathfinding Algorithm

---

## Genetic Learning Algorithm - Reinforcement Learning

For the genetic learning algorithm, we created classes for the Brain, Dot, and Population. The Brain class contains functions to randomize movement, clone brains, and mutate brains. The Dot class contains functions to display dot movement and updates, as well as to calculate the fitness of the dot (as explained in the Pathfinding Algorithm section), and make a baby dot by cloning it using the clone function from Brain. The Population class applies the functions defined in Dot to every dot in the population. The Population class also finds the best dot in the current generation by using linear search for the index of the dot with the highest fitness. A "natural selection" function copies this best dot to the new generation as well as selects parents for the remaining dots in the population based on fitness scores. For each dot in the new generation (with the exception of the best dot), we mutuate it at a mutation rate of 0.02. We also created functions to save and upload trained data using Python's pickle module to save the direction vectors of the best dot in binary code. This is useful for gamemode 2, which allows users to load in a trained model and watch it beat the game. Dots are considered "dead" once they 1) collide with an obstacle or 2) exceed the max steps (which is increased by 20 steps every 30 generations - this allows the program to train more quickly and focus on smaller segments of the path at a time). A function in Population called allDotsDead() returns True once all dots are dead or if a dot has reached the goal, marking the end of a generation.

Our algorithm was based on https://github.com/Code-Bullet/Smart-Dots-Genetic-Algorithm-Tutorial however included significant changes to accomodate for the different game environemnt (Pygame), different language (Python), and a completely new rewards system that is based on our path finding algorithm rather than a straight path distance. 

---

A “design document” for your project in the form of a Markdown file called DESIGN.md that discusses, technically, how you implemented your project and why you made the design decisions you did. Your design document should be at least several paragraphs in length. Whereas your documentation is meant to be a user’s manual, consider your design document your opportunity to give the staff a technical tour of your project underneath its hood.
