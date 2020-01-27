import numpy as np
import copy

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
                # print("White has won")
                return WHITE
            if self.board[0][i] == BLACK:
                # print("Black has won")
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

    def random_policy(self, legal_moves):
        rand = np.random.randint(len(legal_moves))
        best_move = legal_moves[rand]
        return best_move

    def random_playout(self, verbose=False):
        if verbose:
            print(self.board)
        while not self.is_won():
            M = Move(self)
            legal_moves = M.pawnLegalMoves()

            best_move = self.random_policy(legal_moves)
            if verbose:
                print("play:", best_move)

            self.update_board(best_move)
            if verbose:
                print(self.board)
        return self.is_won()

    def ucb(self, w, n, t, c):
        return (w / n) + c * np.sqrt(np.log(t) / n)

    def flat_mc(self, nb_playout=10):
        '''
        policy='random' : one random playout
        winning_rate refers to white winning rate
        '''
        # print(self.board)
        move_count = 0
        while not self.is_won():
            move_count += 1
            # print('move count', move_count)
            # print("Move:", move_count)
            M = Move(self)
            legal_moves = M.pawnLegalMoves()

            winning_rate = []
            for legal_move in legal_moves:
                board_initial = copy.deepcopy(self)
                # play the first move
                board_initial.update_board(legal_move)
                # play nb_game random games
                history = []
                for _ in range(nb_playout):
                    board_playout = copy.deepcopy(board_initial)
                    history.append(board_playout.random_playout())
                    # print(history)
                winning_rate.append((history.count(1) / nb_playout) * 100)
            # print(len(white_winning_rate))
            best_rate = max(winning_rate)
            best_move_index = winning_rate.index(best_rate)
            best_move = legal_moves[best_move_index]
            print("best white winning rate", best_rate)
            best_move = self.random_policy(legal_moves)

            # print("play:", move)
            self.update_board(best_move)
            # print(self.board)

        # def game(self, policy, nb_simu=1, explo_param=0.4):
    #     '''
    #     policy='random' : one random playout
    #     winning_rate refers to white winning rate
    #     '''
    #     # print(self.board)
    #     move_count = 0
    #     win_count = 0
    #     simu_count = 0
    #
    #     while not self.is_won():
    #         move_count += 1
    #         print('move count', move_count)
    #         # print("Move:", move_count)
    #         M = Move(self)
    #         legal_moves = M.pawnLegalMoves()
    #
    #         if policy == "random":
    #             best_move = self.random_policy(legal_moves)
    #
    #         winning_rate = []
    #         ucbounds = []
    #         ucbound = []
    #         tot_simu_count = 0
    #         for legal_move in legal_moves:
    #             board_initial = copy.deepcopy(self)
    #             # play the first move
    #             board_initial.update_board(legal_move)
    #             # play nb_game random games
    #
    #             history = []
    #             simu_count = 0
    #             for _ in range(nb_simu):
    #                 simu_count += 1
    #                 stat = {'move_count': move_count, 'win_count': win_count, 'simu_count': simu_count}
    #                 tot_simu_count += 1
    #                 # print("simu_count", simu_count)
    #                 board_playout = copy.deepcopy(board_initial)
    #                 history.append(board_playout.random_playout())
    #                 ucbound = self.ucbound(win_count, simu_count, tot_simu_count, explo_param)
    #                 ucbounds.append(ucbound)
    #             winning_rate.append((history.count(1) / nb_simu) * 100)
    #             ucbound = max(ucbounds)
    #         # print(len(white_winning_rate))
    #
    #         if policy == 'flat':
    #             best_move_index = winning_rate.index(max(winning_rate))
    #             best_move = legal_moves[best_move_index]
    #
    #         if policy == 'ucb':
    #             best_move_index = ucbound.index(max(ucbound))
    #             best_move = legal_moves[best_move_index]
    #             print(ucbound)
    #
    #         move = best_move
    #         # print("play:", move)
    #         self.update_board(move)
    #         # print(self.board)
    #
    #         if self.is_won() == WHITE:
    #             win_count += 1
    #             print("win_count", win_count)
    #
    #     stat = {'move_count': move_count, 'win_count': win_count, 'simu_count': simu_count}
    #     print(stat)

    # def flat_mc(self, nb_game, legal_moves):
    #     white_winning_rate = []
    #     for legal_move in legal_moves:
    #         board_initial = copy.deepcopy(self)
    #         # play the first move
    #         board_initial.update_board(legal_move)
    #         # play nb_game random games
    #         history = []
    #         for _ in range(nb_game):
    #             board_playout = copy.deepcopy(board_initial)
    #             history.append(board_playout.random_playout())
    #             # print(history)
    #         white_winning_rate.append((history.count(1) / nb_game) * 100)
    #     # print(len(white_winning_rate))
    #     best_rate = max(white_winning_rate)
    #     best_move_index = white_winning_rate.index(best_rate)
    #     best_move = legal_moves[best_move_index]
    #     print("best white winning rate", best_rate)
    #     return best_move


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
                # print("current move:", [i, j])
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
                # print("possibleMoves", possibleMoves)
                for possibleMove in possibleMoves:
                    if self.isValid(possibleMove):
                        legalMoves.append(possibleMove)
        # print("legal moves:", legalMoves)
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
    BOARD_SIZE = 5
    nb_playout = 10
    explo_param = 0.4
    verbose = False

    board = Board(BOARD_SIZE)

    # print(board.random_playout(verbose=verbose))
    board.flat_mc(nb_playout)

    print("done !")

