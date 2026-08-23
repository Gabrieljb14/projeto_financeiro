from datetime import date
from app.categoria import Tipo
from app.lancamento import Lancamento
from app.validadores import validar_datas


class Fechamento:

    def __init__(
        self, lancamentos: list[Lancamento], data_inicio: date, data_fim: date) -> None:
        self.validar_intervalo_de_datas(data_inicio, data_fim)
        self.data_inicio = data_inicio
        self.data_fim = data_fim
        self.lancamentos = lancamentos

        self.total_receitas = self.calcular_total_receitas()
        self.total_despesas = self.calcular_total_despesas()
        self.saldo = self.total_receitas - self.total_despesas

    @staticmethod
    def validar_intervalo_de_datas(data_inicio: date, data_fim: date) -> None:
        validar_datas(data_inicio, data_fim)

    def obter_lancamentos_do_periodo(self) -> list[Lancamento]:
        return [l for l in self.lancamentos if self.data_inicio <= l.data <= self.data_fim]

    def calcular_total_receitas(self) -> float:
        return sum(l.valor for l in self.obter_lancamentos_do_periodo() if l.categoria.tipo == Tipo.RECEITA)

    def calcular_total_despesas(self) -> float:
        return sum(l.valor for l in self.obter_lancamentos_do_periodo() if l.categoria.tipo == Tipo.DESPESA)