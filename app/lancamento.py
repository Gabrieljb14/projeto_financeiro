from datetime import date
from app.categoria import Categoria
from app.validadores import validar_valores_positivos

class Lancamento:

    contador_generico = 1


    def __init__(self, descricao_entrada: str, valor: float, categoria: Categoria, data: date) -> None:
        if not isinstance (categoria, Categoria):
            raise ValueError("Categoria não especificada")
        self.categoria = categoria
        Lancamento.validar_valor(valor)
        self.valor = valor
        self.descricao = self.valida_e_formata_descricao(descricao_entrada)
        self.data = date.today()

    @staticmethod
    def validar_valor(valor: float) -> None:
        validar_valores_positivos(valor)
        if valor == 0.0:
            raise ValueError("Registro sem movimentação real")
    
    def valida_e_formata_descricao(self, descricao: str) -> str:
        if not descricao or not descricao.strip():
            descricao = f"Lançamento {Lancamento.contador_generico}"
            Lancamento.contador_generico += 1
     
    
        descricao_formatada = descricao.strip().capitalize()
        return descricao_formatada
        