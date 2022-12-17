from itertools import cycle

import numpy as np

blocks = cycle(
    [
        np.array([[1, 1, 1, 1]], dtype=bool),
        np.array([[0, 1, 0], [1, 1, 1], [0, 1, 0]], dtype=bool),
        np.array([[0, 0, 1], [0, 0, 1], [1, 1, 1]][::-1], dtype=bool),
        np.array([[1], [1], [1], [1]], dtype=bool),
        np.array([[1, 1], [1, 1]], dtype=bool),
    ]
)

with open("input_day_17.txt", "r") as f:
    moves = [-1 if c == "<" else +1 for c in f.read().strip()]

print(len(moves))
moves = cycle(moves)

board = np.zeros((4 * 2022, 7), dtype=bool)

highest_rock = 0
for block_idx in range(2022):
    block = next(blocks)
    stopped = False
    left_edge = 2
    bottom_edge = highest_rock + 3
    while not stopped:
        move = next(moves)
        trial_move = left_edge + move
        if trial_move >= 0 and trial_move + block.shape[1] <= 7:
            board_tile = board[
                         bottom_edge: bottom_edge + block.shape[0],
                         trial_move: trial_move + block.shape[1],
                         ]

            if np.all(~(board_tile & block)):
                left_edge = trial_move

        trial_down = bottom_edge - 1
        if trial_down < 0:
            stopped = True
        else:
            board_tile = board[
                         trial_down: trial_down + block.shape[0],
                         left_edge: left_edge + block.shape[1],
                         ]
            if np.all(~(board_tile & block)):
                bottom_edge = trial_down
            else:
                stopped = True
        if stopped:
            board[
            bottom_edge: bottom_edge + block.shape[0],
            left_edge: left_edge + block.shape[1],
            ] += block
            highest_rock = max(bottom_edge + block.shape[0], highest_rock)

print(highest_rock)
