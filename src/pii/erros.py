import sys

from src.pii.detectors import detect
from src.pii.evaluate import carregar


def main(label: str, max_ex: int = 6) -> None:
    achados = 0
    for amostra in carregar():
        texto = amostra["text"]
        gold = {(e["start"], e["end"]) for e in amostra["entities"] if e["label"] == label}
        pred = {(e["start"], e["end"]) for e in detect(texto) if e["label"] == label}
        if gold != pred:
            print("TEXTO:", texto)
            print("  esperado: ", [texto[s:e] for s, e in sorted(gold)])
            print("  detectado:", [texto[s:e] for s, e in sorted(pred)])
            achados += 1
            if achados >= max_ex:
                break


if __name__ == "__main__":
    main(sys.argv[1])