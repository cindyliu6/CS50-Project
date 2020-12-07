# VERY LOOSELY BASED
# https://www.educative.io/edpresso/how-to-implement-a-breadth-first-search-in-python
# https://www.codementor.io/blog/basic-pathfinding-explained-with-python-5pil8767c1

def find_path(board, start, end):
    path = [end]

    queue = [start]
    currVal = 0

    start_x = start[1]
    start_y = start[0]
    board[start_x][start_y] = 1
    

    while queue:
        tile = queue.pop(0)

        if tile == end:
            break

        y = tile[0]
        x = tile[1]

        currVal = board[x][y]

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

    path_not_found = True

    while path_not_found:
        lastTile = path[-1]

        y = lastTile[0]
        x = lastTile[1]
        lastVal = board[x][y]

        if board[x-1][y] == board[x][y] - 1:
            path.append((y, x-1))

        elif board[x+1][y] == board[x][y] - 1:
            path.append((y, x+1))

        elif board[x][y-1] == board[x][y] - 1:
            path.append((y-1, x))

        elif board[x][y+1] == board[x][y] - 1:
            path.append((y+1, x))

        path_end = path[-1]
        end_x = path_end[1]
        end_y = path_end[0]


        if board[end_x][end_y] == 1:
            path_not_found = False

        
    path.reverse()
    return path

        





