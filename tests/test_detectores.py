from src.pii.detectors import detect


def labels(texto):
    return {e["label"] for e in detect(texto)}


def test_cpf_valido_e_invalido():
    assert "CPF" in labels("CPF 529.982.247-25")
    assert "CPF" not in labels("CPF 529.982.247-24")


def test_cartao_luhn():
    assert "CARD" in labels("cartão 4111 1111 1111 1111")
    assert "CARD" not in labels("protocolo 4111 1111 1111 1112")


def test_email_e_senha():
    achados = labels("login: ana@example.com senha: abc123XYZ!")
    assert {"EMAIL", "PASSWORD"} <= achados

def test_telefone_nao_vira_cartao():
    achados = {e["label"] for e in detect("Pode ligar no +55 46 98196-0013")}
    assert achados == {"PHONE"}

def test_endereco():
    achados = detect("Moro na Rua das Flores, 123, CEP 80000-000.")
    enderecos = [e for e in achados if e["label"] == "ADDRESS"]
    assert len(enderecos) == 1