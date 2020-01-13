from breakthrough import Board
from breakthrough import Move

BOARD_SIZE = 5
WHITE = 1
BLACK = 2
EMPTY = 0

color = WHITE
pos = 'e4'

B = Board(BOARD_SIZE)
print(B.board) 

M = Move(color, pos, B, BOARD_SIZE)

print(M.legalPawnMoves())

move_count = 0
while not B.isFinished():
    move_count += 1
    print("Move:", move_count)
    print(B.board)
    #move = random choice ([move for move in M.legalPawnMoves()])
    print("play:", move)
    #update board
    print(B.board)
