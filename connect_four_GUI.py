#!/usr/bin/env python

import pygame
import connect_four as cf
import numpy as np
import random

pygame.init()

screenWidth = 800
screenHeight = 800
COLUMNS = 7
ROWS = 6
gapSize = 10
coinRadius = 40
boardWidth = COLUMNS*2*coinRadius + gapSize*(COLUMNS + 1)
boardHeight = ROWS*2*coinRadius + gapSize*(ROWS + 1)

bg1 = pygame.image.load('CFbg.jpg')
bg2 = pygame.image.load('CFbg1.jpg')
vsPBut = pygame.image.load('vsPlayer.jpg')
vsCBut = pygame.image.load('vsComp.jpg')

NAVYBLUE = (10, 20, 255)
RED = (255, 0, 0)
YELLOW = (255, 255, 0)
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)

refBoard = cf.create_board()
playerColours = [RED, YELLOW]

class Coin:
    def __init__(self, x, y, colour):
        self.x = x
        self.y = y
        self.colour = colour

    def dropGameCoin (self, win):
        pygame.draw.circle(win, self.colour, (int(self.x), int(self.y) + 5), coinRadius)

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
    win.blit(bg2, (0,0))
    # board.drawBoard(win)
    for i in range(6):
        for j in range(7):
            gameRow, gameCol = convert_coordinates(i, j)
            if(refBoard[i][j] != 0):
                circle = Coin(gameCol, gameRow - 1, playerColours[int(refBoard[i][j] - 1)])
                circle.dropGameCoin(startWin)
            # else:
            #     circle = Coin(gameCol, gameRow, BLACK)
            #     circle.dropGameCoin(startWin)
    pygame.display.update()

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

