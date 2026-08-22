from datetime import date
from app.categoria import Categoria
from app.validadores import validar_valores_positivos

class Lancamento:

    contador_generico = 1

    descricoes_existentes = set()

    def __init__(self, descricao_entrada: str, valor: float, categoria: Categoria) -> None:
        if not isinstance (categoria, Categoria):
            raise ValueError("Categoria não especificada")
        self.categoria = categoria
        self.validar_valor(valor)
        self.valor = valor
        self.descricao = self.valida_e_formata_descricao(descricao_entrada)
        self.data = date.today

    @staticmethod
    def validar_valor(valor: float) -> None:
        validar_valores_positivos(valor)
    
    def valida_e_formata_descricao(self, descricao: str) -> str:
        if not descricao or not descricao.strip():
            descricao = f"Lançamento {Lancamento.contador_generico}"


        while descricao in Lancamento.descricoes_existente:
            Lancamento.contador_generico += 1
            descricao = f"Lançamento {Lancamento.contador_generico}"     
    
        Lancamento.descricoes_existentes.add(descricao)
        descricao_formatada = descricao.strip().capitalize()
        return descricao_formatada
        