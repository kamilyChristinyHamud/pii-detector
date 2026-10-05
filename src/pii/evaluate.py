import json
from collections import defaultdict


def carregar(path="data/dataset.jsonl"):
    with open(path, encoding="utf-8") as f:
        return [json.loads(linha) for linha in f]


def igual(a, b):
    return a["label"] == b["label"] and a["start"] == b["start"] and a["end"] == b["end"]


def sobrepoe(a, b):
    return a["label"] == b["label"] and a["start"] < b["end"] and b["start"] < a["end"]


def avaliar(detect, path="data/dataset.jsonl", tolerante=False):
    bate = sobrepoe if tolerante else igual
    stats = defaultdict(lambda: {"tp": 0, "fp": 0, "fn": 0})
    for amostra in carregar(path):
        gold = amostra["entities"]
        pred = detect(amostra["text"])
        for g in gold:
            if any(bate(g, p) for p in pred):
                stats[g["label"]]["tp"] += 1
            else:
                stats[g["label"]]["fn"] += 1
        for p in pred:
            if not any(bate(g, p) for g in gold):
                stats[p["label"]]["fp"] += 1
    return stats


def prf(s):
    tp, fp, fn = s["tp"], s["fp"], s["fn"]
    p = tp / (tp + fp) if tp + fp else 0.0
    r = tp / (tp + fn) if tp + fn else 0.0
    f1 = 2 * p * r / (p + r) if p + r else 0.0
    return p, r, f1


def relatorio(stats, titulo):
    print(f"\n=== {titulo} ===")
    print(f"{'tipo':10} {'prec':>6} {'rec':>6} {'f1':>6}   tp   fp   fn")
    total = {"tp": 0, "fp": 0, "fn": 0}
    for label in sorted(stats):
        s = stats[label]
        p, r, f1 = prf(s)
        print(f"{label:10} {p:6.2f} {r:6.2f} {f1:6.2f} {s['tp']:4} {s['fp']:4} {s['fn']:4}")
        for k in total:
            total[k] += s[k]
    p, r, f1 = prf(total)
    print(f"{'TOTAL':10} {p:6.2f} {r:6.2f} {f1:6.2f} {total['tp']:4} {total['fp']:4} {total['fn']:4}")


if __name__ == "__main__":
    def detector_vazio(texto):
        return []

    relatorio(avaliar(detector_vazio), "estrito (detector vazio)")
    relatorio(avaliar(detector_vazio, tolerante=True), "tolerante (detector vazio)")