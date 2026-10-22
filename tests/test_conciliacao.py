import pytest
import math
from datetime import date
from freezegun import freeze_time
from app.conciliacao import Conciliacao
from app.conta import Conta
from app.lancamento import Lancamento
from app.fechamento import Fechamento
from app.categoria import Categoria, Tipo
from decimal import Decimal

class TestConciliacao:

#Teste de validação

    @pytest.fixture(autouse=True)
    def redefinir_estado(self) -> None:
        Categoria.limpar_estado()

    def test_conciliacao_true(self) -> None:
        c = Conta("Alexandre O Grande", Decimal('520.6'))
        categoria_salario = Categoria("Salário", Tipo.RECEITA)
        categoria_imposto = Categoria("Imposto", Tipo.DESPESA)
    
        with freeze_time("2026-01-15"):
            l1 = Lancamento("Pagamento", Decimal('960.8'), categoria_salario)
            l2 = Lancamento("INSS", Decimal('440.2'), categoria_imposto)
    
            f = Fechamento([l1, l2], date(2026, 1, 1), date(2026, 1, 31))
            con = Conciliacao(c, f)
    
            assert con.saldo_conta == Decimal('520.6')
            assert con.saldo_fechamento == Decimal('520.6')
            assert con.diferenca == Decimal('0.0')
            assert con.conciliado is True

    def test_conciliacao_false(self) -> None:
        c = Conta("Alexandre O Grande", Decimal('0.0'))
        categoria_salario = Categoria("Salário", Tipo.RECEITA)
        categoria_imposto = Categoria("Imposto", Tipo.DESPESA)

        with freeze_time("2026-01-15"):
            l1 = Lancamento("Pagamento", Decimal('960.8'), categoria_salario)
            l2 = Lancamento("INSS", Decimal('440.2'), categoria_imposto)

        f = Fechamento([l1, l2], date(2026, 1, 1), date(2026, 1, 31))
        con = Conciliacao(c, f)

        assert con.saldo_conta == Decimal('0.0')
        assert con.saldo_fechamento == Decimal('520.6')
        assert con.diferenca == Decimal('520.6')
        assert con.conciliado is False

#Teste de erro

    def test_conta_e_fechamento_vazios(self) -> None:
        with pytest.raises(ValueError):
            Conciliacao(None, None)

    def test_conta_vazio(self) -> None:
        categoria_salario = Categoria("Salário", Tipo.RECEITA)
        categoria_imposto = Categoria("Imposto", Tipo.DESPESA)

        with freeze_time("2026-01-15"):
            l1 = Lancamento("Pagamento", Decimal('960.8'), categoria_salario)
            l2 = Lancamento("INSS", Decimal('440.2'), categoria_imposto)

        f = Fechamento([l1, l2], date(2026, 1, 1), date(2026, 1, 31))

        with pytest.raises(TypeError):
            Conciliacao(fechamento=f)

    def test_fechamento_vazio(self) -> None:
        c = Conta("Alexandre O Grande", Decimal('1000.0'))
        with pytest.raises(TypeError):
            Conciliacao(conta=c)
