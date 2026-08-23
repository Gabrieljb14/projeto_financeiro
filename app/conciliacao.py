import math
from app.conta import Conta
from app.fechamento import Fechamento

class Conciliacao:

    def __init__(self, conta: Conta, fechamento: Fechamento) -> None:
        if not isinstance (conta, Conta):
            raise ValueError("Conta não especificada")
        elif not isinstance (fechamento, Fechamento):
            raise ValueError("Fechamento não especificado")
        self.saldo_conta = conta.saldo
        self.saldo_fechamento = fechamento.saldo
        self.diferenca = round(abs(self.saldo_fechamento - self.saldo_conta), 2)
        self.conciliado = math.isclose(self.saldo_conta, self.saldo_fechamento, abs_tol=0.01)
