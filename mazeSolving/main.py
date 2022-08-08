import queue

import pygame

from Node import Node

# Initialize pygame
pygame.init()
clock = pygame.time.Clock()

# Create Window Variables
WINDOW_WIDTH = 500
ROWS = 10
GAP = WINDOW_WIDTH // ROWS
FPS = 5

# Create Window
window = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_WIDTH))
pygame.display.set_caption('Maze Solver')

# Initialize Colors
WHITE = (255, 255, 255)
GREY = (150, 150, 150)
BLACK = (0, 0, 0)
RED = (255, 0, 0)


def draw_grid(win, rows, width):
    """
    Draws Grid on pygame screen
    :param win: pygame window
    :param rows: int, number of rows and columns
    :param width: int, width of pygame window
    :return: None
    """

    gap = width // rows
    for i in range(rows):
        pygame.draw.line(win, GREY, (0, i * gap), (width, i * gap))
    for j in range(rows):
        pygame.draw.line(win, GREY, (j * gap, 0), (j * gap, width))


def make_grid(rows, gap):
    """
    Creates nested array of nodes
    :param rows: int, number of rows
    :param gap: int, width of each node
    :return: nested array of nodes
    """
    grid = []
    for i in range(rows):
        grid.append([])
        for j in range(rows):
            node = Node(i, j, gap, rows)
            grid[i].append(node)
    return grid


def draw(win, grid, rows, width):
    """
    Draws grid and nodes on pygame window
    :param win: pygame window
    :param grid: nested array of Nodes
    :param rows: int, number of rows
    :param width: int, width of pygame window
    :return:
    """
    win.fill(WHITE)
    for row in grid:
        for node in row:
            node.draw(win)
    draw_grid(win, rows, width)
    pygame.display.update()


def is_valid(path, grid):
    """
    Checks if new path is valid
    :param path: string, path
    :param grid: nested array of nodes
    :return: Boolean, True or False
    """
    row = 1
    col = 1
    for letter in path:
        if letter == "L":
            row -= 1
        if letter == "R":
            row += 1
        if letter == "U":
            col -= 1
        if letter == "D":
            col += 1
    if grid[row][col].color != BLACK:
        return True
    else:
        return False


def print_path(path, grid):
    """
    Draws path on pygame window
    :param path: string, path
    :param grid: nested array of nodes
    :return: Node
    """

    row = 1
    col = 1

    for letter in path:

        if letter == "L":
            row -= 1
        if letter == "R":
            row += 1
        if letter == "U":
            col -= 1
        if letter == "D":
            col += 1
        grid[row][col].make_blue()
    return grid[row][col]


def reverse_path(path, grid):
    """
    Reverses and Draws reversed path in red
    :param path: string, path
    :param grid: nested array of nodes
    :return: None
    """
    row = ROWS - 2
    col = ROWS - 2

    reverse_path = path[::-1]
    for letter in reverse_path:
        grid[row][col].make_red()
        if letter == "L":
            row += 1
        if letter == "R":
            row -= 1
        if letter == "U":
            col += 1
        if letter == "D":
            col -= 1
        grid[row][col].make_red()


def premade_maze(grid):
    """
    Draws premade maze
    :param grid: nested array of nodes
    :return: none
    """

    grid[6][1].make_black()
    grid[7][1].make_black()
    grid[2][2].make_black()
    grid[3][2].make_black()
    grid[4][2].make_black()
    grid[5][2].make_black()
    grid[6][2].make_black()
    grid[5][3].make_black()
    grid[5][4].make_black()
    grid[5][5].make_black()
    grid[4][5].make_black()
    grid[3][5].make_black()
    grid[3][4].make_black()
    grid[2][7].make_black()
    grid[3][7].make_black()
    grid[4][7].make_black()
    grid[5][7].make_black()
    grid[2][8].make_black()
    grid[7][4].make_black()
    grid[7][5].make_black()
    grid[7][6].make_black()
    grid[7][7].make_black()
    grid[7][8].make_black()


if __name__ == "__main__":
    # creates grid
    grid = make_grid(ROWS, GAP)
    # makes top left and bottom right corners the beginning and end of maze
    grid[1][1].make_red()
    grid[ROWS-2][ROWS-2].make_red()
    # creates premade grid
    premade_maze(grid)

    start = False

    # draws boundary of maze
    for j in range(ROWS):
        grid[0][j].make_black()
        grid[j][0].make_black()
        grid[ROWS-1][j].make_black()
        grid[j][ROWS-1].make_black()

    # creates queue of paths
    paths = queue.Queue()
    paths.put("")

    # create infinite loop
    run = True
    while run is True:
        clock.tick(30)
        draw(window, grid, ROWS, WINDOW_WIDTH)

        # if mouse is left-clicked and maze has not been locked,
        # make square black
        if pygame.mouse.get_pressed()[0] == 1 and start is False:
            mouse_x, mouse_y = pygame.mouse.get_pos()
            row = mouse_x // GAP
            col = mouse_y // GAP
            node = grid[row][col]
            node.make_black()

        # if mouse is right-clicked and maze has not been locked,
        # make square white
        if pygame.mouse.get_pressed()[2] == 1 and start is False:
            mouse_x, mouse_y = pygame.mouse.get_pos()
            row = mouse_x // GAP
            col = mouse_y // GAP
            node = grid[row][col]
            node.make_white()

        # if maze is locked
        if start is True:
            for event in pygame.event.get():
                # if a key is pressed
                if event.type == pygame.KEYDOWN:
                    # if the s key is pressed
                    if event.key == pygame.K_s:
                        for _ in range(paths.qsize()):
                            # get first path in queue
                            curr_path = paths.get()
                            # if the path is empty or the last move was not left
                            if curr_path == "" or curr_path[-1] != "L":
                                # move right
                                for i in ["R"]:
                                    new_path = curr_path + i
                                    # if right is valid move
                                    if is_valid(new_path, grid):
                                        # add new path to queue
                                        paths.put(new_path)

                            # if the path is empty or the last move was not right
                            if curr_path == "" or curr_path[-1] != "R":
                                # move left
                                for i in ["L"]:
                                    new_path = curr_path + i
                                    # if left is valid move
                                    if is_valid(new_path, grid):
                                        # add new path to queue
                                        paths.put(new_path)

                            # if the path is empty or the last move was not up
                            if curr_path == "" or curr_path[-1] != "U":
                                # move down
                                for i in ["D"]:
                                    # if down is valid move
                                    new_path = curr_path + i
                                    # add new path to queue
                                    if is_valid(new_path, grid):
                                        paths.put(new_path)

                            # if the path is empty or the last move was not down
                            if curr_path == "" or curr_path[-1] != "D":
                                # move up
                                for i in ["U"]:
                                    new_path = curr_path + i
                                    # if up is valid move
                                    if is_valid(new_path, grid):
                                        # add new path to queue
                                        paths.put(new_path)

                        # for every path in the queue
                        for _ in range(paths.qsize()):
                            path = paths.get()
                            # if the path ends at the end node
                            if print_path(path, grid) == grid[ROWS-2][ROWS-2]:
                                # break the loop
                                start = False
                                # print the path in red
                                reverse_path(path, grid)
                                break
                            # queue path again
                            paths.put(path)

        for event in pygame.event.get():
            # if x in top right of window is pressed
            if event.type == pygame.QUIT:
                # exit the window
                run = False
            # if a key is pressed
            if event.type == pygame.KEYDOWN:
                # if space is pressed
                if event.key == pygame.K_SPACE:
                    # lock the maze
                    start = True

    pygame.quit()
