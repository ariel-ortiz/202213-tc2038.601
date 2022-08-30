
def identity_matrix(n: int) -> list[list[int]]:
    return [[1 if row == column else 0 for column in range(n)]
            for row in range(n)]


if __name__ == '__main__':
    from pprint import pprint

    pprint(identity_matrix(10))
