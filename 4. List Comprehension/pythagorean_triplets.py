def triplets(n: int) -> list[tuple[int, int, int]]:
    return [(a, b, c)
            for a in range(1, n)
            for b in range(a + 1, n)
            for c in range(1, n)
            if c ** 2 == a ** 2 + b ** 2]


if __name__ == '__main__':
    from pprint import pprint

    pprint(triplets(100))
