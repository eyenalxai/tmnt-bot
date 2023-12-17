from pyphen import Pyphen  # type: ignore


def count_syllables(*, pyphen: Pyphen, words: list[str]) -> int:
    return sum(len(pyphen.inserted(word=w).split("-")) for w in words)
