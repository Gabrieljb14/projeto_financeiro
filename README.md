# Projeto Financeiro

Situação do projeto

Este é o meu primeiro projeto de Programação Orientada a Objetos com testes automatizados. A ideia é construir, passo a passo, um pequeno sistema de controle financeiro: contas, categorias, lançamentos, fechamentos mensais, conciliação bancária e extratos — sempre com uma bateria de testes cobrindo cada classe.

Este README documenta as classes, as decisões de projeto tomadas ao longo do caminho e o raciocínio por trás delas. Mais do que "o que o código faz", o objetivo aqui é registrar **por que** ele foi feito assim.

---

## Índice

- [Passo 1 — Preparando o ambiente](#passo-1--preparando-o-ambiente)
- [Passo 2 — O pacote `app`](#passo-2--o-pacote-app)
- [Passo 3 — Conta](#passo-3--conta)
- [Passo 4 — Categoria](#passo-4--categoria)
- [Passo 5 — Validadores compartilhados](#passo-5--validadores-compartilhados)
- [Passo 6 — Lancamento](#passo-6--lancamento)
- [Passo 7 — Fechamento](#passo-7--fechamento)
- [Passo 8 — Conciliacao](#passo-8--conciliacao)
- [Passo 9 — Extrato](#passo-9--extrato)
- [Passo 10 — Rodando tudo](#passo-10--rodando-tudo)
- [Resumo do que aprendi](#resumo-do-que-aprendi)
- [Próximos passos e melhorias possíveis](#próximos-passos-e-melhorias-possíveis)

---

## Passo 1 — Preparando o ambiente

```
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

O `requirements.txt` traz o `pytest` como dependência principal para os testes. Os testes de `Fechamento`, `Extrato` e `Conciliacao` também dependem do **`freezegun`**, usado para simular datas diferentes na criação dos lançamentos sem depender da data real do sistema — vale lembrar de instalá-lo à parte (`pip install freezegun`) se ele ainda não estiver no `requirements.txt`.

---

## Passo 2 — O pacote `app`

O código-fonte fica todo dentro da pasta `app/`, e os testes em `tests/` — cada classe tem seu próprio arquivo, e cada arquivo de teste espelha o nome da classe que testa (`app/conta.py` ↔ `tests/test_conta.py`).

```
app/
├── conta.py
├── categoria.py
├── lancamento.py
├── fechamento.py
├── conciliacao.py
├── extrato.py
└── validadores.py
tests/
├── test_conta.py
├── test_categoria.py
├── test_lancamento.py
├── test_fechamento.py
├── test_conciliacao.py
└── test_extrato.py
```

---

## Passo 3 — Conta

A primeira classe do projeto, e a mais simples: representa uma conta com **nome** e **saldo**.

```python
class Conta:
    def __init__(self, nome: str, saldo: float) -> None:
        self.nome = nome
        self.saldo = saldo

    def adicionar_dinheiro(self, valor: float) -> None: ...
    def remover_dinheiro(self, valor: float) -> None: ...
    def visualizar_saldo(self) -> float: ...
```

Decisão de projeto

`Conta` não deixa qualquer parte do sistema alterar o saldo diretamente — quem quiser mexer nele precisa passar por `adicionar_dinheiro` ou `remover_dinheiro`, que validam o valor antes de aplicar a mudança. Isso é o mesmo princípio de **objeto rico**: a regra de negócio ("saldo nunca aceita valor inválido, débito nunca passa do saldo disponível") vive dentro da classe, não espalhada pelo sistema.

`remover_dinheiro` tem uma validação a mais que `adicionar_dinheiro`: além do valor ter que ser positivo, ele não pode ultrapassar o saldo disponível. Essa regra é exclusiva da `Conta` — nenhuma outra classe do projeto reaproveita essa parte.

---

## Passo 4 — Categoria

Toda categoria tem um **nome** e um **tipo** (`RECEITA` ou `DESPESA`, representado com `Enum` em vez de string solta, para evitar erros de digitação).

```python
class Tipo(Enum):
    RECEITA = 1
    DESPESA = 2

class Categoria:
    contador_generico = 1
    nomes_existentes = set()

    def __init__(self, nome_entrada: str, tipo: Tipo) -> None: ...
```

Decisão de projeto — nomes únicos e geração automática

Duas categorias com o mesmo nome não fazem sentido no domínio (não existem duas categorias "Salário"). Por isso, `Categoria` mantém um `set()` de todos os nomes já usados como **atributo de classe** — compartilhado entre todas as instâncias, e não recriado a cada objeto novo — e recusa qualquer nome duplicado.

Se nenhum nome for informado, a classe gera um automaticamente ("Item 1", "Item 2"...), usando outro atributo de classe (`contador_generico`) para saber onde parou. Essa foi a primeira vez, no projeto, em que a diferença entre **atributo de instância** (`self.algo`) e **atributo de classe** (`Categoria.algo`) fez diferença de verdade: se o contador e o conjunto de nomes fossem `self.`, cada categoria nova "esqueceria" o histórico das anteriores.

Como o estado é compartilhado entre instâncias, os testes usam uma fixture (`limpar_estado`) que reseta `nomes_existentes` e `contador_generico` antes de cada teste — sem isso, um teste "vazaria" estado para o próximo.

---

## Passo 5 — Validadores compartilhados

Durante a construção de `Conta` e `Lancamento`, percebi que a mesma regra — **"esse valor precisa ser positivo"** — se repetia em lugares diferentes. Em vez de duplicar o `if/raise` em cada classe, essa validação foi extraída para um módulo neutro:

```python
# app/validadores.py
def validar_valores_positivos(valor: float) -> None: ...
def validar_datas(data_inicio: date, data_fim: date) -> None: ...
```

Decisão de projeto — DRY (Don't Repeat Yourself)

`validar_valores_positivos` é usada por `Conta` (em `adicionar_dinheiro`/`remover_dinheiro`) e por `Lancamento` (na criação de cada lançamento). Já `validar_datas` — que garante que `data_fim` não vem antes de `data_inicio`, e que ambos os parâmetros são realmente objetos `date` — é reaproveitada por `Fechamento` e `Extrato`, que trabalham com períodos.

O que **não** foi para esse módulo: a regra de saldo suficiente da `Conta.remover_dinheiro`. Ela só faz sentido para quem tem saldo — não é uma regra genérica sobre números, é uma regra específica do domínio de `Conta`.

---

## Passo 6 — Lancamento

Um lançamento tem **descrição**, **valor**, **data** (sempre a de hoje, gerada automaticamente) e uma **categoria**.

```python
class Lancamento:
    contador_generico = 1

    def __init__(self, descricao_entrada: str, valor: float, categoria: Categoria) -> None: ...
```

Decisão de projeto — guardar o objeto Categoria, não só o nome

`Lancamento` guarda a **instância inteira** de `Categoria`, não apenas o nome dela. Isso importa porque o valor de todo lançamento é sempre positivo — quem decide se ele soma ou subtrai no total é o `tipo` da categoria (`RECEITA` ou `DESPESA`). Guardando só uma string, essa informação precisaria ser buscada em outro lugar toda vez; guardando o objeto, `lancamento.categoria.tipo` já resolve.

Decisão de projeto — descrição repetida é permitida

Diferente de `Categoria`, duas descrições iguais ("Uber", "Uber") fazem sentido — são lançamentos diferentes, em datas diferentes. Por isso, quando a descrição vem vazia, `Lancamento` só gera um texto sequencial ("Lançamento 1", "Lançamento 2"...) sem checar duplicidade contra nada, ao contrário do que `Categoria` faz com nomes.

---

## Passo 7 — Fechamento

`Fechamento` consolida os lançamentos de um período: recebe uma lista de `Lancamento` e um intervalo de datas, filtra o que está dentro do período e calcula receitas, despesas e saldo.

```python
class Fechamento:
    def __init__(self, lancamentos: list[Lancamento], data_inicio: date, data_fim: date) -> None: ...

    def obter_lancamentos_do_periodo(self) -> list[Lancamento]: ...
    def calcular_total_receitas(self) -> float: ...
    def calcular_total_despesas(self) -> float: ...
```

Decisão de projeto — saldo da Conta ≠ saldo do Fechamento

`Conta.saldo` é um estado vivo e cumulativo: "quanto existe agora". `Fechamento.saldo` é uma fotografia fixa de um recorte de tempo: "qual foi o resultado (receitas − despesas) só naquele período". Os dois têm o mesmo nome, mas representam conceitos diferentes — e é exatamente essa diferença que a classe `Conciliacao` existe para verificar.

Para simular lançamentos com datas diferentes nos testes (já que `Lancamento` sempre usa `date.today()`), os testes usam `freeze_time`, da biblioteca `freezegun`, para "congelar" a data do sistema durante a criação de cada lançamento.

---

## Passo 8 — Conciliacao

Verifica se o saldo de uma `Conta` bate com o saldo de um `Fechamento` de um período específico — por exemplo, se o saldo da conta ao fim de agosto bate com o fechamento de agosto.

```python
class Conciliacao:
    def __init__(self, conta: Conta, fechamento: Fechamento) -> None: ...
```

Decisão de projeto — tolerância de arredondamento

Como valores monetários aqui são `float`, uma comparação direta com `==` corre o risco de falhar por imprecisão de ponto flutuante, mesmo quando os valores "deveriam" ser iguais. Por isso, `Conciliacao` usa `math.isclose(..., abs_tol=0.01)` — uma tolerância de um centavo — em vez de comparação exata.

`Conciliacao` também segue o padrão adotado desde `Fechamento`: guarda apenas os números relevantes (`saldo_conta`, `saldo_fechamento`, `diferenca`, `conciliado`), não os objetos `Conta` e `Fechamento` inteiros.

---

## Passo 9 — Extrato

Resume os `Fechamento`s de um período — o mesmo tipo de agregação que `Fechamento` faz com `Lancamento`, um nível acima.

```python
class Extrato:
    def __init__(self, fechamentos: list[Fechamento], data_inicio: date, data_fim: date) -> None: ...

    def obter_fechamentos_do_periodo(self, fechamentos: list[Fechamento]) -> list[Fechamento]: ...
    def calcular_total_receitas(self, fechamentos_periodo: list[Fechamento]) -> float: ...
    def calcular_total_despesas(self, fechamentos_periodo: list[Fechamento]) -> float: ...
```

Decisão de projeto — filtrando um intervalo dentro de outro intervalo

Diferente de `Fechamento` (que compara **uma data** contra um intervalo), `Extrato` compara **um intervalo** (o período de cada `Fechamento`) contra outro intervalo (o período do próprio `Extrato`). Um fechamento só entra no extrato se estiver **totalmente contido** no período pedido — início e fim do fechamento dentro do início e fim do extrato.

Como cada `Fechamento` já calcula seus próprios totais na criação, `Extrato` não precisa reabrir os lançamentos individuais nem filtrar por categoria de novo — ele apenas **soma totais já prontos** (`fechamento.total_receitas`, `fechamento.total_despesas`) de cada fechamento que passou pelo filtro.

---

## Passo 10 — Rodando tudo

```
pytest -v
```

A opção `-v` (verbose) mostra o nome de cada teste individualmente — útil para acompanhar quais casos estão passando por classe.

---

## Resumo do que aprendi

| Conceito                            | Onde apliquei                                                   |
| ------------------------------------ | ----------------------------------------------------------------- |
| Classe simples                       | `Conta`                                                            |
| Objeto rico                          | `Conta`, `Lancamento` — validações vivem dentro da classe          |
| Atributo de classe vs. de instância  | `Categoria.nomes_existentes`, `contador_generico`                  |
| Reaproveitamento de regra (DRY)      | `validadores.py`, usado por `Conta`, `Lancamento`, `Fechamento`, `Extrato` |
| Associação                           | `Lancamento → Categoria`, `Fechamento → Lancamento`                |
| Agregação de coleção                 | `Fechamento` (soma `Lancamento`), `Extrato` (soma `Fechamento`)     |
| Delegação                            | `Extrato` soma totais já calculados por cada `Fechamento`          |
| Testes automatizados                 | `tests/test_*.py` com pytest, e `freezegun` para simular datas     |
| Invariante                           | Valor de lançamento sempre positivo, período sempre `fim ≥ início` |

---

## Próximos passos e melhorias possíveis

- Adicionar `freezegun` ao `requirements.txt`, já que os testes dependem dele.
- Revisar o método `valida_tipo_de_categoria` em `Categoria` — hoje ele existe mas não é chamado no `__init__`, então um `tipo` inválido (`None`, ou algo fora do `Enum`) ainda não é validado na prática.
- Considerar o uso de `Decimal` no lugar de `float` para valores monetários, evitando problemas de precisão em cálculos financeiros mais sensíveis.
- Avaliar se `Lancamento` deveria (ou não) se conectar diretamente a uma `Conta` — hoje as duas classes são independentes por design; a decisão foi mantê-las desacopladas até que `Fechamento`/`Conciliacao` deixassem claro se essa conexão automática seria necessária.
