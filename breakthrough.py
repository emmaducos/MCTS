import numpy as np

WHITE = 1
BLACK = 2
EMPTY = 0

class Board:
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

    def __setitem__(self, key, item):
        self.board[key] = item

    def is_won(self):
        for i in range(self.board_size):
            if self.board[self.board_size - 1][i] == WHITE:
                print("White has won")
                return WHITE
            if self.board[0][i] == BLACK:
                print("Black has won")
                return BLACK
        return EMPTY

    def update_board(self, move):
        self.board[move[0][0], move[0][1]] = EMPTY
        if self.turn == WHITE:
            self.board[move[1][0], move[1][1]] = WHITE
            self.turn = BLACK
        elif self.turn == BLACK:
            self.board[move[1][0], move[1][1]] = BLACK
            self.turn = WHITE

    def playout(self):
        print(self.board)
        move_count = 0
        while not self.is_won():
            move_count += 1
            print("Move:", move_count)
            M = Move(self)
            legal_moves = M.pawnLegalMoves()
            move = self.random_policy(legal_moves)
            print("play:", move)
            self.update_board(move)
            print(self.board)
        return float(self.is_won())

    def random_policy(self, legal_moves):
        rand = np.random.randint(len(legal_moves))
        return legal_moves[rand]


class Move:
    def __init__(self, board):
        self.board = board
        self.color = board.turn
        self.board_size = board.board_size

    def pawnLegalMoves(self):
        """ A function that returns the all possible moves
            from https://impythonist.wordpress.com/2017/01/01/modeling-a-chessboard-and-mechanics-of-its-pieces-in-python/
        """
        legalMoves = []
        for i in range(self.board_size):
            for j in range(self.board_size):
                #print("current move:", [i, j])
                possibleMoves = []

                if self.color == WHITE:
                    try:
                        temp = self.board[i + 1][j - 1]
                        possibleMoves.append([[i, j], [i + 1, j - 1]])
                    except:
                        pass
                    try:
                        temp = self.board[i + 1][j]
                        possibleMoves.append([[i, j], [i + 1, j]])
                    except:
                        pass
                    try:
                        temp = self.board[i + 1][j + 1]
                        possibleMoves.append([[i, j], [i + 1, j + 1]])
                    except:
                        pass

                if self.color == BLACK:
                    try:
                        temp = self.board[i - 1][j - 1]
                        possibleMoves.append([[i, j], [i - 1, j - 1]])
                    except:
                        pass
                    try:
                        temp = self.board[i - 1][j]
                        possibleMoves.append([[i, j], [i - 1, j]])
                    except:
                        pass
                    try:
                        temp = self.board[i - 1][j + 1]
                        possibleMoves.append([[i, j], [i - 1, j + 1]])
                    except:
                        pass

                # Filter values
                #print("possibleMoves", possibleMoves)
                for possibleMove in possibleMoves:
                    if self.isValid(possibleMove):
                        legalMoves.append(possibleMove)
        #print("legal moves:", legalMoves)
        return legalMoves

    def isValid(self, possibleMove):
        # outranged
        if possibleMove[1][0] >= self.board_size \
                or possibleMove[1][1] >= self.board_size \
                or possibleMove[1][0] < 0 \
                or possibleMove[1][1] < 0:
            return False

        # current player is white
        if self.color == WHITE:
            if self.board[possibleMove[0][0], possibleMove[0][1]] == WHITE:
                # move one square down
                if possibleMove[1][0] != possibleMove[0][0] + 1:
                    return False
                # if there is a black pawn
                if self.board[possibleMove[1][0]][possibleMove[1][1]] == BLACK:
                    # only if on the upper diagonals
                    if possibleMove[1][1] == possibleMove[0][1] + 1 \
                            or possibleMove[1][1] == possibleMove[0][1] - 1:
                        return True
                    return False
                # if there is no black or white pawn
                elif self.board[possibleMove[1][0]][possibleMove[1][1]] == EMPTY:
                    if possibleMove[1][1] == possibleMove[0][1] + 1 \
                            or possibleMove[1][1] == possibleMove[0][1] - 1 \
                            or possibleMove[1][1] == possibleMove[0][1]:
                        return True
                    return False
            return False

        elif self.color == BLACK:
            if self.board[possibleMove[0][0], possibleMove[0][1]] == BLACK:
                if possibleMove[1][0] != possibleMove[0][0] - 1:
                    return False
                if self.board[possibleMove[1][0]][possibleMove[1][1]] == WHITE:
                    if possibleMove[1][1] == possibleMove[0][1] + 1 \
                            or possibleMove[1][1] == possibleMove[0][1] - 1:
                        return True
                    return False
                elif self.board[possibleMove[1][0]][possibleMove[1][1]] == EMPTY:
                    if possibleMove[1][1] == possibleMove[0][1] + 1 \
                            or possibleMove[1][1] == possibleMove[0][1] - 1 \
                            or possibleMove[1][1] == possibleMove[0][1]:
                        return True
                    return False
            return False
        return False


if __name__ == "__main__":
    pass
