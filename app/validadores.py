def validar_valores_positivos(valor: float) -> None:
    if valor <= 0.0:
        raise ValueError("Registro sem movimentação real!")
    pass

from datetime import date

def validar_datas(data_inicio: date, data_fim: date) -> None:
    if not isinstance (data_inicio, date) or not isinstance (data_fim, date):
        raise TypeError("Data de fechamento não identificada")
    if data_fim < data_inicio:
        raise ValueError("Data final não pode ser inferior a data inicial")

