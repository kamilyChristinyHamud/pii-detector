from src.pii.evaluate import avaliar, relatorio
from src.pii.pipeline import detect_all

relatorio(avaliar(detect_all), "pipeline completo (estrito)")
relatorio(avaliar(detect_all, tolerante=True), "pipeline completo (tolerante)")