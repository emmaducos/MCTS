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

    # def update_board(self, move):
    #     self.board[move[0][0], move[0][1]] = EMPTY
    #     if self.precedent_turn == WHITE:
    #         self.board[move[1][0], move[1][1]] = BLACK
    #         self.precedent_turn = BLACK
    #     elif self.precedent_turn == BLACK:
    #         self.board[move[1][0], move[1][1]] = WHITE
    #         self.precedent_turn = WHITE
    
    def update_board(self, move):
        self.board[move[0][0], move[0][1]] = EMPTY
        if self.turn == WHITE:
            self.board[move[1][0], move[1][1]] = WHITE
            self.turn = BLACK
        elif self.turn == BLACK:
            self.board[move[1][0], move[1][1]] = BLACK
            self.turn = WHITE

class Node:
    """ A node in the game tree. 
        Note wins is always from the viewpoint of precedent_turn.
        Crashes if state not specified.
    """
    def __init__(self, move = None, parent = None, state = None):
        self.move = move # the move that got us to this node - "None" for the root node
        self.parentNode = parent # "None" for the root node
        self.childNodes = []
        self.wins = 0
        self.visits = 0
        self.untriedMoves = state.pawnLegalMoves() # future child nodes
        self.turn = state.turn # the only part of the state that the Node needs later
        
    def UCTSelectChild(self, explo_param):
        """ Use the UCB1 formula to select a child node. A constant explo_param is applied so we vary the amount of
            exploration versus exploitation.
        """
        s = sorted(self.childNodes, key = lambda c: c.wins/c.visits + explo_param * math.sqrt(2*math.log(self.visits)/c.visits))[-1]
        return s
    
    def AddChild(self, m, s):
        """ Remove m from untriedMoves and add a new child node for this move.
            Return the added child node
        """
        n = Node(move = m, parent = self, state = s)
        self.untriedMoves.remove(m)
        self.childNodes.append(n)
        return n
    
    def Update(self, result):
        """ Update this node - one additional visit and result additional wins. 
            result must be from the viewpoint of turn.
        """
        self.visits += 1
        self.wins += result

    def __repr__(self):
        return "[M:" + str(self.move) + " W/V:" + str(self.wins) + "/" + str(self.visits) + " U:" + str(self.untriedMoves) + "]"

    def TreeToString(self, indent):
        s = self.IndentString(indent) + str(self)
        for c in self.childNodes:
             s += c.TreeToString(indent+1)
        return s

    def IndentString(self,indent):
        s = "\n"
        for i in range (1,indent+1):
            s += "| "
        return s

    def ChildrenToString(self):
        s = ""
        for c in self.childNodes:
             s += str(c) + "\n"
        return s

def UCT(rootstate, itermax, explo_param, verbose = False):
    """ Conduct a UCT search for itermax iterations starting from rootstate.
        Return the best move from the rootstate.
        """

    rootnode = Node(state=rootstate)

    for i in range(itermax):
        node = rootnode
        state = rootstate.clone()

        # Select
        while node.untriedMoves == [] and node.childNodes != []: # node is fully expanded and non-terminal
            node = node.UCTSelectChild(explo_param=explo_param)
            state.update_board(node.move)

        # Expand
        if node.untriedMoves != []: # if we can expand (i.e. state/node is non-terminal)
            m = random.choice(node.untriedMoves) 
            state.update_board(m)
            node = node.AddChild(m,state) # add child and descend tree

        # Rollout - this can often be made orders of magnitude quicker using a state.GetRandomMove() function
        while state.pawnLegalMoves() != []: # while state is non-terminal
            state.update_board(random.choice(state.pawnLegalMoves()))

        # Backpropagate
        while node != None: # backpropagate from the expanded node and work back to the root node
            node.Update(state.is_won()) # state is terminal. Update node with result from POV of node.playerJustMoved
            node = node.parentNode

    # Output some information about the tree - can be omitted
    # if verbose: print rootnode.TreeToString(0)
    # else: print rootnode.ChildrenToString()

    return sorted(rootnode.childNodes, key = lambda c: c.visits)[-1].move # return the move that was most visited
  

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
            if policy == 'uct':
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

if __name__ == "__main__":
    BOARD_SIZE = 5
    explo_param = 0.4

    state = BreakThroughState(BOARD_SIZE)

    while (state.pawnLegalMoves() != []):
        print(state.board)
        if state.turn == WHITE:
            m = UCT(rootstate=state, itermax=1000, explo_param=explo_param, verbose=False) # play with values for itermax and verbose = True
        else:
            m = UCT(rootstate=state, itermax=100, explo_param=explo_param, verbose=False)
        print("Best Move: " + str(m) + "\n")
        state.update_board(m)
    if state.is_won(state.turn) == 1.0:
        print("Player " + str(state.turn) + " wins!")
    elif state.is_won(state.turn) == 0.0:
        print("Player " + str(3 - state.turn) + " wins!")
    else: print("Nobody wins!")

    print("done !")

