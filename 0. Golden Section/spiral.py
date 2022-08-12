from math import sqrt
from turtle import fd, rt, done, circle, pencolor, pensize, speed


PHI = 1 / ((sqrt(5) - 1) / 2)


def spiral(times: int) -> None:
    length = 5.0
    for _ in range(times):
        circle(length, 90)
        length *= PHI


if __name__ == '__main__':
    print(f'phi = {PHI}')
    pensize(5)
    pencolor('medium purple')
    speed('fastest')
    spiral(9)
    done()
