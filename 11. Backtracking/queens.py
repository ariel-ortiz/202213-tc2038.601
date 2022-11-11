from copy import deepcopy
from pprint import pprint
from typing import Optional


Board = list[list[int]]


def is_safe(board: Board, row: int, col: int) -> bool:
    # Other queen on left side of the same row?
    for i in range(col):
        if board[row][i]:
            return False
    # Other queen in upper left diagonal?
    for i, j in zip(range(row - 1, -1, -1),
                    range(col - 1, -1, -1)):
        if board[i][j]:
            return False
    # Other queen in lower left diagonal?
    for i, j in zip(range(row + 1, len(board)),
                    range(col - 1, -1, -1)):
        if board[i][j]:
            return False
    return True


def solve(board: Board, col: int) -> Optional[Board]:
    if col == len(board):
        return board
    for row in range(len(board)):
        if is_safe(board, row, col):
            new_board = deepcopy(board)
            new_board[row][col] = 1
            result = solve(new_board, col + 1)
            if result:
                return result
    return None


if __name__ == '__main__':
    pprint(solve([[0, 0, 0, 0],
                  [0, 0, 0, 0],
                  [0, 0, 0, 0],
                  [0, 0, 0, 0]], 0))
