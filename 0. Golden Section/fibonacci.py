def fibonacci(n: int) -> int:
    a = 0
    b = 1
    for _ in range(n + 1):
        a, b = b, a + b
    return a


if __name__ == '__main__':
    prev = 1
    for i in range(2, 100):
        current = fibonacci(i)
        print(f'fibonacci({i}) = {current}, phi = {current /  prev}')
        prev = current
