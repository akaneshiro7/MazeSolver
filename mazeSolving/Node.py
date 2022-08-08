import pygame

class Node:
    def __init__(self, row, col, width, total_row):
        self.row = row
        self.col = col
        self.x = row * width
        self.y = col * width
        self.width = width
        self.total_row = total_row
        self.color = (255, 255, 255)

    def get_position(self):
        return self.row, self.col

    def make_black(self):
        self.color = (0, 0, 0)

    def make_white(self):
        self.color = (255, 255, 255)

    def make_blue(self):
        self.color = (0, 0, 255)

    def make_red(self):
        self.color = (255, 0, 0)

    def at_end(self):
        return self.color == (255, 0, 0)

    def draw(self, win):
        pygame.draw.rect(win, self.color, (self.x, self.y, self.width, self.width))

