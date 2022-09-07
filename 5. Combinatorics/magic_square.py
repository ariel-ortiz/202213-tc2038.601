from typing import Optional
from timeit import timeit
from combinatorics import permute


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


def solve_problem_brute_force_1() -> Optional[list[list[int]]]:
    for a in range(1, 10):
        for b in range(1, 10):
            for c in range(1, 10):
                for d in range(1, 10):
                    for e in range(1, 10):
                        for f in range(1, 10):
                            for g in range(1, 10):
                                for h in range(1, 10):
                                    for i in range(1, 10):
                                        if (len({a, b, c, d, e, f, g, h, i})
                                                == 9):
                                            square = [[a, b, c],
                                                      [d, e, f],
                                                      [g, h, i]]
                                            if check_square(square):
                                                return square
    return None


def solve_problem_brute_force_2() -> Optional[list[list[int]]]:
    for p in permute(list(range(1, 10))):
        square = [p[:3],
                  p[3:6],
                  p[6:]]
        if check_square(square):
            return square
    return None


if __name__ == '__main__':
    # print(check_square([[1, 2, 3],
    #                     [4, 5, 6],
    #                     [7, 8, 9]]))
    # print(check_square([[8, 1, 6],
    #                     [3, 5, 7],
    #                     [4, 9, 2]]))

    def just_do_it() -> None:
        print(solve_problem_brute_force_2())

    t = timeit(just_do_it, number=1)
    print(f'Time = {t:.3f} s')
