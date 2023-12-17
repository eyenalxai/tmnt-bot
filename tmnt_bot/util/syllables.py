from lingua import Language as LinguaLanguage
from pyphen import Pyphen  # type: ignore
from result import Err, Ok, Result


def count_syllables_in_word(
    *,
    language: LinguaLanguage,
    pyphen: Pyphen,
    cmudict_dict: dict,
    word: str,
) -> Result[int, str]:
    if language == LinguaLanguage.ENGLISH:
        try:
            return Ok(
                [
                    len(list(y for y in x if y[-1].isdigit()))
                    for x in cmudict_dict[word.lower()]
                ][0]
            )
        except KeyError:
            return Ok(len(pyphen.inserted(word=word).split("-")))

    if language == LinguaLanguage.RUSSIAN:
        vowels = ["а", "е", "ё", "и", "о", "у", "ы", "э", "ю", "я"]
        return Ok(sum(letter in vowels for letter in word.lower()))

    return Err("Cannot count syllables in word because language is not supported")


def count_syllables(
    *,
    language: LinguaLanguage,
    pyphen: Pyphen,
    cmudict_dict: dict,
    words: list[str],
) -> Result[int, str]:
    syllables_count = 0
    for word in words:
        word_syllables_count = count_syllables_in_word(
            language=language,
            pyphen=pyphen,
            cmudict_dict=cmudict_dict,
            word=word,
        )

        if isinstance(word_syllables_count, Err):
            return Err(word_syllables_count.err_value)

        syllables_count += word_syllables_count.ok_value

    return Ok(syllables_count)
