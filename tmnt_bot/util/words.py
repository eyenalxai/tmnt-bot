from spacy import Language as SpacyLanguage


def extract_words_only(*, nlp: SpacyLanguage, text: str) -> list[str]:
    doc = nlp(text=text)
    filtered_tokens = [token.text for token in doc if token.is_alpha]
    return filtered_tokens
