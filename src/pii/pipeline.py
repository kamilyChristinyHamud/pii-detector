from src.pii.detectors import detect
from src.pii.ner import detect_ner


def detect_all(texto: str) -> list[dict]:
    aceitos = list(detect(texto))
    for e in detect_ner(texto):
        if not any(e["start"] < a["end"] and a["start"] < e["end"] for a in aceitos):
            aceitos.append(e)
    return sorted(aceitos, key=lambda x: x["start"])