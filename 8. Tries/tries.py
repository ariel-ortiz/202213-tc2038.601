from __future__ import annotations
from typing import Generic, Optional, TypeVar
from collections.abc import Iterator

NUM_LETTERS = ord('z') - ord('a') + 1

T = TypeVar('T')  # Generic type for the Tier class
N = TypeVar('N')  # Generic type for the nested Node class


class Trie(Generic[T]):

    class Node(Generic[N]):

        __children: list[Optional[Trie.Node[N]]]
        __num_children: int
        value: Optional[N]

        def __init__(self) -> None:
            self.__children = ([None] * NUM_LETTERS)
            self.__num_children = 0
            self.value = None

        def __len__(self) -> int:
            return self.__num_children

        def __bool__(self) -> bool:
            return True

        def __getitem__(self, index: int) -> Optional[Trie.Node[N]]:
            return self.__children[index]

        def __setitem__(
                self,
                index: int,
                value: Optional[Trie.Node[N]]) -> None:
            self.__children[index] = value
            self.__num_children += 1

        def __iter__(self) -> Iterator:
            return iter(self.__children)

    __root: Trie.Node[T]

    def __init__(self) -> None:
        self.__root = Trie.Node()

    def insert(self, key: str, value: T) -> None:
        current: Optional[Trie.Node[T]] = self.__root
        for c in key:
            i: int = Trie.__c2i(c)
            if isinstance(current, Trie.Node):
                if not current[i]:
                    current[i] = Trie.Node()
                current = current[i]
        if isinstance(current, Trie.Node):
            current.value = value

    def search(self, key: str) -> Optional[T]:
        current: Optional[Trie.Node[T]] = self.__root
        for c in key:
            i: int = Trie.__c2i(c)
            if isinstance(current, Trie.Node):
                if not current[i]:
                    return None
                current = current[i]
        if isinstance(current, Trie.Node):
            return current.value
        return None

    def remove(self, key: str) -> bool:
        current: Optional[Trie.Node[T]] = self.__root
        for c in key:
            i: int = Trie.__c2i(c)
            if isinstance(current, Trie.Node):
                if not current[i]:
                    return False
                current = current[i]
        if isinstance(current, Trie.Node):
            if current.value is not None:
                current.value = None
                return True
        return False

    @staticmethod
    def __c2i(c: str) -> int:
        return ord(c.lower()) - ord('a')

    @staticmethod
    def __i2c(i: int) -> str:
        return chr(i + ord('a'))


if __name__ == '__main__':
    t: Trie[int] = Trie()
    t.insert('help', 1)
    t.insert('he', 2)
    t.insert('hello', 3)
    t.insert('hello', 10)
    print(t.search('he'))
    print(t.search('hell'))
    print(t.search('hello'))
    print(t.search('ant'))
    print(t.remove('help'))
    print(t.remove('help'))
    print(t.search('help'))
    t.insert('help', 42)
    print(t.search('help'))
