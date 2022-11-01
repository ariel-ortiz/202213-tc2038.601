
def brute_force_search(text: str, pattern: str) -> list[int]:
    result: list[int] = []
    for i in range(len(text) - len(pattern) + 1):
        t = i
        j = 0
        while t < len(text) and j < len(pattern):
            if text[t] != pattern[j]:
                break
            t += 1
            j += 1
        else:
            result.append(i)
    return result


def kmp_table(pattern: str) -> list[int]:
    result: list[int] = [-1] * (len(pattern) + 1)
    result[1] = 0
    prefix_len: int = 0
    i: int = 1
    while i < len(pattern):
        if pattern[prefix_len] == pattern[i]:
            prefix_len += 1
            i += 1
            result[i] = prefix_len
        elif prefix_len > 0:
            prefix_len = result[prefix_len]
        else:
            i += 1
            result[i] = 0
    return result


def kmp_search(text: str, pattern: str) -> list[int]:
    t: int = 0
    p: int = 0
    result: list[int] = []
    table: list[int] = kmp_table(pattern)
    while t < len(text):
        if pattern[p] == text[t]:
            p += 1
            t += 1
            if p == len(pattern):
                result.append(t - p)
                p = table[p]
        else:
            p = table[p]
            if p == -1:
                p = 0
                t += 1
    return result


if __name__ == '__main__':
    # print(brute_force_search('aaaaab', 'aab'))
    # print(brute_force_search('aaaaab', 'aabc'))
    # print(brute_force_search('aabaaab', 'aab'))
    # print(brute_force_search('aabbabbabbabba', 'abba'))
    # print(kmp_table('abcdab'))
    # print(kmp_table('xxyzxxyx'))
    # print(kmp_table('xyzabc'))
    # print(kmp_table('aabc'))
    print(kmp_search('aabbabbabbabba', 'abba'))
