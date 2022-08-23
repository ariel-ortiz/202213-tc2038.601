from typing import Generator


def powers_of_two(n: int) -> Generator[int, None, None]:
    return (2 ** x for x in range(n))


def powers_of_two_with_yield(n: int) -> Generator[int, None, None]:
    x = 1
    for _ in range(n):
        yield x
        x += 2


def my_generator() -> Generator[int, None, None]:
    n = 4
    yield n
    n *= 2
    yield n
    n = n * 2 - 1
    yield n


def infinite_generator() -> Generator[int, None, None]:
    n = 0
    while True:
        yield n
        n += 2


if __name__ == '__main__':

    g1 = powers_of_two(1_000_000)
    for _ in range(10):
        print(next(g1))

    print()
    g2 = powers_of_two_with_yield(1_000_000)
    for _ in range(10):
        print(next(g2))

    print()
    g3 = my_generator()
    try:
        while True:
            print(next(g3))
    except StopIteration:
        ...

    print()
    for x in my_generator():
        print(x)

    print()
    for x in infinite_generator():
        if x > 10:
            break
        print(x)
