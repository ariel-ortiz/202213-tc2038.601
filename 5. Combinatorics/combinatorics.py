
def power_set(s: list[int]) -> list[list[int]]:
    if s:
        r = power_set(s[:-1])
        return r + [t + [s[-1]] for t in r]
    else:
        return [[]]


def sorted_nicely(s: list[list[int]]) -> list[list[int]]:

    def compare_by_size_and_content(t: list[int]) -> tuple[int, list[int]]:
        return (len(t), t)

    return sorted(s, key=compare_by_size_and_content)


def combinations(s: list[int], n: int) -> list[list[int]]:
    return [t for t in power_set(s) if len(t) == n]


if __name__ == '__main__':
    from pprint import pprint

    pprint(sorted_nicely(power_set([1, 2, 3, 4])))
    print()
    pprint(sorted_nicely(combinations([1, 2, 3, 4], 2)))
