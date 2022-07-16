"""
Tic Tac Toe Player
"""

import math, copy, random

X = "X"
O = "O"
EMPTY = None


class Error(Exception):
    """Base class for exceptions."""
    pass

class InvalidActionError(Error):
    """Exception raised for invalid actions."""
    def __init__(self, message):
        self.messsage = message

def initial_state():
    """
    Returns starting state of the board.
    """
    return [[EMPTY, EMPTY, EMPTY],
            [EMPTY, EMPTY, EMPTY],
            [EMPTY, EMPTY, EMPTY]]


def player(board):
    """
    Returns player who has the next turn on a board.
    """
    numX = 0
    numO = 0

    for row in range(3):
        for col in range(3):
            if board[row][col] == "X":
                numX += 1
            elif board[row][col] == "O":
                numO += 1
    if numX == numO:
        return X
    elif numX > numO:
        return O


def actions(board):
    """
    Returns set of all possible actions (i, j) available on the board.
    """
    all_actions = set()

    for row in range(3):
        for col in range(3):
            if board[row][col] == EMPTY:
                one_action = (row,col)
                all_actions.add(one_action)
    return all_actions

def result(board, action):
    """
    Returns the board that results from making move (i, j) on the board.
    """
    copy_board = copy.deepcopy(board)
    
    if copy_board[action[0]][action[1]] != EMPTY:
        raise InvalidActionError("Not a valid action for the board.")
    
    copy_board[action[0]][action[1]] = player(board)
    return copy_board

def winner(board):
    """
    Returns the winner of the game, if there is one.
    """
    for row in range(3):
        if board[row][0] == board[row][1] == board[row][2]:
            if board[row][0] == X or board[row][1] == X or board[row][2] == X:
                return X
            elif board[row][0] == O or board[row][1] == O or board[row][2] == O:
                return O
        
    row = 0
    if board[row][0] == board[row+1][0] == board[row+2][0]:
        if board[row][0] == X or board[row+1][0] == X or board[row+2][0] == X:
            return X
        elif board[row][0] == O or board[row+1][0] == O or board[row+2][0] == O:
            return O
    if board[row][1] == board[row+1][1] == board[row+2][1]:
        if board[row][1] == X or board[row+1][1] == X or board[row+2][1] == X:
            return X
        elif board[row][1] == O or board[row+1][1] == O or board[row+2][1] == O:
            return O
    if board[row][2] == board[row+1][2] == board[row+2][2]:
        if board[row][2] == X or board[row+1][2] == X or board[row+2][2] == X:
            return X
        elif board[row][2] == O or board[row+1][2] == O or board[row+2][2] == O:
            return O

    if board[row][0] == board[row+1][1] == board[row+2][2]:
        if board[row][0] == X or board[row+1][1] == X or board[row+2][2] == X:
            return X
        elif board[row][0] == O or board[row+1][1] == O or board[row+2][2] == O:
            return O
    if board[row][2] == board[row+1][1] == board[row+2][0]:
        if board[row][2] == X or board[row+1][1] == X or board[row+2][0] == X:
            return X
        elif board[row][2] == O or board[row+1][1] == O or board[row+2][0] == O: 
            return O

    return None


def terminal(board):
    """
    Returns True if game is over, False otherwise.
    """

    if winner(board) != None:
        return True

    for row in range(3):
        for col in range(3):
            if board[row][col] == EMPTY:
                return False
    return True


def utility(board):
    """
    Returns 1 if X has won the game, -1 if O has won, 0 otherwise.
    """
    if winner(board) == X:
        return 1
    elif winner(board) == O:
        return -1
    else:
        return 0 
    

def minimax(board):
    """
    Returns the optimal action for the current player on the board.
    """
    max_dict = {}
    min_dict = {}

    if player(board) == X:
        for action in actions(board):
            max_dict[action] = minvalue(result(board, action))
        all_values = max_dict.values()
        max_value = max(all_values)
        list_of_keys = list()
        for key, value in max_dict.items():
            if value == max_value:
                list_of_keys.append(key)
        max_key = random.choice(list_of_keys)       
        # print("X is AI", max_dict)
        return max_key
    else:
        for action in actions(board):
            min_dict[action] = maxvalue(result(board, action))
        all_values = min_dict.values()
        min_value = min(all_values)
        list_of_keys = list()
        for key, value in min_dict.items():
            if value == min_value:
                list_of_keys.append(key)
        min_key = random.choice(list_of_keys)
        # print("O is AI", min_dict)
        return min_key
            
            
def maxvalue(board):
    """
    Returns the best possible value for X 
    """
    if terminal(board):
        return utility(board)
    v = -math.inf
    for action in actions(board):
        v = max(v, minvalue(result(board, action)))
    return v

def minvalue(board):
    """
    Returns the best possible value for O 
    """
    if terminal(board):
        return utility(board)
    v = math.inf
    for action in actions(board):
        v = min(v, maxvalue(result(board, action)))
    return v


