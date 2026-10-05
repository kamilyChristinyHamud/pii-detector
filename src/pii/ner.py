import spacy

_nlp = None

TERMOS_DOC = {"cpf", "cnpj", "cep", "rg", "cnh", "pis", "email", "e-mail"}


def _carregar():
    global _nlp
    if _nlp is None:
        _nlp = spacy.load("pt_core_news_sm")
    return _nlp


def detect_ner(texto: str) -> list[dict]:
    doc = _carregar()(texto)
    achados = []
    for ent in doc.ents:
        if ent.label_ != "PER":
            continue
        # sigla de documento nunca é nome de pessoa
        if ent.text.lower() in TERMOS_DOC:
            continue
        # palavra única no início da frase: maiúscula engana o modelo
        if len(ent) == 1 and ent.start == ent.sent.start:
            continue
        achados.append(
            {"label": "PERSON", "start": ent.start_char, "end": ent.end_char}
        )
    return achados