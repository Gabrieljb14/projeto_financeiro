import pytest
from app.conta import Conta

class TestConta:

    # Testes de validação

    def test_cria_conta(self) -> None:
        c = Conta("Alexandre O Grande", 960.9)
        assert c.nome == "Alexandre O Grande"
        assert c.saldo == 960.9

    def test_adicionar_dinheiro_sucesso(self) -> None:
        c = Conta("Alexandre O Grande", 960.9)
        c.adicionar_dinheiro(120.0)
        assert c.saldo == 1080.9

    def test_visualizar_saldo(self) -> float:
        c = Conta("Alexandre O Grande", 960.9)
        assert c.saldo == 960.9

    # Testes de Erro

    def test_adicionar_dinheiro_excecao(self) -> None:
        c = Conta("Alexandre O Grande", 960.9)
        with pytest.raises(ValueError):
            c.adicionar_dinheiro(-50.0)

    def test_validar_nome(self) -> None:
        c = Conta ("  ", 0.0)
        with pytest.raises(ValueError):
            c._validar_nome(None)

    def test_adicionar_dinheiro_valor_nulo(self) -> None:
        c = Conta("Alexandre O Grande", 960.9)
        with pytest.raises(ValueError):
            c.adicionar_dinheiro(0.0)

    def test_adicionar_dinheiro_valor_nulo(self) -> None:
        c = Conta("Alexandre O Grande", 960.9)
        with pytest.raises(ValueError):
            c.adicionar_dinheiro(0.0)