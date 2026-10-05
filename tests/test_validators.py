from src.pii.validators import valid_cpf, valid_cnpj, luhn


def test_cpf():
    assert valid_cpf("529.982.247-25")
    assert not valid_cpf("111.111.111-11")
    assert not valid_cpf("529.982.247-24")


def test_cnpj():
    assert valid_cnpj("11.222.333/0001-81")
    assert not valid_cnpj("11.222.333/0001-80")


def test_luhn():
    assert luhn("4111 1111 1111 1111")
    assert not luhn("4111 1111 1111 1112")