from src.pii.evaluate import avaliar, relatorio
from src.pii.ner import detect_ner

for tolerante in (False, True):
    stats = avaliar(detect_ner, tolerante=tolerante)
    nome = "tolerante" if tolerante else "estrito"
    relatorio({"PERSON": stats["PERSON"]}, f"spaCy sm, PERSON ({nome})")