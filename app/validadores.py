def validar_valores_positivos(valor: float) -> None:
    if valor <= 0.0:
        raise ValueError("Registro sem movimentação real!")
    pass