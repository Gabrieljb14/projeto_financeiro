from enum import Enum

class Tipo(Enum):
    RECEITA = 1
    DESPESA = 2

class Categoria():

    contador_generico = 1

    nomes_existentes = set()

    def __init__(self, nome_entrada: str, tipo: Tipo) ->None:
        self.tipo = tipo 
        self.nome = self.valida_e_formata_nome(nome_entrada)

    def valida_e_formata_nome(self, nome: str) -> str:
        if not nome or not nome.strip():
            nome = f"Item {Categoria.contador_generico}"
            while nome in Categoria.nomes_existentes:
                Categoria.contador_generico += 1
                nome = f"Item {Categoria.contador_generico}"     


        nome_formatado = nome.strip().capitalize()

        if nome_formatado in Categoria.nomes_existentes:
            raise ValueError (f"O nome {nome_formatado} já existe!")

        Categoria.nomes_existentes.add(nome_formatado)
        return nome_formatado

    def valida_tipo_de_categoria (self, tipo: Tipo) -> None:
        if not Tipo(None):
            raise ValueError("O tipo da categoria deve ser selecionado")

    @classmethod
    def limpar_estado(cls) -> None:
        cls.nomes_existentes.clear()
        cls.contador_generico = 1


