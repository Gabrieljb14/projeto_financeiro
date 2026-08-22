from app.validadores import validar_valores_positivos

class Conta:

    def __init__(self, nome: str, saldo: float) -> None:
        self.nome = nome
        self.saldo = saldo

    def _validar_nome(self, nome: str) -> None:
        if not nome or not nome.strip():
            raise ValueError("O nome da conta é obrigatório")

    def adicionar_dinheiro(self, valor: float) -> None:
        validar_valores_positivos(valor)
        self.saldo += valor

    def remover_dinheiro(self, valor: float) -> None:
        validar_valores_positivos(valor)
        if valor > self.saldo:
            raise ValueError("Saldo insuficiente para realizar o saque.")
        self.saldo -= valor

    def visualizar_saldo(self) -> float:
        return self.saldo

#Fazer validação de nome vazio