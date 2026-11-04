"""Estruturas de dados e algoritmos implementados do zero.

O pacote ``dsa`` reúne as estruturas clássicas que aparecem em entrevistas
técnicas e em provas de estruturas de dados e algoritmos:

    - ``ListaDupla``    : lista duplamente encadeada genérica
    - ``Pilha`` / ``Fila`` : pilha (LIFO) e fila (FIFO)
    - ``ArvoreBinaria`` : árvore binária de busca
    - ``TabelaHash``    : tabela hash com encadeamento
    - ordenação         : inserção, seleção, bolha, fusão, rápida e balde
    - ``Grafo``         : lista de adjacência, BFS, DFS, Kruskal
    - buscas            : linear, binária, ternária e por salto

Exemplo:

    >>> from dsa import ListaDupla, ordenacao_rapida
    >>> lista = ListaDupla([3, 1, 2])
    >>> lista.inserir_fim(4)
    ListaDupla([3, 1, 2, 4])
    >>> ordenacao_rapida(list(lista))
    [1, 2, 3, 4]
"""

from .arvore_binaria import ArvoreBinaria, No
from .busca import (
    busca_binaria,
    busca_em_lista_ordenada,
    busca_linear,
    busca_por_salto,
    busca_ternaria,
)
from .grafos import Grafo
from .linked_list import ListaDupla
from .ordenacao import (
    ordenacao_por_bolha,
    ordenacao_por_balde,
    ordenacao_por_fusao,
    ordenacao_por_insercao,
    ordenacao_por_selecao,
    ordenacao_rapida,
)
from .pilha_fila import Fila, Pilha
from .tabela_hash import TabelaHash

__all__ = [
    "ArvoreBinaria",
    "Fila",
    "Grafo",
    "ListaDupla",
    "No",
    "Pilha",
    "TabelaHash",
    "busca_binaria",
    "busca_em_lista_ordenada",
    "busca_linear",
    "busca_por_salto",
    "busca_ternaria",
    "ordenacao_por_bolha",
    "ordenacao_por_balde",
    "ordenacao_por_fusao",
    "ordenacao_por_insercao",
    "ordenacao_por_selecao",
    "ordenacao_rapida",
]
