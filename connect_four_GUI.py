#!/usr/bin/env python

import pygame
import connect_four as cf
import numpy as np

pygame.init()

screenWidth = 800
screenHeight = 700
COLUMNS = 7
ROWS = 6
gapSize = 10
coinRadius = 40
boardWidth = COLUMNS*2*coinRadius + gapSize*(COLUMNS + 1)
boardHeight = ROWS*2*coinRadius + gapSize*(ROWS + 1)

NAVYBLUE = (60, 60, 100)
RED = (255, 0, 0)
YELLOW = (255, 255, 0)
BLACK = (0, 0, 0)

startWin = pygame.display.set_mode((screenWidth,screenHeight))
pygame.display.set_caption("ConnectFour")

class Coin:
    def __init__(self, x, y, colour):
        x = self.x
        y = self.y
        colour = self.colour

    def dropGameCoin (self, win):
        pygame.draw.circle(win, self.colour, (self.x, self.y), coinRadius)

class Board:
    def __init__(self, x, y, width, height, colour):
        x = self.x
        y = self.y
        width = self.width
        height = self.height
        colour = self.colour

    def drawBoard(self, win):
        pygame.draw.rect(win, self.colour, (self.x, self.y, self.width, self.height))


refBoard = cf.create_board()
playerColours = [RED, YELLOW]

run = True
while(run):
    pygame.time.delay(100)
    
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False

    pygame.display.update()

pygame.quit()