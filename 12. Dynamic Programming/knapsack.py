
from dataclasses import dataclass
from pprint import pprint


@dataclass
class Item:
    name: str
    weight: int
    cost: int


@dataclass
class Entry:
    value: int
    items: list[Item]


Table = list[list[Entry]]


def compute_cell(item: Item, table: Table, i: int, j: int) -> None:
    if i == 0:
        if item.weight <= j:
            table[i][j] = Entry(item.cost, [item])
    else:
        previous: Entry = table[i - 1][j]
        table[i][j] = previous
        if item.weight <= j:
            remaining_space: Entry = table[i - 1][j - item.weight]
            current: int = item.cost + remaining_space.value
            if current > previous.value:
                table[i][j] = Entry(current,
                                    remaining_space.items + [item])


def solve(size: int, items: list[Item]) -> Table:
    table: Table = [[Entry(0, []) for _ in range(size + 1)]
                    for _ in range(len(items))]
    for i in range(len(table)):
        for j in range(1, len(table[i])):
            compute_cell(items[i], table, i, j)
    return table


if __name__ == '__main__':
    table: Table = solve(4,
                         [Item('Laptop', 3, 2000),
                          Item('Stereo', 4, 3000),
                          Item('iPhone', 1, 2000),
                          Item('Guitar', 1, 1500),
                          Item('MP3', 1, 1000)])
    pprint(table)
