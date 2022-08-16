

def factorial(n: int) -> int:
    result = 1
    for i in range(1, n + 1):
        result *= i
    return result


print(__name__)

if __name__ == '__main__':
    print('In example 3')
    print(factorial(4))
