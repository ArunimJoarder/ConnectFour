# import pygame
import connect_four as cf
import numpy as np
import random
import time

TOTAL = 10
NO_AB = 0
NO_MC = 0
NO_DRAW = 0
DEPTH = 6

TIME_MM = 0
TIME_AB = 0

for times in range(TOTAL):
    refBoard = cf.create_board()
    gameover = False
    draw = 0

    turn = 0

    timeAB = 0
    timeMM = 0

    NoOfAB = 0
    NoOfMM = 0
    while not gameover:
        timeTaken1 = 0
        timeTaken2 = 0
        if turn == 0:
            NoOfMM += 1
            start1 = time.time()
            col = cf.move_selector(refBoard, DEPTH, turn + 1, 'MM')
            if cf.check_column(refBoard, col):
                row = cf.last_row(refBoard, col)
                tempRow, tempCol = cf.drop_coin(refBoard, row, col, turn + 1)
            else:
                continue
            if cf.checkDraw(refBoard):
                gameover = True
                draw = 5
                # pygame.display.update()
                print("DRAW")
                cf.print_board(refBoard)
                end1 = time.time()

            if cf.win_cond(refBoard, turn + 1):
                gameover = True
                # pygame.display.update()
                print("MC WINS")
                cf.print_board(refBoard)
                print()
                end1 = time.time()

            turn += 1
            turn %= 2
            end1 = time.time()
            timeTaken1 = end1 - start1
            timeMM += timeTaken1

        else:
            NoOfAB += 1
            start2 = time.time()
            col = cf.move_selector(refBoard, DEPTH, turn + 1, 'AB')
            if cf.check_column(refBoard, col):
                row = cf.last_row(refBoard, col)
                tempRow, tempCol = cf.drop_coin(refBoard, row, col, turn + 1)
            else:
                continue
                
            if cf.checkDraw(refBoard):
                gameover = True
                draw = 5
                # pygame.display.update()
                print("DRAW")
                cf.print_board(refBoard)
                print()
                end2 = time.time()

            if cf.win_cond(refBoard, turn + 1):
                gameover = True
                # pygame.display.update()
                print("AB WINS")
                cf.print_board(refBoard)
                print()
                end2 = time.time()

            turn += 1
            turn %= 2
            end2 = time.time()
            timeTaken2 = end2 - start2
            timeAB += timeTaken2
        print(timeTaken1, timeTaken2)
    
    timeAB = timeAB/NoOfAB
    timeMM = timeMM/NoOfMM
    
    if draw:
        NO_DRAW += 1
    elif turn == 0:
        NO_AB += 1
    elif turn == 1:
        NO_MC += 1

    TIME_AB += timeAB
    TIME_MM += timeMM

    print("No Of Games = ", times + 1)
    print("NO_AB = ", NO_AB)
    print("NO_MM = ", NO_MC)
    print("NO_DRAW = ", NO_DRAW)
    print("Avg. timeAB = ", timeAB)
    print("Avg. timeMM = ", timeMM)
    print()


print("TOTAL = ", TOTAL)
print("NO_AB = ", NO_AB)
print("NO_MM = ", NO_MC)
print("NO_DRAW = ", NO_DRAW)
print("Avg. TIME_AB = ", TIME_AB/TOTAL)
print("Avg. TIME_MM = ", TIME_MM/TOTAL)
