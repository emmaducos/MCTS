import shogi
import random as rnd
import MonteCarloTreeSearch


class State:
    PIECE_TYPES = ['NONE',
                   'PAWN', 'LANCE', 'KNIGHT', 'SILVER',
                   'GOLD',
                   'BISHOP', 'ROOK',
                   'KING',
                   'PROM_PAWN', 'PROM_LANCE', 'PROM_KNIGHT', 'PROM_SILVER',
                   'PROM_BISHOP', 'PROM_ROOK',
                   ]

    def __init__(self, board=None, state=None):

        if board is None and state is not None:
            # State is given
            self.board = shogi.Board()  #(move_stack=list(state.getBoard().move_stack))
            self.playerNo = state.getPlayerNo()
            self.visitCount = state.getVisitCount()
            self.winScore = state.getWinScore()
        elif board is not None and state is None:
            # Board is given
            self.board = shogi.Board()  #(move_stack=list(board.move_stack))
            self.visitCount = 0
            self.winScore = 0
        else:
            # No data is given
            self.board = shogi.Board()
            self.visitCount = 0
            self.winScore = 0

    def getBoard(self):
        return self.board

    def setBoard(self, board):
        self.board = board

    def getPlayerNo(self):
        return self.playerNo

    def setPlayerNo(self, playerNo):
        # print("set playerNo {}".format(playerNo))
        self.playerNo = playerNo

    def getOpponent(self):
        opponent = 1 if self.playerNo == 0 else 0
        return opponent

    def getVisitCount(self):
        return self.visitCount

    def setVisitCount(self, visitCount):
        self.visitCount = visitCount

    def getWinScore(self):
        return self.winScore

    def setWinScore(self, win_Score):
        self.winScore = win_Score

    def getAllPossibleStates(self):
        possibleStates = []
        available_moves = list(self.board.legal_moves)
        if (self.board.turn == 0):
            playerNo = 1
        else:
            playerNo = 0
        for p in range(available_moves.__len__()):
            newState = State(board=self.board)
            newState.setPlayerNo(playerNo)
            newState.getBoard().push(available_moves[p])
            possibleStates.append(newState)

        return possibleStates

    def randomPlay(self):
        score = 0
        available_moves = list(self.board.legal_moves)
        total_moves = len(available_moves)
        player = self.board.turn
        if (total_moves - 1 <= 0):
            return score, player
        rand = rnd.randint(0, total_moves - 1)

        # Get piece to be captured in this move
        captured_piece = self.board.piece_type_at(available_moves[rand].to_square)
        captured_piece = State.PIECE_TYPES[captured_piece]

        if (captured_piece == 'PAWN'):
            score = MonteCarloTreeSearch.MonteCarloTreeSearch.WIN_SCORE / 1.6

        elif (captured_piece == 'LANCE' or captured_piece == 'KNIGHT' or captured_piece == 'SILVER'):
            score = MonteCarloTreeSearch.MonteCarloTreeSearch.WIN_SCORE / 1.4

        elif (captured_piece == 'GOLD' or captured_piece == 'BISHOP' or captured_piece == 'ROOK'):
            score = MonteCarloTreeSearch.MonteCarloTreeSearch.WIN_SCORE / 1.45

        elif (
                captured_piece == 'PROM_PAWN' or captured_piece == 'PROM_LANCE' or captured_piece == 'PROM_KNIGHT' or captured_piece == 'PROM_SILVER'):
            score = MonteCarloTreeSearch.MonteCarloTreeSearch.WIN_SCORE / 1.3

        elif (
                captured_piece == 'PROM_BISHOP' or captured_piece == 'PROM_ROOK' or captured_piece == 'PROM_KNIGHT' or captured_piece == 'PROM_SILVER'):
            score = MonteCarloTreeSearch.MonteCarloTreeSearch.WIN_SCORE / 1.25

        self.board.push(available_moves[rand])

        status, _ = self.board.checkStatus()
        if (status == shogi.Board.status_IS_CHECK):
            score = score + (MonteCarloTreeSearch.MonteCarloTreeSearch.WIN_SCORE / 1.1)

        if (status == shogi.Board.status_IS_CHECKMATE):
            score = score + MonteCarloTreeSearch.MonteCarloTreeSearch.Int_Max_Value
            print(self.board)

        return score, player

    def incrementVisit(self):
        self.visitCount += 1

    def addScore(self, score):
        if (self.winScore != MonteCarloTreeSearch.MonteCarloTreeSearch.Int_Min_Value):
            self.winScore += score

    def togglePlayer(self):
        self.playerNo = 1 if self.playerNo == 0 else 0
