from lingua import Language as LinguaLanguage
from result import Err, Ok, Result
from spacy import Language as SpacyLanguage


def get_spacy_model_by_language(
    *,
    language: LinguaLanguage | None,
    nlp_en: SpacyLanguage,
    nlp_ru: SpacyLanguage,
) -> Result[SpacyLanguage, str]:
    if language == LinguaLanguage.ENGLISH:
        return Ok(nlp_en)

    if language == LinguaLanguage.RUSSIAN:
        return Ok(nlp_ru)

    return Err("No spacy model for language")
