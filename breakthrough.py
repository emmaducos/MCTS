import numpy as np

WHITE = 1
BLACK = 2
EMPTY = 0

chess_map_from_alpha_to_index = {
   "a" : 0,
   "b" : 1,
   "c" : 2,
   "d" : 3,
   "e" : 4,
   "f" : 5,
   "g" : 6,
   "h" : 7
}

chess_map_from_index_to_alpha = {
   0: "a",
   1: "b",
   2: "c",
   3: "d",
   4: "e",
   5: "f",
   6: "g",
   7: "h"
}

class Board():
    def __init__(self, board_size):
        self.board_size = board_size
        self.board = np.zeros((board_size, board_size), dtype=np.int8)
        self.turn = WHITE

        for i in range(0, 2):
            for j in range(0, board_size):
                self.board[i][j] = WHITE
        for i in range(board_size - 2, board_size):
            for j in range(0, board_size):
                self.board[i][j] = BLACK
        
    def __getitem__(self, key):
        return self.board[key]


class Move():
    def __init__(self, color, pos, board):
        self.color = color
        self.pos = pos
        self.board = board

    def hexa2ind(self):
        column, row = list(self.pos.strip().lower())
        row = int(row) - 1
        column = chess_map_from_alpha_to_index[column]
        i,j = row, column
        return (i, j)

    def ind2hexa(self, row, column):
        row += 1
        column = chess_map_from_index_to_alpha[column]
        return(str(column) + str(row))

    def legalPawnMoves(self):
        """ A function(positionString, board) that returns the all possible moves
            of a knight stood on a given position
            from https://impythonist.wordpress.com/2017/01/01/modeling-a-chessboard-and-mechanics-of-its-pieces-in-python/
        """
        (i,j) = self.hexa2ind()
        possibleMoves = []

        try:
            temp = self.board[i + 1][j - 1]
            possibleMoves.append([i + 1, j - 1])
        except:
            pass
        try:
            temp = self.board[i + 1][j]
            possibleMoves.append([i + 1, j])
        except:
            pass
        try:
            temp = self.board[i + 1][j + 1]
            possibleMoves.append([i + 1, j + 1])
        except:
            pass

        # Filter values
        print(possibleMoves)
        legalMoves = [possibleMove for possibleMove in possibleMoves if self.isValid(possibleMove)].sort()
        return legalMoves

    def isValid(self, possibleMove):
        pass