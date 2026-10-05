import spacy

_nlp = None


def _carregar():
    global _nlp
    if _nlp is None:
        _nlp = spacy.load("pt_core_news_sm")
    return _nlp


def detect_ner(texto: str) -> list[dict]:
    doc = _carregar()(texto)
    achados = []
    for ent in doc.ents:
        if ent.label_ == "PER":
            achados.append(
                {"label": "PERSON", "start": ent.start_char, "end": ent.end_char}
            )
    return achados