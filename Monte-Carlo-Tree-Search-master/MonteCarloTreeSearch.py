import Tree
import UCT
import Node as nd
import shogi
import time


class MonteCarloTreeSearch:
    WIN_SCORE = 10
    opponent = -1
    Int_Min_Value = -100000
    Int_Max_Value = 100000
    # 100000
    look_ahead = 0
    PIECE_TYPES = ['NONE',
                   'PAWN', 'LANCE', 'KNIGHT', 'SILVER',
                   'GOLD',
                   'BISHOP', 'ROOK',
                   'KING',
                   'PROM_PAWN', 'PROM_LANCE', 'PROM_KNIGHT', 'PROM_SILVER',
                   'PROM_BISHOP', 'PROM_ROOK',
                   ]
    debug = False

    def __init__(self):
        self.level = 3

    def getLevel(self):
        return self.level

    def setLevel(self, level):
        self.level = level

    def getMillisForCurrentLevel(self):
        return 2 * (self.level - 1) + 1

    def selectPromisingNode(rootNode):
        node = rootNode
        uct = UCT.UCT()
        while (len(node.getChildArray()) > 0):
            node = uct.findBestNodeWithUCT(node=node, root=rootNode)
            if (node.getParent().ID != rootNode.ID):
                print("a")
        return node

    def expandNode(node):
        possibleStates = node.getState().getAllPossibleStates()
        for st in possibleStates:
            newNode = nd.Node(state=st)
            newNode.setParent(node)
            newNode.getState().setPlayerNo(node.getState().getOpponent())
            # newNode.getState().setPlayerNo(node.getState().getPlayerNo())
            node.getChildArray().append(newNode)

    def backPropagation(nodeToExplore, score, playerWhoWon):
        tempNode = nodeToExplore
        while (tempNode != None):
            tempNode.getState().incrementVisit()
            if (tempNode.getState().getPlayerNo() == playerWhoWon):
                #                tempNode.getState().addScore(MonteCarloTreeSearch.WIN_SCORE)
                tempNode.getState().addScore(score)

            if (hasattr(tempNode, 'parent')):
                tempNode = tempNode.getParent()
            else:
                tempNode = None

    def simulateRandomPlayout(self, node):
        tempNode = nd.Node(node=node)
        tempState = tempNode.getState()
        boardStatus, player = tempState.getBoard().checkStatus()
        count = 0
        Gscore = 0
        currentPlayer = node.state.getPlayerNo()
        opponentPlayer = node.state.getOpponent()
        try:
            #            if(player == MonteCarloTreeSearch.opponent):
            #                tempNode.getParent().getState().setWinScore(MonteCarloTreeSearch.Int_Min_Value)
            #                return boardStatus, player

            # while(boardStatus == shogi.Board.status_IN_PROGRESS or boardStatus == shogi.Board.status_IS_CHECK):
            while (boardStatus != shogi.Board.status_IS_GAMEOVER):
                if (count == MonteCarloTreeSearch.look_ahead):
                    break
                tempState.togglePlayer()
                score, player = tempState.randomPlay()
                if (player == currentPlayer):
                    # Current Player played the simulation
                    score = score
                else:
                    # Opponent Player played the simulation
                    score = -score
                Gscore = Gscore + score
                tempBoard = tempState.getBoard()
                if (len(tempBoard.legal_moves) == 0):
                    break;
                count += 1

            #                if(hasattr(tempNode,'parent')):
            #                    if(tempNode.getParent().getState().getPlayerNo() == player):
            #                        tempNode.getParent().getState().addScore(score)
            #                else:
            #                    print("No Parent")
            if (Gscore >= 0):
                # Current player has a positive game
                return Gscore, currentPlayer
            else:
                return Gscore, opponentPlayer
        except Exception as e:
            print(e)

    def evaluateChildandParent(parentNode=None, childNode=None, playerNo=None):

        childBoard = childNode.getState().getBoard()
        parentBoard = parentNode.getState().getBoard()

        #        if(MonteCarloTreeSearch.debug):
        #            print(childBoard)
        #            print("^^^^^^^^CB above^^^^^^^^^")
        #
        #            print(parentBoard)
        #            print("^^^^^^^^PB above^^^^^^^^^")

        #        if(parentBoard.turn != playerNo):
        #            return 0

        score = 0
        childMove = childBoard.move_stack[-1]
        if childMove.promotion == True:
            score += 2

        # Get piece to be captured in this move
        captured_piece = parentBoard.piece_type_at(childMove.to_square)
        captured_piece = MonteCarloTreeSearch.PIECE_TYPES[captured_piece]

        attackers = childBoard.attackers(childBoard.turn, childMove.to_square)
        if captured_piece != 'NONE':
            print("")
            #            print(attackers)
            print(len(attackers))

        if captured_piece == 'PAWN':
            score += MonteCarloTreeSearch.WIN_SCORE / 1.5

        elif captured_piece == 'LANCE' or captured_piece == 'KNIGHT' or captured_piece == 'SILVER':
            score += MonteCarloTreeSearch.WIN_SCORE / 1.3

        elif captured_piece == 'GOLD' or captured_piece == 'BISHOP' or captured_piece == 'ROOK':
            score += MonteCarloTreeSearch.WIN_SCORE / 1.2

        elif captured_piece == 'PROM_PAWN' or captured_piece == 'PROM_LANCE' or captured_piece == 'PROM_SILVER':
            score += MonteCarloTreeSearch.WIN_SCORE / 1.25

        elif captured_piece == 'PROM_BISHOP' or captured_piece == 'PROM_ROOK' or captured_piece == 'PROM_KNIGHT' or captured_piece == 'PROM_SILVER':
            score += MonteCarloTreeSearch.WIN_SCORE / 1.15

        status, _ = childBoard.checkStatus()
        if status == shogi.Board.status_IS_CHECK:
            score = score + (MonteCarloTreeSearch.WIN_SCORE / 1.1)
        #            print(attackers)

        if status == shogi.Board.status_IS_CHECKMATE:
            score = score + MonteCarloTreeSearch.Int_Max_Value

        if score != 0:
            MonteCarloTreeSearch.backPropagation(childNode, score, playerNo)

        return score

    def findNextMove(self, board, playerNo):
        if (playerNo == 0):
            MonteCarloTreeSearch.opponent = 1
        else:
            MonteCarloTreeSearch.opponent = 0
        if (MonteCarloTreeSearch.opponent == -1):
            print("ERROR")
        tree = Tree.Tree()
        rootNode = tree.getRoot()
        rootState = rootNode.getState()
        rootState.setBoard(board)
        rootState.setPlayerNo(MonteCarloTreeSearch.opponent)
        t0 = time.time()
        moves = list(board.legal_moves)
        print("Number of legal Moves {}".format(len(moves)))
        for i in range(len(moves) + 1):
            # print("performing move {}".format(i))
            # Phase 1 Selection
            if ((i + 2) == len(moves)):
                print("WARNING")
            promisingNode = MonteCarloTreeSearch.selectPromisingNode(rootNode)
            # Phase 2 Expansion
            if (i > 0):
                if (promisingNode.getParent().ID != rootNode.ID):
                    print("asdsa")
            MonteCarloTreeSearch.expandNode(promisingNode)
            if (i == -1):
                for z in range(len(promisingNode.getChildArray())):
                    print("=======board{}========".format(z))
                    print(promisingNode.childArray[z].state.getBoard())
            # Phase 3 Simulation
            nodeToExplore = promisingNode
            length = len(promisingNode.getChildArray())
            Escore = 0
            if (length > 0):
                nodeToExplore = promisingNode.getRandomChildNode()
                if (i < len(moves)):
                    # if(nodeToExplore.getParent().ID == rootNode.ID):
                    Escore = MonteCarloTreeSearch.evaluateChildandParent(promisingNode, nodeToExplore, playerNo)
            mcts = MonteCarloTreeSearch()
            score = 0
            player = -1
            try:
                score, player = mcts.simulateRandomPlayout(node=nodeToExplore)
                currentPlayer = nodeToExplore.state.getPlayerNo()
                opponentPlayer = nodeToExplore.state.getOpponent()

                Gscore = score + Escore
                if (Gscore >= 0):
                    # Current player has a positive game
                    player = currentPlayer
                else:
                    player = opponentPlayer

            except:
                print("Error")
            # Phase 4 BackPropagation
            MonteCarloTreeSearch.backPropagation(nodeToExplore, Gscore, player)

            if (MonteCarloTreeSearch.opponent == -1):
                print("ERROR")

        bestNode = rootNode.getChildWithMaxScore()
        tree.setRoot(bestNode)
        t1 = time.time()
        try:
            return bestNode.getState().getBoard(), t1 - t0, len(moves)
        except Exception as e:
            print(e)
