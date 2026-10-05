import re

from src.pii.validators import luhn, valid_cnpj, valid_cpf

PREFIXOS_VIA = (
    "Aeroporto|Alameda|Área|Avenida|Campo|Chácara|Colônia|Condomínio|Conjunto|Distrito|"
    "Esplanada|Estação|Estrada|Favela|Fazenda|Feira|Jardim|Ladeira|Lago|Lagoa|Largo|"
    "Loteamento|Morro|Núcleo|Parque|Passarela|Pátio|Praça|Praia|Quadra|Recanto|Residencial|"
    "Rodovia|Rua|Setor|Sítio|Travessa|Trecho|Trevo|Vale|Vereda|Via|Viaduto|Viela|Vila"
)
LIGACAO = r"(?:de|da|do|das|dos|e)"
PALAVRA = r"[A-ZÀ-ÖØ-Þ][^\W\d_]*"
ADDRESS_RE = re.compile(
    rf"\b(?:{PREFIXOS_VIA})\s+(?:{LIGACAO}\s+)?{PALAVRA}"
    rf"(?:\s+(?:{LIGACAO}\s+)?{PALAVRA})*(?:,\s*\d{{1,5}}(?!\d))?"
)

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
    "ADDRESS": ADDRESS_RE,
}

VALIDADORES = {"CPF": valid_cpf, "CNPJ": valid_cnpj, "CARD": luhn}

# ordem = prioridade em caso de sobreposição
PRIORIDADE = ["CPF", "CNPJ", "PHONE", "CARD", "EMAIL", "PASSWORD", "CEP", "ADDRESS"]


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