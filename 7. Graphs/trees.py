from collections import deque
from typing import Callable, Optional

Tree = Optional[list]

t: Tree = \
    ['A',
     ['B',
      ['D', None, None],
      None],
     ['C',
      None,
      ['E',
       ['F', None, None],
       ['G', None, None]]]]


def in_order(root: Tree, fun: Callable[[str], None]) -> None:
    if root:
        in_order(root[1], fun)
        fun(root[0])
        in_order(root[2], fun)


def pre_order(root: Tree, fun: Callable[[str], None]) -> None:
    if root:
        fun(root[0])
        pre_order(root[1], fun)
        pre_order(root[2], fun)


def post_order(root: Tree, fun: Callable[[str], None]) -> None:
    if root:
        post_order(root[1], fun)
        post_order(root[2], fun)
        fun(root[0])


def level_order(root: Tree, fun: Callable[[str], None]) -> None:
    queue: deque[Tree] = deque()
    queue.append(root)
    while queue:
        current = queue.popleft()
        if current:
            queue.append(current[1])
            queue.append(current[2])
            fun(current[0])


if __name__ == '__main__':

    in_order(t, print)
    result = ''

    def do_it(value: str) -> None:
        global result
        result += value

    in_order(t, do_it)
    print(result)
    result = ''
    pre_order(t, do_it)
    print(result)
    result = ''
    post_order(t, do_it)
    print(result)
    result = ''
    level_order(t, do_it)
    print(result)
