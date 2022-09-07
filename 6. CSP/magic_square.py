from typing import NamedTuple, Optional
from csp import CSP, Constraint


class GridLocation(NamedTuple):
    row: int
    column: int


def check_square(square: list[list[int]]) -> bool:
    ((a, b, c),
     (d, e, f),
     (g, h, i)) = square
    return ((a + b + c)     # Rows
            == (d + e + f)
            == (g + h + i)
            == (a + d + g)  # Columns
            == (b + e + h)
            == (c + f + i)
            == (a + e + i)  # Diagonals
            == (g + e + c))


class MagicPuzzleConstraint(Constraint[int, GridLocation]):

    def __init__(self, variables: list[int]) -> None:
        super().__init__(variables)
        self.variables: list[int] = variables

    def satisfied(self, assignment: dict[int, GridLocation]) -> bool:
        ...
