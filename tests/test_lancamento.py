import pytest
from datetime import date
from app.categoria import Categoria, Tipo
from app.lancamento import Lancamento

class TestLancamento:

#Teste de validação

    @pytest.fixture(autouse=True)
    def redefinir_estado(self) -> None:
        Categoria.limpar_estado()

    def test_criar_lancamento(self) -> None:
        categoria_salario = Categoria("Salário", Tipo.RECEITA)
        l = Lancamento("Uber", 20.8, categoria_salario)
        assert l.descricao == "Uber"
        assert l.valor == 20.8
        assert l.categoria == categoria_salario
        assert l.data == date.today()

#Teste de erro

    def test_criar_lancamento_vazio(self) -> None:
            categoria_salario = Categoria("Salário", Tipo.RECEITA)
            l = Lancamento("", 20.8, categoria_salario)
            m = Lancamento("", 20.8, categoria_salario)
            n = Lancamento("", 20.8, categoria_salario)
            assert l.descricao == "Lançamento 1"
            assert m.descricao == "Lançamento 2"
            assert n.descricao == "Lançamento 3"
            assert l.valor == 20.8
            assert l.categoria == categoria_salario
            assert l.data == date.today()

    def test_lancar_valor_vazio(self) -> None:
        categoria_salario = Categoria("Salário", Tipo.RECEITA)
        with pytest.raises(ValueError, match="Registro sem movimentação real!"):
            Lancamento("Uber", 0.0, categoria_salario)

    def test_lancar_categoria_vazia(self) -> None:
          categoria_salario = None
          with pytest.raises(ValueError, match="Categoria não especificada"):
                Lancamento("Ifood", 35.9, categoria_salario)