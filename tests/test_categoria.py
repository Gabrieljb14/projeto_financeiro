import pytest
from app.categoria import Categoria, Tipo

class TestCategoria:

#Teste validação

    @pytest.fixture(autouse=True)
    def redefinir_estado(self) -> None:
        Categoria.limpar_estado()

    def test_criar_categoria_receita(self) -> None:
        c = Categoria("Salário", Tipo.RECEITA)
        assert c.nome == "Salário"
        assert c.tipo == Tipo.RECEITA

    def test_criar_categoria_despesa(self) -> None:
            c = Categoria("Imposto", Tipo.DESPESA)
            assert c.nome == "Imposto"
            assert c.tipo == Tipo.DESPESA

#Teste de erro

    def test_criar_categoria_duplicada(self) -> None:
         Categoria("Salário", Tipo.DESPESA)
         with pytest.raises(ValueError):
              Categoria("Salário", Tipo.DESPESA)

    def test_criar_categoria_sem_nome_em_sequencia(self) -> None:
        c = Categoria("", Tipo.RECEITA)
        d = Categoria("", Tipo.DESPESA)
        e = Categoria("", Tipo.DESPESA)
        f = Categoria("", Tipo.RECEITA)
        g = Categoria("", Tipo.RECEITA)
        assert c.nome == "Item 1"
        assert d.nome == "Item 2"
        assert e.nome == "Item 3"
        assert f.nome == "Item 4"
        assert g.nome == "Item 5"

    def test_valida_tipo_de_categoria(self) -> None:
        c = Categoria("Salário", None)
        with pytest.raises(ValueError):
             c.valida_tipo_de_categoria(None)