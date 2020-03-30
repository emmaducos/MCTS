import MonteCarloTreeSearch
import Shogi
import random as rnd


def randomPlay(board, player):
    available_moves = list(board.legal_moves)
    total_moves = len(available_moves)
    if total_moves == 0:
        print("No Moves")
    elif total_moves == 1:
        board.push(available_moves[0])
    else:
        rand = rnd.randint(0, total_moves - 1)
        board.push(available_moves[rand])
    return board

def main():
    board = Shogi.Board()
    mcts = MonteCarloTreeSearch.MonteCarloTreeSearch()
    gameStatus = board.status_IN_PROGRESS
    move = 0
    #    timeTaken = []
    #    movesTaken = []
    #    arr = []
    while gameStatus != board.status_IS_GAMEOVER:
        if move % 100 == 0:
            print("asdasd")
        if gameStatus == board.status_IS_CHECK:
            print("Check")
        if board.turn == 0:
            board, time, moves = mcts.findNextMove(board, board.turn)
            #            timeTaken.append(time)
            #            movesTaken.append(moves)
            #            arr.append([time,moves])
            #            print("Move {}::".format(board.move_stack[len(board.move_stack) - 1]))
            print(board)
            print("Played By Black - Down")
        else:
            board = randomPlay(board, board.turn)
            # board,time,moves = mcts.findNextMove(board,board.turn)
            #            timeTaken.append(time)
            #            movesTaken.append(moves)
            #            arr.append([time,moves])
            # board=DQNtestMCTS.agent.act(board)
            print("Move {}::".format(board.move_stack[len(board.move_stack) - 1]))
            print(board)
            print("Played By White - Up")
        move += 1
        print("================= Move {}: ====================".format(move))

        gameStatus, _ = board.checkStatus()

    print(board.checkStatus())
    return gameStatus

if __name__ == "__main__":
    results = []
    for i in range(1):
        print(i)
        result = main()
        results.append(result)

    print("Draws    = ", results.count(0))
    print("Player 1 = ", results.count(1))
    print("Player 2 = ", results.count(2))
