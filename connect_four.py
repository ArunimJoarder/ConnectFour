#!/usr/bin/env python

import numpy
from copy import deepcopy
import random
import math

No_ROW = 6
No_COLUMN = 7
DEPTH = 3

def create_board():
    board = numpy.zeros((No_ROW, No_COLUMN))
    return board

def check_column(board, column):
    return board[No_ROW - 1][column] == 0

def last_row(board, column):
    for row in range(No_ROW):
        if board[row][column] == 0:
            return row

def drop_coin(board, row, column, coin):
    board[row][column] = coin
    return row, column

def valid_pos(board, row, column):
    if row == 0:
        return True
    elif row > 0:
        if board[row - 1, column] != 0 and valid_pos(board, row - 1, column):
            return True
        else:
            return False
                    

def win_cond(board, coin_type):
    for i in range(No_ROW):
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

def checkDraw(board):
    for i in range(No_COLUMN):
        if check_column(board, i):
            return 0
    return 1

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
        if row - i < 0:
            break
        
        if board[row - i][column] == coin_type:
            count_ver += 1
        else:
            break
    ##

    # DiagonalLeftCheck
    for i in range(1,4):
        if row + i > No_ROW - 1 or column - i < 0:
            break
        
        if valid_pos(board, row + i, column - i):
            if board[row + i][column - i] == coin_type:  
                count_diag_l += 1
            else:
                break
        else:
            break

    for i in range(1,4):
        if column + i > No_COLUMN - 1 or row - i < 0:
            break
        
        if valid_pos(board, row - i, column + i):
            if board[row - i][column + i] == coin_type:
                count_diag_l += 1
            else:
                break
    ##

    # DiagonalRightCheck
    for i in range(1,4):
        if row - i < 0 or column - i < 0:
            break
        
        if valid_pos(board, row - i, column - i):
            if board[row - i][column - i] == coin_type:  
                count_diag_r += 1
            else:
                break
        else:
            break

    for i in range(1,4):
        if column + i > No_COLUMN - 1 or row + i > No_ROW - 1:
            break
        
        if valid_pos(board, row + i, column + i):
            if board[row + i][column + i] == coin_type:
                count_diag_r += 1
            else:
                break
    ##

    score_h = 10**count_hor - (not count_hor)
    score_v = 10**count_ver - (not count_ver)
    score_l = 10**count_diag_l - (not count_diag_l)
    score_r = 10**count_diag_r - (not count_diag_r)
    return max(max(score_h, score_l), max(score_r, score_v))

def boardScoreMax(scoreBoard):
    return numpy.amax(numpy.array(scoreBoard))
    
def miniMax(board, depth, turn):
    if depth == 0 or win_cond(board, 1) or win_cond(board, 2):
        scores = numpy.zeros(No_COLUMN)
        scores_1 = numpy.zeros(No_COLUMN)
        scores_2 = numpy.zeros(No_COLUMN)
        for i in range(No_COLUMN):
            if check_column(board, i):
                row_i = last_row(board, i)
                scores_2[i] = score(board, row_i, i, 2)
                scores_1[i] = score(board, row_i, i, 1)

        scores = scores_2 - scores_1

        scoreSum = 0
        for i in range(No_COLUMN):
            scoreSum += scores[i]

        return (-1**turn)*scoreSum

    if turn == 2:
        best_value = -math.inf
        for i in range(No_COLUMN):
            if check_column(board, i):
                board_test = deepcopy(board)
                row_i = last_row(board_test, i)

                if score(board_test, row_i, i, 1) >= 1000:
                    return math.inf
                
                drop_coin(board_test, row_i, i, turn)
                
                if win_cond(board_test, 2):
                    return math.inf
                else:   
                    value = miniMax(board_test, depth - 1, 1)

                if value >= best_value:
                    best_value = value

        return best_value

    else:
        best_value = math.inf
        for i in range(No_COLUMN):
            if check_column(board, i):
                board_test = deepcopy(board)
                row_i = last_row(board_test, i)

                if score(board_test, row_i, i, 2) >= 1000:
                    return -math.inf
                
                drop_coin(board_test, row_i, i, turn)
                
                if win_cond(board_test, 1):
                    return -1*math.inf
                else:   
                    value = miniMax(board_test, depth - 1, 2)

                if value <= best_value:
                    best_value = value

        return best_value

