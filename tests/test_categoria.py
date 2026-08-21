import pytest
from app.categoria import Categoria, Tipo

class TestCategoria:

#Teste validação

    @pytest.fixture(autouse=True)
    def redefinir_estado(self) -> None:
        Categoria.limpar_estado() #Limpa a categoria para cada teste

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

    def test_criar_categoria_sem_nome(self) -> None:
         c = Categoria(" ", Tipo.DESPESA)
         assert c.nome == "Item 1"