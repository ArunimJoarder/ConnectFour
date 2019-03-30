#!/usr/bin/env python

import pygame
import connect_four as cf
import numpy as np
import random

pygame.init()

screenWidth = 800
screenHeight = 700
COLUMNS = 7
ROWS = 6
gapSize = 10
coinRadius = 40
boardWidth = COLUMNS*2*coinRadius + gapSize*(COLUMNS + 1)
boardHeight = ROWS*2*coinRadius + gapSize*(ROWS + 1)

NAVYBLUE = (10, 20, 255)
RED = (255, 0, 0)
YELLOW = (255, 255, 0)
BLACK = (0, 0, 0)


class Coin:
    def __init__(self, x, y, colour):
        self.x = x
        self.y = y
        self.colour = colour

    def dropGameCoin (self, win):
        pygame.draw.circle(win, self.colour, (int(self.x), int(self.y)), coinRadius)

class Board:
    def __init__(self, x, y, width, height, colour):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.colour = colour

    def drawBoard(self, win):
        pygame.draw.rect(win, self.colour, (self.x, self.y, self.width, self.height))

def startupDraw(win, board):
    board.drawBoard(win)
    for i in range(7):
        for j in range(6):
            circle = Coin((screenWidth - boardWidth)/2 + gapSize + coinRadius + i*(2*coinRadius + gapSize), (screenHeight - boardHeight)*2/3 + gapSize + coinRadius + j*(2*coinRadius + gapSize), BLACK)
            circle.dropGameCoin(win)

def convert_coordinates(i, j):
    return (screenHeight - boardHeight)*2/3 + gapSize + coinRadius + 5*(2*coinRadius + gapSize) - i*(2*coinRadius + gapSize), (screenWidth - boardWidth)/2 + gapSize + coinRadius + j*(2*coinRadius + gapSize)

def getCol(x):
    if x < (screenWidth - boardWidth)/2:
        return 0
    elif x > (screenWidth - boardWidth)/2 + boardWidth:
        return 6
    for i in range(7):
        if x > (screenWidth - boardWidth)/2 + gapSize + coinRadius + i*(2*coinRadius + gapSize) - coinRadius - gapSize/2 and x < (screenWidth - boardWidth)/2 + gapSize + coinRadius + i*(2*coinRadius + gapSize) + coinRadius + gapSize/2:
            return i

def coin_animation(win, x, color):
    pygame.draw.rect(win, BLACK, ((0,((screenHeight - boardHeight)*2//3 - 2*coinRadius - 10), screenWidth, 2*coinRadius + 10)))
    pygame.draw.circle(win, color, (x,(screenHeight - boardHeight)*2//3 - coinRadius - 5), coinRadius-2)
    pygame.display.update()

    
refBoard = cf.create_board()
playerColours = [RED, YELLOW]
gameBoard = Board((screenWidth - boardWidth)/2, (screenHeight - boardHeight)*2/3, boardWidth, boardHeight, NAVYBLUE)

vsComputer = 0
vsComputer = int(input("vs PLAYER(1) / vs COMPUTER(2) ? : ")) - 1

startWin = pygame.display.set_mode((screenWidth,screenHeight))
pygame.display.set_caption("ConnectFour")



startupDraw(startWin, gameBoard)
turn = 0
gameover = False
while not gameover:
    pygame.time.delay(10)
    
    pygame.display.update()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            gameover = True

        if vsComputer:
            if turn == 0:
                mouseClick = pygame.mouse.get_pressed()
                mouse_x, mouse_y = pygame.mouse.get_pos()
                coin_animation(startWin, mouse_x, playerColours[turn])
                if mouseClick[0] == 1:
                    pygame.draw.rect(startWin, BLACK, ((0,((screenHeight - boardHeight)*2//3 - 2*coinRadius - 10), screenWidth, 2*coinRadius + 10)))
                    col = getCol(mouse_x)
                    if cf.check_column(refBoard, col):
                        row = cf.last_row(refBoard, col)
                        tempRow, tempCol = cf.drop_coin(refBoard, row, col, turn + 1)
                        gameRow, gameCol = convert_coordinates(tempRow, tempCol)
                        coin_1 = Coin(gameCol, gameRow, playerColours[turn])
                        coin_1.dropGameCoin(startWin)
                    else:
                        continue

                    if cf.win_cond(refBoard, turn + 1):
                        gameover = True
                        pygame.display.update()
                        print("PLAYER ", turn + 1, "Wins!!")

                    turn += 1
                    turn %= 2

            else:
                col = cf.move_selector(refBoard, 4, turn + 1, 'alphaBeta')
                if cf.check_column(refBoard, col):
                    row = cf.last_row(refBoard, col)
                    tempRow, tempCol = cf.drop_coin(refBoard, row, col, turn + 1)
                    gameRow, gameCol = convert_coordinates(tempRow, tempCol)
                    coin_1 = Coin(gameCol, gameRow, playerColours[turn])
                    coin_1.dropGameCoin(startWin)
                else:
                    continue

                if cf.win_cond(refBoard, turn + 1):
                    gameover = True
                    pygame.display.update()
                    print("COMPUTER Wins!!")

                turn += 1
                turn %= 2

        else:
            mouseClick = pygame.mouse.get_pressed()
            mouse_x, mouse_y = pygame.mouse.get_pos()
            coin_animation(startWin, mouse_x, playerColours[turn])
            if mouseClick[0] == 1:
                col = getCol(mouse_x)
                if cf.check_column(refBoard, col):
                    row = cf.last_row(refBoard, col)
                    tempRow, tempCol = cf.drop_coin(refBoard, row, col, turn + 1)
                    gameRow, gameCol = convert_coordinates(tempRow, tempCol)
                    coin_1 = Coin(gameCol, gameRow, playerColours[turn])
                    coin_1.dropGameCoin(startWin)
                else:
                    continue

                if cf.win_cond(refBoard, turn + 1):
                    gameover = True
                    pygame.display.update()
                    print("PLAYER", turn + 1, "Wins!!")

                turn += 1
                turn %= 2


pygame.quit()