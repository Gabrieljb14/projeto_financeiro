import pytest
from datetime import date
from freezegun import freeze_time
from app.categoria import Categoria, Tipo
from app.lancamento import Lancamento
from app.fechamento import Fechamento
from app.extrato import Extrato

class TestExtrato:

    @pytest.fixture(autouse=True)
    def redefinir_estado(self) -> None:
        Categoria.limpar_estado()

# Teste de validação

    def test_calcula_totais_corretamente(self) -> None:
        categoria_receita = Categoria("", Tipo.RECEITA)
        categoria_despesa = Categoria("", Tipo.DESPESA)

        with freeze_time("2026-01-01"):
            l1 = Lancamento("Salário", 960.9, categoria_receita)
        with freeze_time("2026-01-10"):
            l2 = Lancamento("Aluguel", 400.0, categoria_despesa)

        with freeze_time("2026-06-01"):
            l3 = Lancamento("Salário", 960.9, categoria_receita)
        with freeze_time("2026-06-10"):
            l4 = Lancamento("Aluguel", 400.0, categoria_despesa)
                    
            f1 = Fechamento([l1, l2], date(2026, 1, 1), date(2026, 1, 31))
            f2 = Fechamento([l3, l4], date(2026, 6, 1), date(2026, 6, 30))

            e = Extrato([f1, f2], data_inicio=date(2026, 1, 1), data_fim=date(2026, 6, 30))

            assert e.total_despesas == 800.0
            assert e.total_receitas == 1921.8
            assert e.saldo == 1121.8

    def test_ignora_fechamento_fora_do_periodo(self) -> None:
        categoria_receita = Categoria("", Tipo.RECEITA)
        categoria_despesa = Categoria("", Tipo.DESPESA)
        
        with freeze_time("2026-01-01"):
            l1 = Lancamento("Salário", 960.9, categoria_receita)
        with freeze_time("2026-01-10"):
            l2 = Lancamento("Aluguel", 400.0, categoria_despesa)
        
        with freeze_time("2026-06-01"):
            l3 = Lancamento("Salário", 960.9, categoria_receita)
        with freeze_time("2026-06-10"):
            l4 = Lancamento("Aluguel", 400.0, categoria_despesa)
                            
            f1 = Fechamento([l1, l2], date(2025, 12, 1), date(2025, 12, 31))   
            f2 = Fechamento([l3, l4], date(2026, 6, 1), date(2026, 6, 30))

        e = Extrato([f1, f2], data_inicio=date(2026, 1, 1), data_fim=date(2026, 6, 30))

        assert e.saldo == 560.9

    def test_lista_vazia_gera_totais_zerados(self) -> None:
        e = Extrato([], date(2026, 1, 1), date(2026, 6, 30))
        assert e.total_receitas == 0
        assert e.total_despesas == 0
        assert e.saldo == 0

    def test_data_fim_anterior_a_data_inicio_gera_erro(self) -> None:
        with pytest.raises(ValueError):
            Extrato([], date(2026, 6, 30), date(2026,1,1))

    def test_data_com_tipo_invalido_gera_erro(self) -> None:
        with pytest.raises(TypeError):
            Extrato([],"2026-06-30", "2026-06-30")