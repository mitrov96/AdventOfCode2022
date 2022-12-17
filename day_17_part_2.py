from collections import deque
from itertools import cycle

import numpy as np

blocks_list = [
    np.array([[1, 1, 1, 1]], dtype=bool),
    np.array([[0, 1, 0], [1, 1, 1], [0, 1, 0]], dtype=bool),
    np.array([[0, 0, 1], [0, 0, 1], [1, 1, 1]][::-1], dtype=bool),
    np.array([[1], [1], [1], [1]], dtype=bool),
    np.array([[1, 1], [1, 1]], dtype=bool),
]

with open("input_day_17.txt", "r") as f:
    moves_list = [-1 if c == "<" else +1 for c in f.read().strip()]

max_range = 8000
board = np.zeros((4 * max_range, 7), dtype=bool)
moves = cycle(moves_list)
blocks = cycle(blocks_list)
highest_rock = 0
move_idx = 0
repeat_dict = {}
last_five_list = deque(maxlen=5)
height_list = []
for block_idx in range(max_range):
    block = next(blocks)
    stopped = False
    left_edge = 2
    bottom_edge = highest_rock + 3
    while not stopped:
        move = next(moves)
        move_idx += 1
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

    last_five_list.append(move_idx % len(moves_list))
    if block_idx % 5 == 0:
        last_five_tuple = tuple(last_five_list)
        if last_five_tuple in repeat_dict:
            repeat_dict[last_five_tuple].append(block_idx)
        else:
            repeat_dict[last_five_tuple] = [block_idx]

    height_list.append(highest_rock)
repeater_period = 0
for k in repeat_dict:
    if len(repeat_dict[k]) > 1:
        repeater_period = repeat_dict[k][-1] - repeat_dict[k][-2]

rocks = 1000000000000
# rocks = 2022
initial = rocks % repeater_period
nr_periods = (rocks - initial) // repeater_period

for k in range(3):
    value = height_list[k * repeater_period + initial]
    print(value)
    if k > 0:
        diff = value - height_list[(k - 1) * repeater_period + initial]
        print(f"diff:{diff}")

print(diff * nr_periods + height_list[initial] - 1)
