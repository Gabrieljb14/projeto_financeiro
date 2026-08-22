import pytest
from datetime import date
from app.categoria import Categoria, Tipo
from app.fechamento import Fechamento
from app.lancamento import Lancamento

class TestFechamento:

#Teste de validação

    def filtrando_fechamento(self) -> None:
        cat_receita = Categoria("Salário", Tipo.RECEITA)
        cat_despesa = Categoria("Imposto", Tipo.DESPESA)
        l1 = Lancamento("Pagamento", 1500.0, cat_receita)
        l2 = Lancamento("IPTU", 100.0, cat_despesa)

        fechamento = Fechamento (lancamentos=[l1, l2], data_inicio=(2026/8/1), data_fim=(2026/8/31))

        filtrados = fechamento.obter_lancamentos_do_periodo()

#Teste de erro

    