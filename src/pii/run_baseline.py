from src.pii.detectors import detect
from src.pii.evaluate import avaliar, relatorio

relatorio(avaliar(detect), "regex baseline (estrito)")
relatorio(avaliar(detect, tolerante=True), "regex baseline (tolerante)")