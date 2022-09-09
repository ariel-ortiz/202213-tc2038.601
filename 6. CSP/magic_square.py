from typing import NamedTuple, Optional
from csp import CSP, Constraint


Grid = list[list[int]]


class GridLocation(NamedTuple):
    row: int
    column: int


def check_square(square: Grid) -> bool:
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
        if len(set(assignment.values())) != len(assignment):
            return False
        if len(assignment) < 9:
            return True
        grid: Grid = [[0, 0, 0],
                      [0, 0, 0],
                      [0, 0, 0]]
        for key, value in assignment.items():
            row, column = value
            grid[row][column] = key
        return check_square(grid)


if __name__ == '__main__':
    from pprint import pprint
    variables: list[int] = list(range(1, 10))
    all_grid_locations: list[GridLocation] = [GridLocation(r, c)
                                              for r in range(3)
                                              for c in range(3)]
    domains: dict[int, list[GridLocation]] = {
        var: all_grid_locations for var in variables}
    csp: CSP[int, GridLocation] = CSP(variables, domains)
    csp.add_constraint(MagicPuzzleConstraint(variables))
    solution: Optional[dict[int, GridLocation]] = csp.backtracking_search()

    if solution is None:
        print('No solution found')
    else:
        pprint(solution)
