from app.lancamento import Lancamento, Tipo

class TestLancamento:

    def test_criar_lancamento(self) -> None:
        l = ("Uber", 20.8, Tipo.DESPESA)
        assert l.descricao == "Uber"
        assert l.descricao == 20.8
        assert l.categoria == Tipo.DESPESA