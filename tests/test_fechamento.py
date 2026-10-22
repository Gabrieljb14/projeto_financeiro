import pytest
from datetime import date
from app.categoria import Categoria, Tipo
from app.fechamento import Fechamento
from app.lancamento import Lancamento
from freezegun import freeze_time
from decimal import Decimal

class TestFechamento:

#Teste de validação

    @pytest.fixture(autouse=True)
    def redefinir_estado(self) -> None:
        Categoria.limpar_estado()

    def test_calcula_totais_corretamente(self) -> None:
        categoria_receita = Categoria("Salário", Tipo.RECEITA)
        categoria_despesa = Categoria("Aluguel", Tipo.DESPESA)

        with freeze_time("2026, 01, 05"):
            l1 = Lancamento("Salário", Decimal('960.9'), categoria_receita)
        with freeze_time("2026, 01, 10"):
            l2 = Lancamento("Aluguel", Decimal('400.0'), categoria_despesa)

        f = Fechamento([l1, l2], date(2026, 1, 1), date(2026, 1, 31))

        assert f.total_receitas == Decimal('960.9')
        assert f.total_despesas == Decimal('400.0')
        assert f.saldo == Decimal('560.9')

#Teste de erro

    def test_ignora_lancamento_fora_do_periodo(self) -> None:
        categoria_receita = Categoria("Salário", Tipo.RECEITA)
        categoria_despesa = Categoria("Aluguel", Tipo.DESPESA)
            
        with freeze_time("2026-01-05"):
            l1 = Lancamento("Salário", Decimal(960.9), categoria_receita)
        with freeze_time("2026-01-10"):
            l2 = Lancamento("Aluguel", Decimal(400.0), categoria_despesa)
            
            f = Fechamento([l1, l2], date(2026, 1, 6), date(2026, 1, 31))
    
            assert len(f.obter_lancamentos_do_periodo()) == 1
            assert f.total_despesas == Decimal(400.0)
            assert f.total_receitas == Decimal(0.0)
            assert f.saldo == Decimal(-400.0)

    def test_lista_vazia_gera_saldo_zerado(self) -> None:
        f = Fechamento([], date(2026,1,1), date(2026,1,31))

        assert f.total_despesas == Decimal(0.0)
        assert f.total_receitas == Decimal(0.0)
        assert f.saldo == Decimal(0.0)

    def test_data_fim_anterior_a_data_comeco(self) -> None:
         with pytest.raises(ValueError):
              Fechamento([], date(2026,1,31), date(2026,1,1))

    def test_data_com_tipagem_errada(self) -> None:
         with pytest.raises(TypeError):
              Fechamento([], "2026,1,1", "2026,1,31")