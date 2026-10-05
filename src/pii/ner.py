import re

import spacy

_nlp = None

TERMOS_DOC = {"cpf", "cnpj", "cep", "rg", "cnh", "pis", "email", "e-mail"}
TRATAMENTO = re.compile(r"\b(?:Sr|Sra|Srta|Dr|Dra|Prof|Profa)\.\s+$")


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
        # nome de pessoa não tem dígito nem @
        if re.search(r"[\d@]", ent.text):
            continue
        # palavra única no início da frase: maiúscula engana o modelo
        if len(ent) == 1 and ent.start == ent.sent.start:
            continue
        # inclui o tratamento (Sr., Sra., Dr....) no trecho do nome
        start = ent.start_char
        m = TRATAMENTO.search(texto[:start])
        if m:
            start = m.start()
        achados.append({"label": "PERSON", "start": start, "end": ent.end_char})
    return achados