import numpy as np
import math
import random

ROW = 6
COL = 7
HUMAN = 0
AI = 1
HUMAN_VALUE = 1
AI_VALUE = 2
game_over = False
DEPTH = 6
# this is the amount of values we need to connect in order to win
GROUP = 4
turn = random.randint(HUMAN, AI)

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

# TODO: remove magic numbers from both checks and turn offset dynamic
def checkForWin(board, lastValue):
    # check for horizontal 4 connected values
    # offset by 3 since we can't win if we start at index 4 through 6
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

def evaluateGroup(group, value):
    score = 0
    temp_value = HUMAN_VALUE
    if value == HUMAN_VALUE:
        temp_value = AI_VALUE

    if group.count(value) == GROUP:
        score += 100
    elif group.count(value) == GROUP - 1 and group.count(0) == 1:
        score += 5
    elif group.count(value) == GROUP - 2 and group.count(0) == 2:
        score += 2

    if group.count(temp_value) == GROUP - 1 and group.count(0) == 1:
        score -= 4

    return score

def scorePosition(board, value):
    score = 0

    # center column preference
    middle_array = [int(i) for i in list(board[:, COL // 2])]
    middle_value = middle_array.count(value)
    score += middle_value * 3

    # horizontal score
    for row in range(ROW):
        # get the entire row
        row_array = [int(i) for i in list(board[row, :])]
        for col in range(COL - 3):
            group = row_array[col:col + GROUP]
            score += evaluateGroup(group, value)
    
    # vertical score
    for col in range(COL):
        col_array = [int(i) for i in list(board[:, col])]
        for row in range(ROW - 3):
            group = col_array[row:row + GROUP]
            score += evaluateGroup(group, value)

    # diagonal positive slope score
    for row in range(ROW - 3):
        for col in range(COL - 3):
            group = [board[row + i][col + i] for i in range(GROUP)]
            score += evaluateGroup(group, value)
    
    # diagonal negative slope score
    for row in range(ROW - 3):
        for col in range(COL - 3):
            group = [board[row + 3 - i][col + i] for i in range(GROUP)]
            score += evaluateGroup(group, value)

    return score

def checkTerminalNode(board):
    # checks if the game is over
    return checkForWin(board, HUMAN_VALUE) or checkForWin(board, AI_VALUE) or len(getValidCol(board)) == 0

def minmax(board, depth, alpha, beta, maximizingPlayer):
    valid = getValidCol(board)
    isTerminal = checkTerminalNode(board)

    if depth == 0 or isTerminal:
        if isTerminal:
            if checkForWin(board, AI_VALUE):
                return (None, 1000000000)
            elif checkForWin(board, HUMAN_VALUE):
                return (None, -1000000000)
            #no more valid moves
            else:
                return (None, 0)
        else:
            return (None, scorePosition(board, AI_VALUE))

    if maximizingPlayer:
        value = -math.inf
        best_col = random.choice(valid)
        for col in valid:
            row = findOpenRow(board, col)
            temp_board = board.copy()
            addValueToBoard(temp_board, row, col, AI_VALUE)
            new_score = minmax(temp_board, depth - 1, alpha, beta, False)[1]
            if new_score > value:
                value = new_score
                best_col = col
            alpha = max(alpha, value)
            if alpha >= beta:
                break
        return best_col, new_score

    else:
        value = math.inf
        best_col = random.choice(valid)
        for col in valid:
            row = findOpenRow(board, col)
            temp_board = board.copy()
            addValueToBoard(temp_board, row, col, HUMAN_VALUE)
            new_score = minmax(temp_board, depth - 1, alpha, beta, True)[1]
            if new_score < value:
                value = new_score
                best_col = col
            beta = min(beta, value)
            if alpha >= beta:
                break
        return best_col, new_score

def getValidCol(board):
    # gets all valid columns
    valid_cols = []
    for col in range(COL):
        if isValidMove(board, col):
            valid_cols.append(col)
    return valid_cols

def pickOptimalMove(board, value):
    valid = getValidCol(board)
    optimal_score = 0
    optimal_col = random.choice(valid)

    for col in valid:
        row = findOpenRow(board, col)
        temp_board = board.copy()
        addValueToBoard(temp_board, row, col, value)
        score = scorePosition(temp_board, value)
        if score > optimal_score:
            optimal_score = score
            optimal_col = col

    return optimal_col

# creating the empty board to start the game
board = createBoard()

while not game_over:
    print(turn, '\n')
    # get player input
    if turn == HUMAN:
        # User chooses a column to add value to
        # Converting user input to an integer
        select = int(input("\nPlayer 1 select a column in the range of 0, 6:\t"))
        # Checking if the user input is in the range of 0, 6
        if isValidMove(board, select):
            row = findOpenRow(board, select)
            addValueToBoard(board, row, select, HUMAN_VALUE)

            if checkForWin(board, HUMAN_VALUE):
                print('\n',"Player 1 wins!", '\n')
                game_over = True
                break
            
            # increasing turn by 1 if not winning move and valid move
            turn += 1
            # alternates between player 1 and ai turn
            turn = turn % 2
            
    
    #process ai turn
    if turn == AI:
        # selects a random location for AI to add value to
        # select = minmax(board, DEPTH, -math.inf, math.inf, True)[0]
        select = pickOptimalMove(board, AI_VALUE)
        if isValidMove(board, select):
            row = findOpenRow(board, select)
            addValueToBoard(board, row, select, AI_VALUE)

            if checkForWin(board, AI_VALUE):
                print('\n',"AI wins!", '\n')
                game_over = True
                break

            turn += 1
            turn = turn % 2

    # shows board between turns
    print('\n')
    showBoard(board)

# shows board after game is over
print('The winning board')
showBoard(board)