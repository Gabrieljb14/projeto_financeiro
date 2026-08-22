def validar_valores_positivos(valor: float) -> None:
    if valor <= 0.0:
        raise ValueError("Valor de transação indisponível!")
    pass