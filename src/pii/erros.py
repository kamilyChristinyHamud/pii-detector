import sys

from src.pii.detectors import detect
from src.pii.evaluate import carregar
from src.pii.ner import detect_ner


def main(label: str, modo: str = "regex", tipo: str = "fp", max_ex: int = 8) -> None:
    detector = detect_ner if modo == "ner" else detect
    achados = 0
    for amostra in carregar():
        texto = amostra["text"]
        gold = {(e["start"], e["end"]) for e in amostra["entities"] if e["label"] == label}
        pred = {(e["start"], e["end"]) for e in detector(texto) if e["label"] == label}
        alvo = (pred - gold) if tipo == "fp" else (gold - pred)
        if alvo:
            print("TEXTO:", texto)
            print("  esperado: ", [texto[s:e] for s, e in sorted(gold)])
            print("  detectado:", [texto[s:e] for s, e in sorted(pred)])
            achados += 1
            if achados >= max_ex:
                break


if __name__ == "__main__":
    modo = sys.argv[2] if len(sys.argv) > 2 else "regex"
    tipo = sys.argv[3] if len(sys.argv) > 3 else "fp"
    main(sys.argv[1], modo, tipo)