from typing import Optional


def find(s: str, words: set[str], answer: list[str]) -> Optional[list[str]]:
    if not s:
        return answer
    index: int = 0
    word: str = ''
    while index < len(s):
        word += s[index]
        if word in words:
            new_answer = find(s[index + 1:], words, answer + [word])
            if new_answer:
                return new_answer
        index += 1
    return None


def word_break(s: str, words: set[str]) -> Optional[str]:
    result = find(s, words, [])
    if result:
        return ' '.join(result)
    return None


if __name__ == '__main__':
    words = {'the', 'them', 'school', 'dog',
             'ran', 'to', 'he', 'she', 'ate'}
    print(word_break('themdog', words))
