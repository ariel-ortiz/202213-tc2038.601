
def mul(m: int, n: int) -> int:
    result = 0
    while m:
        if m & 1:
            result += n
        n <<= 1
        m >>= 1
    return result


if __name__ == '__main__':
    x = 456789
    y = 345121233453425
    print(mul(x, y) == x * y)
