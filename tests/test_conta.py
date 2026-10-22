import pytest
from app.conta import Conta
from decimal import Decimal

class TestConta:

    # Testes de validação

    def test_cria_conta(self) -> None:
        c = Conta("Alexandre O Grande", Decimal('960.9'))
        assert c.nome == "Alexandre O Grande"
        assert c.saldo == Decimal('960.9')

    def test_adicionar_dinheiro_sucesso(self) -> None:
        c = Conta("Alexandre O Grande", Decimal('960.9'))
        c.adicionar_dinheiro(Decimal('120.0'))
        assert c.saldo == Decimal('1080.9')

    def test_visualizar_saldo(self) -> float:
        c = Conta("Alexandre O Grande", Decimal('960.9'))
        assert c.saldo == Decimal('960.9')

    # Testes de Erro

    def test_adicionar_dinheiro_excecao(self) -> None:
        c = Conta("Alexandre O Grande", Decimal('960.9'))
        with pytest.raises(ValueError):
            c.adicionar_dinheiro(Decimal('-50.0'))

    def test_validar_nome(self) -> None:
        c = Conta ("  ", Decimal('0.0'))
        with pytest.raises(ValueError):
            c._validar_nome(None)

    def test_adicionar_dinheiro_valor_nulo(self) -> None:
        c = Conta("Alexandre O Grande", Decimal('960.9'))
        with pytest.raises(ValueError):
            c.adicionar_dinheiro(Decimal('0.0'))

    def test_adicionar_dinheiro_valor_nulo(self) -> None:
        c = Conta("Alexandre O Grande", Decimal('960.9'))
        with pytest.raises(ValueError):
            c.adicionar_dinheiro(Decimal('0.0'))