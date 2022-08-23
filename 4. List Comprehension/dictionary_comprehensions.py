def powers_of_two(n: int) -> dict[int, int]:
    return {k: 2 ** k for k in range(n)}


if __name__ == '__main__':
    d = powers_of_two(11)
    print(f'd[10] = {d[10]}')
    for key, value in d.items():
        print(f'{key:2}:{value:5}')
