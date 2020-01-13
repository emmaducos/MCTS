from breakthrough import Board
from breakthrough import Move

BOARD_SIZE = 5
WHITE = 1
BLACK = 2
EMPTY = 0

color = WHITE
pos = 'd4'

B = Board(BOARD_SIZE)
print(B.board) 

M = Move(color, pos, B)

print(M.legalPawnMoves())