import numpy as np
import copy
import itertools

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

    def pawnLegalMoves(self):
        legalMoves = []
        for i in range(self.board_size):
            for j in range(self.board_size):
                # print("current move:", [i, j])
                possibleMoves = []

                if self.turn == WHITE:
                    try:
                        self.board[i + 1][j - 1]
                        possibleMoves.append([[i, j], [i + 1, j - 1]])
                    except:
                        pass
                    try:
                        self.board[i + 1][j]
                        possibleMoves.append([[i, j], [i + 1, j]])
                    except:
                        pass
                    try:
                        self.board[i + 1][j + 1]
                        possibleMoves.append([[i, j], [i + 1, j + 1]])
                    except:
                        pass

                if self.turn == BLACK:
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
        if self.turn == WHITE:
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

        elif self.turn == BLACK:
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

    def is_won(self):
        for i in range(self.board_size):
            if self.board[self.board_size - 1][i] == WHITE:
                return WHITE
            if self.board[0][i] == BLACK:
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

class Game():
    def __init__(self, board, verbose=False):
        self.board = board
        self.random_policy = Random_policy(self.board)
        self.flat_mc_policy = Flat_mc_policy(board=self.board, game=self)
        self.verbose = verbose

    def play(self, board, policy_white='random', policy_black='random', verbose=False):
        if verbose:
            print(board.board)
        policies = itertools.cycle([policy_white, policy_black])
        while not board.is_won():
            policy = next(policies)
            if policy == 'random':
                best_move = self.random_policy.best_move()
            if policy == 'flat_mc':
                best_move = self.flat_mc_policy.best_move()

            if verbose:
                print("play:", best_move)
            board.update_board(best_move)
            if verbose:
                print(board.board)
        return board.is_won()

class Random_policy():
    """
    prend en entrée l'état du jeu (board), et retourne le meilleur coup possible suivant la politique de la classe
    """
    def __init__(self, board, nb_playout=1):
        self.board = board
        
    def best_move(self):
        legal_moves = board.pawnLegalMoves()
        best_move_index = np.random.randint(len(legal_moves))
        best_move = legal_moves[best_move_index]
        return best_move

class UCB_policy(Random_policy):
    def __init__(self, board, nb_playout=10):
        self.board = board
        self.nb_playout = nb_playout

    def ucb(self, w, n, t, c):
        return (w / n) + c * np.sqrt(np.log(t) / n)

    # def best_move(self):
    #     legal_moves = self.board.pawnLegalMoves()
        
    #     for _ in range(nb_playout):
    #         for legal_move in legal_moves:
    #             pass
    #     return best_move

class Flat_mc_policy(Random_policy):
    def __init__(self, board, game, nb_playout=10, verbose=False):
        self.game = game
        self.board = board
        self.win_rate = []
        self.win_history = []
        self.nb_playout = nb_playout
        self.verbose = verbose
    
    def choose_move(self, legal_moves):
        chosen_moves = itertools.cycle(legal_moves)
        chosen_move = next(chosen_moves)
        print(chosen_move)
        return chosen_move

    def best_move(self):
        board_initial = copy.deepcopy(self.board)
        legal_moves = self.board.pawnLegalMoves()

        for _ in range(nb_playout):
            board_initial = copy.deepcopy(self.board)
            chosen_move = self.choose_move(legal_moves)

            # play the first move
            board_initial.update_board(chosen_move)

            rslt = self.game.play(board=board_initial, policy_white='random', policy_black='random', verbose=self.verbose)
            self.win_history.append(rslt)

            if verbose:
                print(self.win_history)

            self.win_rate.append((self.win_history.count(1) / self.nb_playout) * 100)

        best_rate = max(self.win_rate)
        best_move_index = self.win_rate.index(best_rate)
        best_move = legal_moves[best_move_index]
        if verbose:
            print("best white winning rate", best_rate)

        return best_move

    # def best_move(self):
    #     legal_moves = self.board.pawnLegalMoves()

    #     for legal_move in legal_moves:
    #         board_initial = copy.deepcopy(self.board)
    #         if verbose:
    #             print(board.board)
    #         # play the first move
    #         board_initial.update_board(legal_move)
    #         # play nb_game random games
    #         for _ in range(self.nb_playout):
    #             board_playout = copy.deepcopy(board_initial)
    #             rslt = self.game.play(policy_black='random', policy_white='random', board=board_playout, verbose=self.verbose)
    #             self.history.append(rslt)
    #             if verbose:
    #                 print(self.history)
    #         self.winning_rate.append((self.history.count(1) / self.nb_playout) * 100)
        
    #     best_rate = max(self.winning_rate)
    #     best_move_index = self.winning_rate.index(best_rate)
    #     best_move = legal_moves[best_move_index]
    #     if verbose:
    #         print("best white winning rate", best_rate)
    #     return best_move

if __name__ == "__main__":
    BOARD_SIZE = 5
    nb_playout = 10
    nb_game = 10
    explo_param = 0.4
    verbose = False
    policy_white = 'flat_mc'
    policy_black = 'random'

    win_history = []
    for _ in range(nb_game):
        board = Board(BOARD_SIZE)
        game = Game(board, verbose=verbose)
        game_rslt = game.play(board=board, policy_white=policy_white, policy_black=policy_black, verbose=verbose)
        win_history.append(game_rslt)
    white_win_rate = (win_history.count(1) / nb_game) * 100
    black_win_rate = (win_history.count(2) / nb_game) * 100

    print("white_win_rate", white_win_rate)
    print("black_win_rate", black_win_rate)

    print("done !")

