# LOOSELY BASED ON
# https://www.educative.io/edpresso/how-to-implement-a-breadth-first-search-in-python
# https://www.codementor.io/blog/basic-pathfinding-explained-with-python-5pil8767c1

# BFS algorithm used in fitness function
# Finds path
def find_path(board, start, end):
    # Start path with last tile in path
    path = [end]

    # Put start in queue to chec
    queue = [start]

    # Tuple and array coordinates are flipped
    # Set val in board at start to 1
    start_x = start[1]
    start_y = start[0]
    board[start_x][start_y] = 1

    # While the queue is not empty
    while queue:
        # Remove first element from queue
        tile = queue.pop(0)

        # Break loop if at the end of the path
        if tile == end:
            break

        # Get the value of the tile that had been popped
        y = tile[0]
        x = tile[1]

        currVal = board[x][y]

        # For every tile not yet visited, set its value on the board to one higher
        # This basically gives min distance from start to each square
        # When this is done, every square from start up to path will be labelled with a value
        if not board[x+1][y]:
            board[x+1][y] = currVal + 1
            queue.append((y, x+1))

        if not board[x-1][y]:
            board[x-1][y] = currVal + 1
            queue.append((y, x-1))

        if not board[x][y+1]:
            board[x][y+1] = currVal + 1
            queue.append((y+1, x))

        if not board[x][y-1]:
            board[x][y-1] = currVal + 1
            queue.append((y-1, x))


    # See if path connecting start to finish is completed
    path_not_found = True

    # While the path is not found
    while path_not_found:
        # Use last value in path (closest in start)
        lastTile = path[-1]

        y = lastTile[0]
        x = lastTile[1]
        lastVal = board[x][y]

        # Search around for a square with a value one lower on the board and add to path
        # Go backward to forward to avoid dead ends
        # This path function was modified depending on which level was being trained
        if board[x-1][y] == board[x][y] - 1:
            path.append((y, x-1))

        elif board[x+1][y] == board[x][y] - 1:
            path.append((y, x+1))

        elif board[x][y-1] == board[x][y] - 1:
            path.append((y-1, x))

        elif board[x][y+1] == board[x][y] - 1:
            path.append((y+1, x))

        ## for Level 3, path alg change
        
        #if board[x][y-1] == board[x][y] - 1:
        #    path.append((y-1, x))

        #elif board[x][y+1] == board[x][y] - 1:
        #    path.append((y+1, x))

        #elif board[x-1][y] == board[x][y] - 1:
        #    path.append((y, x-1))

        #elif board[x+1][y] == board[x][y] - 1:
        #    path.append((y, x+1))


        # Check if the start has been reached
        path_end = path[-1]
        end_x = path_end[1]
        end_y = path_end[0]

        # When the start is reached, break out of loop
        if board[end_x][end_y] == 1:
            path_not_found = False

    # Reverse path so that it is now start to finish
    path.reverse()
    return path
