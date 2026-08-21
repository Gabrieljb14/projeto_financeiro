class Conta:

    def __init__(self, nome: str, saldo: float) -> None:
        self.nome = nome
        self.saldo = saldo

    def _validar_nome(self, nome: str) -> None:
        if not nome or not nome.strip():
            raise ValueError("O nome da conta é obrigatório")

    def _validar_valor_positivo(self, valor: float) -> None:
        if valor <= 0.0:
            raise ValueError("Valor de transação indisponível!")

    def adicionar_dinheiro(self, valor: float) -> None:
        self._validar_valor_positivo(valor)
        self.saldo += valor

    def remover_dinheiro(self, valor: float) -> None:
        self._validar_valor_positivo(valor)
        if valor > self.saldo:
            raise ValueError("Saldo insuficiente para realizar o saque.")
        self.saldo -= valor

    def visualizar_saldo(self) -> float:
        return self.saldo

#Fazer validação de nome vazio