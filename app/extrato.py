from datetime import date
from app.fechamento import Fechamento
from app.validadores import validar_datas

class Extrato:

    def __init__(self, fechamentos: list[Fechamento], data_inicio: date, data_fim: date) -> None:
        self.validar_intervalo_de_datas(data_inicio, data_fim)
        self.data_inicio = data_inicio
        self.data_fim = data_fim
        fechamentos_periodo = self.obter_fechamentos_do_periodo(fechamentos)
        self.total_receitas = self.calcular_total_receitas(fechamentos_periodo)
        self.total_despesas = self.calcular_total_despesas(fechamentos_periodo)
        self.saldo = self.total_receitas - self.total_despesas

    @staticmethod
    def validar_intervalo_de_datas(data_inicio: date, data_fim: date) -> None:
        validar_datas(data_inicio, data_fim)

    def obter_fechamento_do_periodo(self, fechamentos   )