# PII-Detector

Detector de dados pessoais em textos em português, feito em Python e 100% local.

## Sobre

Criei esse projeto porque dados pessoais aparecem em todo tipo de texto, como logs, chamados e e-mails, e muitas vezes passam despercebidos. O programa lê um texto e mostra onde estão dados como CPF e nomes de pessoas, sem enviar nada para serviços externos.

Ele faz parte dos meus estudos em privacidade, LGPD e Privacy by Design.

## Como funciona

O detector trabalha em duas camadas:

- **Regex e validadores:** encontram padrões como o CPF e conferem se o número é válido, usando os dígitos verificadores.
- **NER com spaCy (modelo `pt_core_news_sm`):** encontra o que a regex não alcança, como nomes de pessoas.

O resultado das duas camadas é combinado em uma lista só.

## Resultados

Avaliei o detector em um dataset sintético gerado com Faker, que já traz as respostas certas para comparação.

| Abordagem | Precisão | Recall | F1 |
|---|:---:|:---:|:---:|
| Só regex | 1.00 | 0.73 | 0.84 |
| Regex + spaCy | 1.00 | 0.96 | 0.98 |

A regex sozinha nunca erra o que encontra, mas não enxerga nomes. Com o spaCy, o recall subiu de 0.73 para 0.96 sem perder precisão. Os nomes de pessoas ainda são o ponto mais fraco (recall de 0.80).

Um aviso importante: dados sintéticos são mais fáceis que textos reais. Por isso, o próximo passo é testar com formatos mais difíceis.

## Como rodar

Você precisa do Python 3.11 e do Git.

```bash
git clone https://github.com/kamilyChristinyHamud/pii-detector.git
cd pii-detector

python -m venv venv
venv\Scripts\activate

pip install presidio-analyzer faker spacy
python -m spacy download pt_core_news_sm
```

## Próximos passos

- Testar com um conjunto de dados mais difícil
- Mascarar os dados encontrados (por exemplo, `123.456.789-00` vira `[CPF]`)
- Gerar um relatório de auditoria sem guardar o dado original
- Criar uma interface de linha de comando


Kamily Hamud, estudante de Cibersegurança.

[LinkedIn](https://www.linkedin.com/in/kamily-hamud) 
