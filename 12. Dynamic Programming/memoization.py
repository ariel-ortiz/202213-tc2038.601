

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


if __name__ == '__main__':
    print([fib_v1(i) for i in range(10)])
    # print(fib_v1(36))
    print()
    print(fib_v2(995))
