from lingua import Language as LinguaLanguage
from pyphen import Pyphen  # type: ignore
from result import Err, Ok, Result


def get_pyphen_by_language(*, language: LinguaLanguage | None) -> Result[Pyphen, str]:
    if language == LinguaLanguage.ENGLISH:
        return Ok(Pyphen(lang="en_US"))

    if language == LinguaLanguage.RUSSIAN:
        return Ok(Pyphen(lang="ru_RU"))

    return Err("No pyphen model for language")
