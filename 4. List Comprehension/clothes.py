def clothes_combinations(shirts: list[str], pants: list[str]) -> list[str]:
    return [f'{shirt} shirt with {pant} pants'
            for shirt in shirts
            for pant in pants]


if __name__ == '__main__':
    from pprint import pprint

    pprint(clothes_combinations(['green', 'red', 'white'],
                                ['blue', 'black']))
