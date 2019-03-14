#!/usr/bin/env python

import numpy
from copy import deepcopy
import random

No_ROW = 6
No_COLUMN = 7

def create_board():
    board = numpy.zeros((No_ROW, No_COLUMN))
    return board

def check_column(board, column):
    return board[0][column] == 0

def last_row(board, column):
    for row in range(No_ROW):
        if board[No_ROW - row - 1][column] == 0:
            return No_ROW - row - 1

def drop_coin(board, row, column, coin):
    board[row][column] = coin

def valid_pos(board, row, column):
    if row == No_ROW - 1:
        return True
    elif row < No_ROW - 1:
        if board[row + 1, column] != 0 and valid_pos(board, row + 1, column):
            return True
        else:
            return False
                    

def win_cond(board, coin_type):
    for i in range(No_ROW-1, -1, -1):
        for j in range(No_COLUMN):
            try:
                if board[i][j]  == board[i+1][j] == board[i+2][j] == board[i+3][j] == coin_type:
                    return True
            except IndexError:
                pass

            try:
                if board[i][j]  == board[i][j+1] == board[i][j+2] == board[i][j+3] == coin_type:
                    return True
            except IndexError:
                pass

            try:
                if not j + 3 > No_COLUMN and board[i][j] == board[i+1][j + 1] == board[i+2][j + 2] == board[i+3][j + 3] == coin_type:
                    return True
            except IndexError:
                pass

            try:
                if not j - 3 < 0 and board[i][j] == board[i+1][j - 1] == board[i+2][j - 2] == board[i+3][j - 3] == coin_type:
                    return True
            except IndexError:
                pass
    return False

def score(board,row, column, coin_type):
    count_hor = 0
    count_ver = 0
    count_diag_r = 0
    count_diag_l = 0
    score_h = 0
    score_v = 0
    score_l = 0
    score_r = 0

    # HorizontalCheck
    for i in range(1,4):
        if column + i > No_COLUMN - 1:
            break
        
        if board[row][column + i] == coin_type:
            count_hor += 1
        else:
            break
    
    for i in range(1,4):
        if column - i < 0:
            break
        
        if board[row][column - i] == coin_type:
            count_hor += 1
        else:
            break
    ##

    # VerticalCheck
    for i in range(1,4):
        if row + i > No_ROW - 1:
            break
        
        if board[row + i][column] == coin_type:
            count_ver += 1
        else:
            break
    ##

    # DiagonalLeftCheck
    for i in range(1,4):
        if row - i < 0 or column - i < 0:
            break
        
        if valid_pos(board, row - i, column - i):
            if board[row - i][column - i] == coin_type:  
                count_diag_l += 1
            else:
                break
        else:
            break

    for i in range(1,4):
        if column + i > No_COLUMN - 1 or row + i > No_ROW - 1:
            break
        
        if valid_pos(board, row + i, column + i):
            if board[row + i][column + i] == coin_type:
                count_diag_l += 1
            else:
                break
    ##

    # DiagonalRightCheck
    for i in range(1,4):
        if row + i < 0 or column - i < 0:
            break
        
        if valid_pos(board, row + i, column - i):
            if board[row + i][column - i] == coin_type:  
                count_diag_r += 1
            else:
                break
        else:
            break

    for i in range(1,4):
        if column + i > No_COLUMN - 1 or row - i > No_ROW - 1:
            break
        
        if valid_pos(board, row - i, column + i):
            if board[row - i][column + i] == coin_type:
                count_diag_r += 1
            else:
                break
    ##

    score_h = 10**count_hor - (not count_hor)
    score_v = 10**count_ver - (not count_ver)
    score_l = 10**count_diag_l - (not count_diag_l)
    score_r = 10**count_diag_r - (not count_diag_r)
    return max(max(score_h, score_l), max(score_r, score_v))

# Main Game Code
turn = 1

board = create_board()

game_over = False

vsComputer = int(input("VS: Computer(1) / Player(2) ? : " ))
print(board)
print("\n")

while not game_over:

    # Player1 Turn
    if turn == 1:
        column = int(input("Player1 input selected column (1 - 7): ")) - 1

        if column > No_COLUMN - 1 or column < 0:
            print("Enter Valid Column")
            continue

        if check_column(board, column):
            row = last_row(board, column)
            drop_coin(board, row, column, turn)

            game_over = win_cond(board, turn)
            if game_over:
                print("\n\nGAME OVER\nPlayer1 Wins!!\n\n")
        
            turn = 2
        else:
            print("\n\nColumn is filled!\n\n")
    ##

    # Player2 Turn
    elif turn == 2 and vsComputer == 2:
        column = int(input("Player2 input selected column (1 - 7): ")) - 1

        if column > No_COLUMN - 1 or column < 0:
            print("Enter Valid Column")
            continue

        if check_column(board, column):
            row = last_row(board, column)
            drop_coin(board, row, column, turn)

            game_over = win_cond(board, turn)
            if game_over:
                print("\n\nGAME OVER\nPlayer2 Wins!!\n\n")
            
            turn = 1
        else:
            print("\n\nColumn is filled!\n\n")
    ##

    # AI Turn
    else:
        board_test = deepcopy(board)
        scores = numpy.zeros(No_COLUMN)
        scores_1 = numpy.zeros(No_COLUMN)
        scores_2 = numpy.zeros(No_COLUMN)
        for i in range(No_COLUMN):
            row_i = last_row(board_test, i)
            scores_2[i] = score(board_test, row_i, i, 2)
            scores_1[i] = score(board_test, row_i, i, 1)

        scores = scores_2 + scores_1
        print(scores, "\n")
        max_score = numpy.amax(numpy.array(scores))

        print(max_score, "\n")

        ind, = numpy.where(numpy.array(scores) == max_score)

        print(ind, "\n")

        column = random.choice(ind)
        row = last_row(board, column)

        drop_coin(board, row, column, turn)

        game_over = win_cond(board, turn)
        if game_over:
            print("\n\nGAME OVER\nCOMPUTER Wins!!\n\n")

        turn = 1
    ##
    print(board)
    print("\n")