

from functools import cache, lru_cache
from typing import Callable


def memoize(fn: Callable[[int], int]) -> Callable[[int], int]:

    my_cache: dict[int, int] = {}

    def local_fun(x: int) -> int:
        if x not in my_cache:
            my_cache[x] = fn(x)
        return my_cache[x]

    return local_fun


@memoize
def fib_v1(n: int) -> int:
    match n:
        case 0 | 1:
            return n
        case _:
            return fib_v1(n - 1) + fib_v1(n - 2)


my_cache: dict[int, int] = {0: 0, 1: 1}


def fib_v2(n: int) -> int:
    if n in my_cache:
        return my_cache[n]
    result = fib_v2(n - 1) + fib_v2(n - 2)
    my_cache[n] = result
    return result


@memoize
def pow2(x: int) -> int:
    return 2 ** x


@cache
def fib_v3(n: int) -> int:
    print(f'Calling fib_v3 with n = {n}')
    if n < 2:
        return n
    return fib_v3(n - 1) + fib_v3(n - 2)


if __name__ == '__main__':
    print([fib_v1(i) for i in range(10)])
    # print(fib_v1(36))
    print()
    print(fib_v2(995))
    # fib_v1 = memoize(fib_v1)  # type: ignore
    # pow2 = memoize(pow2)  # type: ignore
    print(fib_v1(100))
    print(fib_v1(5))
    print(pow2(10))
    print(fib_v3(5))
    print(fib_v3(3))
