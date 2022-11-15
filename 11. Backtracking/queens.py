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


def queens(n: int) -> Optional[Board]:
    board = [[0 for _ in range(n)] for _ in range(n)]
    return solve(board, 0)


def print_solution(board: Board) -> None:
    for row in board:
        for x in row:
            if x:
                print('Q', end=' ')
            else:
                print('.', end=' ')
        print()


if __name__ == '__main__':
    board = queens(20)
    if board:
        print_solution(board)
    else:
        print('No solution found')
