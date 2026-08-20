import pytest
from app.conta import Conta


class TestConta:

        def test_cria_conta(self) -> None:
        c = Conta("Alexandre O Grande", 960.9)
        assert c.nome == "Alexandre O Grande"
        assert c.saldo == 960.9

    def test_adicionar_dinheiro_sucesso(self) -> None:
        c = Conta("Alexandre O Grande", 960.9)
        c.adicionar_dinheiro(120.0)
        assert c.saldo == 1080.9

    def test_adicionar_dinheiro_excecao(self) -> None:
        c = Conta("Alexandre O Grande", 960.9)
        with pytest.raises(ValueError):
            c.adicionar_dinheiro(-50.0)

    def test_adicionar_dinheiro_valor_nulo(self) -> None:
        c = Conta("Alexandre O Grande", 960.9)
        with pytest.raises(ValueError):
            c.adicionar_dinheiro(0.0)

    def test_adicionar_dinheiro_valor_nulo(self) -> None:
        c = Conta("Alexandre O Grande", 960.9)
        with pytest.raises(ValueError):
            c.adicionar_dinheiro(0.0)