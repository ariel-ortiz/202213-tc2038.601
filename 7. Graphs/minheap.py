from heapq import heapify, heappop


def heap_sort(a: list[int]) -> None:
    heapify(a)
    result: list[int] = []
    while a:
        result.append(heappop(a))
    a[:] = result


if __name__ == '__main__':
    data = [7, 2, 5, 6, 1, 4]
    # heapify(data)
    # print(data)
    # x = heappop(data)
    # print()
    # print(x)
    # print(data)
    # x = heappop(data)
    # print()
    # print(x)
    # print(data)
    heap_sort(data)
    print(data)