def alphaBeta(board, depth, alpha, beta, turn):
    if depth == 0 or win_cond(board, 1) or win_cond(board, 2):
        scores = numpy.zeros(No_COLUMN)
        scores_1 = numpy.zeros(No_COLUMN)
        scores_2 = numpy.zeros(No_COLUMN)
        for i in range(No_COLUMN):
            if check_column(board, i):
                row_i = last_row(board, i)
                scores_2[i] = score(board, row_i, i, 2)
                scores_1[i] = score(board, row_i, i, 1)

        scores = scores_2 + scores_1

        scoreSum = 0
        for i in range(No_COLUMN):
            scoreSum += scores[i]

        return (-1**turn)*scoreSum

    if turn == 2:
        best_value = -math.inf
        
        for i in range(No_COLUMN):
            if check_column(board, i):
                board_test = deepcopy(board)
                row_i = last_row(board_test, i)

                if score(board_test, row_i, i, 1) >= 1000:
                    return math.inf
                
                drop_coin(board_test, row_i, i, turn)
                
                if win_cond(board_test, 2):
                    return math.inf
                else:   
                    value = alphaBeta(board_test, depth - 1, alpha, beta, 1)

                if value >= best_value:
                    best_value = value
                
                alpha = max(alpha, value)

                if alpha >= beta:
                    break

        return best_value

    else:
        best_value = math.inf

        for i in range(No_COLUMN):
            if check_column(board, i):
                board_test = deepcopy(board)
                row_i = last_row(board_test, i)

                if score(board_test, row_i, i, 2) >= 1000:
                    return -math.inf
                
                drop_coin(board_test, row_i, i, turn)
                
                if win_cond(board_test, 1):
                    return -math.inf
                else:   
                    value = alphaBeta(board_test, depth - 1, alpha, beta, 2)

                if value <= best_value:
                    best_value = value

                beta = min(beta, value)

                if alpha >= beta:
                    break

        return best_value
        
bestScore = -math.inf
# bestMove = -1

class samples:
    def __init__(self):
        self.NoSAMPLES = 100000
        self.sampleCount = 0
        self.bestScore = -math.inf

    def check(self):
        if self.sampleCount <= self.NoSAMPLES//7:
            return 1
        return 0

    def reset(self):
        self.bestScore = -math.inf
        self.sampleCount = 0

def monteCarlo(board, depth, turn, a):
    if a.check():
        if depth == 0:
            a.sampleCount += 1
            scores = numpy.zeros(No_COLUMN)
            scores_1 = numpy.zeros(No_COLUMN)
            scores_2 = numpy.zeros(No_COLUMN)
            for i in range(No_COLUMN):
                if check_column(board, i):
                    row_i = last_row(board, i)
                    scores_2[i] = score(board, row_i, i, 2)
                    scores_1[i] = score(board, row_i, i, 1)

            scores = scores_2 + scores_1

            scoreSum = 0
            for i in range(No_COLUMN):
                scoreSum += scores[i]

            return (-1**turn)*scoreSum
        
        elif turn == 2:
            board_test = deepcopy(board)
            while 1:
                i = random.randrange(0, No_COLUMN)
                
                if check_column(board_test, i):
                    row_i = last_row(board_test, i)
                    if score(board_test, row_i, i, 1) >= 1000:
                        return -math.inf

                    drop_coin(board_test, row_i, i, turn)
                    if win_cond(board_test, 2):
                        return +math.inf
                    else:
                        value = monteCarlo(board_test, depth - 1, 1, a)

                        if value > a.bestScore:
                            a.bestScore = value
                            # bestMove = move
                return a.bestScore

        elif turn == 1:
            board_test = deepcopy(board)
            while 1:
                i = random.randrange(0, No_COLUMN)
                
                if check_column(board_test, i):
                    row_i = last_row(board_test, i)
                    if score(board_test, row_i, i, 2) >= 1000:
                        return math.inf

                    drop_coin(board_test, row_i, i, turn)
                    if win_cond(board_test, 1):
                        return -math.inf
                    else:
                        value = monteCarlo(board_test, depth - 1, 2, a)

                        if value > a.bestScore:
                            a.bestScore = value
                            # bestMove = move
                return a.bestScore
    return a.bestScore

def move_selector(board, depth, turn, Ptype):
    choices = numpy.zeros(No_COLUMN)
    for i in range(No_COLUMN):
        if check_column(board, i):
            board_test = deepcopy(board)
            row_i = last_row(board_test, i)
            drop_coin(board_test, row_i, i, turn)
            if Ptype == 'AB':
                choices[i] = alphaBeta(board_test, depth - 1, -math.inf, math.inf, 1)
            elif Ptype == 'MC':
                a = samples()
                choices[i] = monteCarlo(board_test, depth - 1, 1, a)
                a.reset()
            else:
                choices[i] = miniMax(board_test, depth - 1, 1)
        else:
            choices[i] = -math.inf

    while 1:
        max_score = boardScoreMax(choices)
        move = numpy.where(numpy.array(choices) == max_score)
        move = random.choice(move)
        move = random.choice(move)
        # print(choices)
        # print(move, '\n')
        
        if check_column(board, move):
            return move
        else:
            choices[move] = -math.inf



def print_board(board):
    print(numpy.flip(board, 0))
