import re


def only_digits(s: str) -> str:
    return re.sub(r"\D", "", s)


def valid_cpf(s: str) -> bool:
    d = only_digits(s)
    if len(d) != 11 or d == d[0] * 11:
        return False
    for i in (9, 10):
        soma = sum(int(d[j]) * (i + 1 - j) for j in range(i))
        if (soma * 10 % 11) % 10 != int(d[i]):
            return False
    return True


def valid_cnpj(s: str) -> bool:
    d = only_digits(s)
    if len(d) != 14 or d == d[0] * 14:
        return False
    pesos1 = [5, 4, 3, 2, 9, 8, 7, 6, 5, 4, 3, 2]
    pesos2 = [6] + pesos1
    for pesos, pos in ((pesos1, 12), (pesos2, 13)):
        r = sum(int(n) * p for n, p in zip(d, pesos)) % 11
        dv = 0 if r < 2 else 11 - r
        if dv != int(d[pos]):
            return False
    return True


def luhn(s: str) -> bool:
    d = only_digits(s)
    if not 13 <= len(d) <= 19:
        return False
    total = 0
    for i, ch in enumerate(reversed(d)):
        n = int(ch)
        if i % 2 == 1:
            n = n * 2 - 9 if n * 2 > 9 else n * 2
        total += n
    return total % 10 == 0