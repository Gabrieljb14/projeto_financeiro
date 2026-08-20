from enum import Enum

class Tipo(Enum):
    RECEITA = 1
    DESPESA = 2

class Categoria():

    contador_generio = 0

    def __init__(self, nome: str, tipo: Tipo) ->None:
        self.nomes = set()
        self.tipo = tipo   

    def evita_nomes_duplicados(self, nome)-> None:

        if not nome:
            while  f"Item {self.contador_generio}" in self.nomes:
                self.contador_generio += 1
            nome = f"Item {self.contador_generio}"

        nome_formatado = nome.strip().capitalize()
         
        if nome_formatado in self.nomes:
            raise ValueError(f"O nome {nome_formatado} já existe")
        self.nomes.add(nome_formatado)

               