def coin_animation(win, x, color, board):
    # pygame.draw.rect(win, BLACK, ((0,((screenHeight - boardHeight)*2//3 - 2*coinRadius - 10), screenWidth, 2*coinRadius + 10)))
    startupDraw(win, board)
    pygame.draw.circle(win, color, (x,(screenHeight - boardHeight)*2//3 - coinRadius - 5), coinRadius-2)
    pygame.display.update()

def firstWindow(win):
    win.blit(bg1, (0,0))
    # pygame.draw.rect(win, YELLOW, (screenWidth / 4 - screenWidth / 6, screenHeight / 2 - screenHeight / 10, screenWidth / 3, screenHeight / 5))
    # pygame.draw.rect(win, RED, (3*screenWidth / 4 - screenWidth / 6, screenHeight / 2 - screenHeight / 10, screenWidth / 3, screenHeight / 5))
    win.blit(vsPBut, (screenWidth / 4 - 265//2, screenHeight / 2 - 300))
    win.blit(vsCBut, (3*screenWidth / 4 - 265//2, screenHeight / 2 - 300))    
    pygame.display.update()
def lastWindow(win, winner, vsComp):
    win.blit(bg1, (0,0))
    fontObj = pygame.font.Font('freesansbold.ttf', 80)
    if winner == 1:
        textSurfaceObj = fontObj.render('Player-1 WINS !!!!', True,WHITE,BLACK)
    elif winner == 0 and vsComp == 0:
        textSurfaceObj = fontObj.render('Player-2 WINS !!!!', True,WHITE,BLACK)
    elif winner == 0 and vsComp == 1:
        textSurfaceObj = fontObj.render('Computer WINS !!!!', True,WHITE,BLACK)
    else:
        textSurfaceObj = fontObj.render('DRAW', True,WHITE,BLACK)


    textRectObj = textSurfaceObj.get_rect()
    textRectObj.center = (screenWidth/2, screenHeight/2)
    win.blit(textSurfaceObj, textRectObj)
    pygame.display.update()


refBoard = cf.create_board()
playerColours = [RED, YELLOW]
gameBoard = Board((screenWidth - boardWidth)/2, (screenHeight - boardHeight)*2/3, boardWidth, boardHeight, NAVYBLUE)

# vsComputer = 0
# vsComputer = int(input("vs PLAYER(1) / vs COMPUTER(2) ? : ")) - 1

startWin = pygame.display.set_mode((screenWidth,screenHeight))
pygame.display.set_caption("ConnectFour")

firstWindow(startWin)

vsComputer = -1
while vsComputer == -1:
    for event in pygame.event.get():
        mouseClick = pygame.mouse.get_pressed()
        mouse_x, mouse_y = pygame.mouse.get_pos()
        # print(mouseClick)
        if mouseClick[0] == 1:
            
            if mouse_x < screenWidth / 2 - 20:
                vsComputer = 0
            elif mouse_x > screenWidth / 2 + 20:
                vsComputer = 1
    # print(1)
    # pygame.time.delay(500)

# print(vsComp)

startupDraw(startWin, gameBoard)
turn = 0
gameover = False
quitFlag = 1
while not gameover:
    pygame.time.delay(10)
    
    pygame.display.update()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            gameover = True
            quitFlag = 0

        if vsComputer:
            if turn == 0:
                mouseClick = pygame.mouse.get_pressed()
                mouse_x, mouse_y = pygame.mouse.get_pos()
                coin_animation(startWin, mouse_x, playerColours[turn], gameBoard)
                if mouseClick[0] == 1:
                    print("Player Chance\n")
                    # pygame.draw.rect(startWin, BLACK, ((0,((screenHeight - boardHeight)*2//3 - 2*coinRadius - 10), screenWidth, 2*coinRadius + 10)))
                    col = getCol(mouse_x)
                    if cf.check_column(refBoard, col):
                        row = cf.last_row(refBoard, col)
                        tempRow, tempCol = cf.drop_coin(refBoard, row, col, turn + 1)
                        gameRow, gameCol = convert_coordinates(tempRow, tempCol)
                        coin_1 = Coin(gameCol, gameRow - 1, playerColours[turn])
                        coin_1.dropGameCoin(startWin)
                    else:
                        continue

                    if cf.win_cond(refBoard, turn + 1):
                        gameover = True
                        pygame.display.update()
                        print("PLAYER ", turn + 1, "Wins!!")
                        cf.print_board(refBoard)

                    turn += 1
                    turn %= 2

            else:
                startupDraw(startWin, gameBoard)
                col = cf.move_selector(refBoard, 6, turn + 1, 'AB')
                if cf.check_column(refBoard, col):
                    row = cf.last_row(refBoard, col)
                    tempRow, tempCol = cf.drop_coin(refBoard, row, col, turn + 1)
                    gameRow, gameCol = convert_coordinates(tempRow, tempCol)
                    coin_1 = Coin(gameCol, gameRow - 1, playerColours[turn])
                    coin_1.dropGameCoin(startWin)
                    coin_animation(startWin, screenWidth // 2, playerColours[turn - 1], gameBoard)
                else:
                    continue

                if cf.win_cond(refBoard, turn + 1):
                    gameover = True
                    pygame.display.update()
                    print("COMPUTER Wins!!")
                    cf.print_board(refBoard)

                turn += 1
                turn %= 2

        else:
            # pygame.event.wait()
            mouseClick = pygame.mouse.get_pressed()
            mouse_x, mouse_y = pygame.mouse.get_pos()
            coin_animation(startWin, mouse_x, playerColours[turn], gameBoard)
            if mouseClick[0] == 1:
                col = getCol(mouse_x)
                if cf.check_column(refBoard, col):
                    row = cf.last_row(refBoard, col)
                    tempRow, tempCol = cf.drop_coin(refBoard, row, col, turn + 1)
                    gameRow, gameCol = convert_coordinates(tempRow, tempCol)
                    coin_1 = Coin(gameCol, gameRow - 1, playerColours[turn])
                    coin_1.dropGameCoin(startWin)
                else:
                    continue

                if cf.win_cond(refBoard, turn + 1):
                    gameover = True
                    pygame.display.update()
                    print("PLAYER", turn + 1, "Wins!!")
                    cf.print_board(refBoard)

                turn += 1
                turn %= 2

    if gameover:
        if quitFlag:
            pygame.time.delay(2000)

# for event in pygame.event.get():
#     # mouseClick = pygame.mouse.get_pressed()
#     print(1)
#     # while mouseClick[0] == 0:
#     lastWindow(startWin, turn, vsComputer)
#     if event == pygame.MOUSEBUTTONUP.:
#         break
lastWindow(startWin, turn, vsComputer)
pygame.time.delay(500)
pygame.quit()