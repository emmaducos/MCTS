import numpy as np

from breakthrough import Board
from breakthrough import Move

BOARD_SIZE = 5

history = []
for _ in range(10):
    B = Board(BOARD_SIZE)
    history.append(B.playout())
    print(history)
