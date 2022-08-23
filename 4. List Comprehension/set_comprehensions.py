def powers_of_two(n: int) -> set[int]:
    return {2 ** x for x in range(n)}


def abs_values(a: list[int]) -> set[int]:
    return {abs(x) for x in a}


if __name__ == '__main__':
    print(powers_of_two(5))
    print(abs_values([1, 2, -1, -2, 3, -4]))
