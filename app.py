import numpy as np
import math
# import pygame
import sys

ROW = 6
COL = 7

def createBoard():
    # Creating the 7 cols and 6 rows required for the game
    board = np.zeros((ROW,COL))
    return board

def addValueToBoard(board, row, col, value):
    # adds value to board where user specifies
    board[row][col] = value

def isValidMove(board, selection):
    # checking if col is empty
    return board[ROW - 1][selection] == 0

def findOpenRow(board, selection):
    for val in range(ROW):
        if board[val][selection] == 0:
            return val

def showBoard(board):
    # reversing board so that the 0,0 is left bottom
    print(np.flip(board, 0))

def checkForWin(board, lastValue):
    # check for horizontal 4 connected values
    # offset by 3 since we can't win if we start at index 4 through 6
    # TODO: remove magic numbers from both checks and turn offset dynamic
    for col in range(COL - 3):
        for row in range(ROW):
            if board[row][col] == lastValue and board[row][col + 1] == lastValue and board[row][col + 2] == lastValue and board[row][col + 3] == lastValue:
                return True
    # check for vertical 4 connected values
    for row in range(ROW - 3):
        for col in range(COL):
            if board[row][col] == lastValue and board[row + 1][col] == lastValue and board[row + 2][col] == lastValue and board[row + 3][col] == lastValue:
                return True

    # check for diagonal positive slope 4 connected values
    for row in range(ROW - 3):
        for col in range(COL - 3):
            if board[row][col] == lastValue and board[row + 1][col + 1] == lastValue and board[row + 2][col + 2] == lastValue and board[row + 3][col + 3] == lastValue:
                return True

    # check for diagonal negative slope 4 connected values
    for row in range(ROW - 3):
        for col in range(3, COL):
            if board[row][col] == lastValue and board[row + 1][col - 1] == lastValue and board[row + 2][col - 2] == lastValue and board[row + 3][col - 3] == lastValue:
                return True


board = createBoard()
game_over = False
turn = 0

while not game_over:
    # get player input
    if turn == 0:
        # User chooses a column to add value to
        # Converting user input to an integer
        select = int(input("Player 1 select a column in the range of 0, 6: "))
        # Checking if the user input is in the range of 0, 6
        if isValidMove(board, select):
            row = findOpenRow(board, select)
            addValueToBoard(board, row, select, 1)

            if checkForWin(board, 1):
                print("Player 1 wins!")
                game_over = True
    
    #get ai input
    else:
        select = int(input("Player 2 select a column in the range of 0, 6: "))
        # select = np.random.randint(0,7)
        if isValidMove(board, select):
            row = findOpenRow(board, select)
            addValueToBoard(board, row, select, 2)

    showBoard(board)

    # increasing turn by 1
    turn += 1

    # alternates between player 1 and ai turn
    turn = turn % 2