import re

from src.pii.validators import luhn, valid_cnpj, valid_cpf

PATTERNS = {
    "CPF": re.compile(r"(?<!\d)\d{3}\.?\d{3}\.?\d{3}-?\d{2}(?!\d)"),
    "CNPJ": re.compile(r"(?<!\d)\d{2}\.?\d{3}\.?\d{3}/?\d{4}-?\d{2}(?!\d)"),
    "CARD": re.compile(r"(?<!\d)(?:\d[ -]?){11,18}\d(?!\d)"),
    "EMAIL": re.compile(r"[\w.+-]+@[\w-]+(?:\.[\w-]+)+"),
    "PASSWORD": re.compile(r"(?i)\b(?:senha|password|pwd)\s*[:=]\s*(\S+)"),
    "PHONE": re.compile(
        r"(?<!\d)(?:\+55[\s-]?)?(?:\(0?\d{2}\)|0?\d{2})[\s-]?9[\s-]?\d{4}[\s-]?\d{4}(?!\d)"
    ),
    "CEP": re.compile(r"(?<!\d)\d{5}-?\d{3}(?!\d)"),
}

VALIDADORES = {"CPF": valid_cpf, "CNPJ": valid_cnpj, "CARD": luhn}

# ordem = prioridade em caso de sobreposição
PRIORIDADE = ["CPF", "CNPJ", "PHONE", "CARD", "EMAIL", "PASSWORD", "CEP"]


def detect(texto: str) -> list[dict]:
    candidatos = []
    for label in PRIORIDADE:
        grupo = 1 if label == "PASSWORD" else 0
        for m in PATTERNS[label].finditer(texto):
            validador = VALIDADORES.get(label)
            if validador and not validador(m.group(grupo)):
                continue
            candidatos.append(
                {"label": label, "start": m.start(grupo), "end": m.end(grupo)}
            )

    aceitos = []
    for c in candidatos:
        if not any(c["start"] < a["end"] and a["start"] < c["end"] for a in aceitos):
            aceitos.append(c)
    return sorted(aceitos, key=lambda e: e["start"])

def test_telefone_nao_vira_cartao():
    achados = {e["label"] for e in detect("Pode ligar no +55 46 98196-0013")}
    assert achados == {"PHONE"}