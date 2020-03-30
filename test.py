import numpy as np
import copy
import itertools
import random
import math

EMPTY = 0
WHITE = 1
BLACK = 2


class BreakThroughState:
    def __init__(self, board_size):
        self.turn = WHITE
        self.board_size = board_size
        assert self.board_size == int(self.board_size) and self.board_size % 2 == 1 # size must be integral and uneven
        
        # initialisation Board
        self.board = np.zeros((board_size, board_size), dtype=np.int8)
        for i in range(0, 2):
            for j in range(0, board_size):
                self.board[i][j] = WHITE
        for i in range(board_size - 2, board_size):
            for j in range(0, board_size):
                self.board[i][j] = BLACK

    def clone(self):
        """Create a deep clone of the game state
        """
        return copy.deepcopy(self)

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
                        self.board[i - 1][j - 1]
                        possibleMoves.append([[i, j], [i - 1, j - 1]])
                    except:
                        pass
                    try:
                        self.board[i - 1][j]
                        possibleMoves.append([[i, j], [i - 1, j]])
                    except:
                        pass
                    try:
                        self.board[i - 1][j + 1]
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

class Node:
    def __init__(self, move = None, parent = None, state = None):
        self.move = move # the move that got us to this node - "None" for the root node
        self.parentNode = parent # "None" for the root node
        self.childNodes = []
        self.wins = 0
        self.visits = 0
        self.untriedMoves = state.pawnLegalMoves() # future child nodes
        self.turn = state.turn # the only part of the state that the Node needs later
        
    def UCTSelectChild(self, explo_param):
        s = sorted(self.childNodes, key = lambda c: c.wins/c.visits + explo_param * math.sqrt(2*math.log(self.visits)/c.visits))[-1]
        return s
    
    def addChild(self, m, s):
        n = Node(move = m, parent = self, state = s)
        self.untriedMoves.remove(m)
        self.childNodes.append(n)
        return n
    
    def update(self, result):
        # print('rslt', result)
        self.visits += 1
        # print('visits', self.visits)
        self.wins += result
        # print('win', self.wins)

    def __repr__(self):
        return "[move:" + str(self.move) + "; wins/visits:" + str(self.wins) + "/" + str(self.visits) + "; nb_untriedmoves:" + str(len(self.untriedMoves)) + "]"

class Policy:
    def __init__(self, state):
        self.state = state

    def random(self):
        legal_moves = self.state.pawnLegalMoves()
        best_move_index = np.random.randint(len(legal_moves))
        best_move = legal_moves[best_move_index]
        return best_move

    def UCT(self, itermax, explo_param):
        """ Conduct a UCT search for itermax iterations starting from rootstate.
            Return the best move from the rootstate.
            """
        rootstate = self.state
        rootnode = Node(state=rootstate)

        for i in range(itermax):
            print("iteration UCT", i)
            node = rootnode
            state = rootstate.clone()
            print(node)
            # Select
            while node.untriedMoves == [] and node.childNodes != []: # node is fully expanded and non-terminal
                node = node.UCTSelectChild(explo_param=explo_param)
                state.update_board(node.move)
            print(node)
            # Expand
            if node.untriedMoves != []: # if we can expand (i.e. state/node is non-terminal)
                m = random.choice(node.untriedMoves) 
                state.update_board(m)
                node = node.addChild(m, state) # add child and descend tree
            print(node)
            # Rollout - this can often be made orders of magnitude quicker using a state.GetRandomMove() function
            while state.pawnLegalMoves() != []: # while state is non-terminal
                state.update_board(random.choice(state.pawnLegalMoves()))
            print(node)
            # Backpropagate
            while node != None: # backpropagate from the expanded node and work back to the root node
                node.update(state.is_won()) # state is terminal. Update node with result from POV of node.playerJustMoved
                node = node.parentNode
            print(node)
        return sorted(rootnode.childNodes, key = lambda c: c.visits)[-1].move # return the move that was most visited

def game(board_size, explo_param, verbose=True):
    state = BreakThroughState(board_size)
    policy = Policy(state)
    print("turn", state.turn)
    while (state.pawnLegalMoves() != []):
        if verbose:
            print(state.board)
        if state.turn == WHITE:
            m = policy.UCT(itermax=100, explo_param=explo_param) # play with values for itermax and verbose = True
        elif state.turn == BLACK:
            m = policy.random()
        if verbose:
            print("Best Move: " + str(m) + "\n")
        state.update_board(m)
    if state.is_won() == WHITE:
        print("Player WHITE wins!")
    elif state.is_won() == BLACK:
        print("Player BLACK wins!")
    else: print("Nobody wins!")
    return state.is_won()

if __name__ == "__main__":
    BOARD_SIZE = 5
    explo_param = 0.4
    verbose = True
    nb_game = 10

    win_history = []
    for _ in range(nb_game):
        game_rslt = game(board_size=BOARD_SIZE, explo_param=explo_param, verbose=verbose)
        win_history.append(game_rslt)
    
    white_win_rate = (win_history.count(1) / nb_game) * 100
    black_win_rate = (win_history.count(2) / nb_game) * 100

    print("white_win_rate", white_win_rate)
    print("black_win_rate", black_win_rate)
    print("done !")

