"""Algoritmos de busca em listas.

Todas as funções devolvem o índice do elemento procurado ou -1 quando o
elemento não existe. As buscas binária, ternária e por salto exigem uma lista
já ordenada; a busca linear funciona com qualquer lista.

Complexidade (n é o número de elementos):
    busca_linear             : O(n)
    busca_binaria            : O(log n)
    busca_ternaria           : O(log3 n)
    busca_por_salto          : O(sqrt(n))
    busca_em_lista_ordenada  : O(log n) para listas grandes, O(n) para listas
                               pequenas (o limite está em LIMIAR_BUSCA_LINEAR)
"""

from math import isqrt
from typing import List

LIMIAR_BUSCA_LINEAR = 32


def busca_linear(lista: List[int], alvo: int) -> int:
    """Procura o alvo percorrendo a lista do começo ao fim.

    Funciona com listas ordenadas ou não, e é a melhor opção para listas
    pequenas, porque não precisa calcular o meio nem comparar tantas vezes.

    Complexidade: O(n), com n o número de elementos.
    """
    for indice, valor in enumerate(lista):
        if valor == alvo:
            return indice
    return -1


def busca_binaria(lista: List[int], alvo: int) -> int:
    """Procura o alvo dividindo a lista ao meio a cada passo.

    A lista precisa estar ordenada. A cada comparação o espaço de busca cai
    pela metade, o que dá uma das buscas mais rápidas que existem.

    Devolve o índice de uma ocorrência do alvo ou -1. Complexidade:
    O(log n), com n o número de elementos.
    """
    inicio = 0
    fim = len(lista) - 1
    while inicio <= fim:
        meio = (inicio + fim) // 2
        if lista[meio] == alvo:
            return meio
        if lista[meio] < alvo:
            inicio = meio + 1
        else:
            fim = meio - 1
    return -1


def busca_ternaria(lista: List[int], alvo: int) -> int:
    """Procura o alvo dividindo a lista em três partes a cada passo.

    A lista precisa estar ordenada. Dois terços da lista são eliminados a
    cada comparação, o que dá um pouco mais de velocidade que a busca
    binária, a um custo maior de controle de fluxo.

    Devolve o índice de uma ocorrência do alvo ou -1. Complexidade:
    O(log3 n), com n o número de elementos.
    """
    inicio = 0
    fim = len(lista) - 1
    while inicio <= fim:
        terco = (fim - inicio) // 3
        primeiro = inicio + terco
        segundo = fim - terco
        if lista[primeiro] == alvo:
            return primeiro
        if lista[segundo] == alvo:
            return segundo
        if alvo < lista[primeiro]:
            fim = primeiro - 1
        elif alvo > lista[segundo]:
            inicio = segundo + 1
        else:
            inicio = primeiro + 1
            fim = segundo - 1
    return -1


def busca_por_salto(lista: List[int], alvo: int) -> int:
    """Procura o alvo saltando de blocos em blocos (busca por salto).

    A lista precisa estar ordenada. Em vez de ir de meio em meio, a busca
    pula sqrt(n) posições de cada vez até encontrar um bloco que possa conter
    o alvo e, dentro desse bloco, faz uma busca linear.

    Devolve o índice de uma ocorrência do alvo ou -1. Complexidade:
    O(sqrt(n)), com n o número de elementos.
    """
    total = len(lista)
    if total == 0:
        return -1
    salto = max(1, isqrt(total))
    anterior = 0
    while anterior < total and lista[min(anterior, total - 1)] < alvo:
        anterior += salto
    inicio = max(0, anterior - salto)
    for indice in range(inicio, min(total, anterior + salto)):
        if lista[indice] == alvo:
            return indice
    return -1


def busca_em_lista_ordenada(lista: List[int], alvo: int) -> int:
    """Escolhe automaticamente entre a busca binária e a busca linear.

    Para listas pequenas a linear vence: a busca binária precisa calcular o
    meio, controlar o laço e voltar atrás, e esse custo extra não compensa
    com poucos elementos. A partir do limite de 32 elementos a binária passa
    a ser mais rápida porque corta a lista pela metade a cada passo.

    A lista precisa estar ordenada. Devolve o índice de uma ocorrência do
    alvo ou -1. Complexidade: O(log n) para listas grandes e O(n) para listas
    pequenas, com n o número de elementos.
    """
    if len(lista) < LIMIAR_BUSCA_LINEAR:
        return busca_linear(lista, alvo)
    return busca_binaria(lista, alvo)
