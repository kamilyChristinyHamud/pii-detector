import json
import random
import re
from pathlib import Path

from faker import Faker

from src.pii.validators import luhn

Faker.seed(42)
random.seed(42)
fake = Faker("pt_BR")


def invalid_cpf() -> str:
    c = fake.cpf()
    return c[:-1] + str((int(c[-1]) + 1) % 10)


def invalid_card() -> str:
    while True:
        n = "".join(random.choices("0123456789", k=16))
        if not luhn(n):
            return n


GENERATORS = {
    "PERSON": fake.name,
    "CPF": fake.cpf,
    "CNPJ": fake.cnpj,
    "EMAIL": fake.email,
    "PHONE": fake.cellphone_number,
    "CEP": fake.postcode,
    "CARD": fake.credit_card_number,
    "PASSWORD": lambda: fake.password(length=10),
    "ADDRESS": fake.street_address,
    "NEG_CPF": invalid_cpf,
    "NEG_CARD": invalid_card,
}

TEMPLATES = [
    "Cliente {PERSON}, CPF {CPF}, pediu entrega no CEP {CEP}.",
    "Contato: {PERSON} - {EMAIL} - {PHONE}",
    "Pagamento no cartão {CARD} em nome de {PERSON}.",
    "A empresa de CNPJ {CNPJ} solicitou a nota fiscal.",
    "login: {EMAIL} senha: {PASSWORD}",
    "Moro na {ADDRESS}, CEP {CEP}. Pode ligar no {PHONE}.",
    "Código de rastreio {NEG_CPF} registrado na transportadora.",
    "Protocolo {NEG_CARD} aberto na central de atendimento.",
    "Resumo do pedido: 2 itens, total de R$ 189,90, sem dados pessoais.",
    "A reunião será na terça às 14h na sala 3.",
]


def build(template: str) -> dict:
    out, ents, last = "", [], 0
    for m in re.finditer(r"\{(\w+)\}", template):
        out += template[last:m.start()]
        label = m.group(1)
        val = str(GENERATORS[label]()).replace("\n", " ")
        if not label.startswith("NEG_"):
            ents.append({"label": label, "start": len(out), "end": len(out) + len(val)})
        out += val
        last = m.end()
    out += template[last:]
    return {"text": out, "entities": ents}


def main(n: int = 300, path: str = "data/dataset.jsonl") -> None:
    Path(path).parent.mkdir(exist_ok=True)
    with open(path, "w", encoding="utf-8") as f:
        for _ in range(n):
            f.write(json.dumps(build(random.choice(TEMPLATES)), ensure_ascii=False) + "\n")
    print(f"{n} amostras salvas em {path}")


if __name__ == "__main__":
    main()