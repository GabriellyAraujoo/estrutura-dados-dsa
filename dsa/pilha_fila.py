"""Pilha (LIFO) e Fila (FIFO) implementadas do zero.

Pilha: o último elemento que entrou é o primeiro que sai (LIFO).
Fila: o primeiro elemento que entrou é o primeiro que sai (FIFO).

A pilha usa uma lista do Python, cujo ``append`` e ``pop`` rodam em tempo
constante amortizado. A fila usa uma lista com um índice de início: elementos
são acrescentados no fim e consumidos pela frente, e o trecho já consumido é
descartado de tempos em tempos para a lista não crescer sem limite.

Complexidade das operações principais (n é o número de elementos):
    empilhar / enfileirar      : O(1) amortizado
    desempilhar / desenfileirar : O(1) amortizado
    topo / frente              : O(1)
    vazia / tamanho / len       : O(1)
"""

from typing import Generic, List, Optional, TypeVar

T = TypeVar("T")


class Pilha(Generic[T]):
    """Pilha (LIFO): insere e remove sempre na mesma ponta.

    Complexidade (n é o número de elementos):
        empilhar       : O(1) amortizado
        desempilhar    : O(1) amortizado
        topo           : O(1)
        vazia          : O(1)
        tamanho / len  : O(1)
    """

    __slots__ = ("_itens",)

    def __init__(self, itens: Optional[List[T]] = None) -> None:
        """Cria a pilha, opcionalmente já preenchida com os valores recebidos."""
        self._itens: List[T] = list(itens) if itens is not None else []

    def empilhar(self, valor: T) -> None:
        """Coloca o valor no topo da pilha.

        Complexidade: O(1) amortizado.
        """
        self._itens.append(valor)

    def desempilhar(self) -> T:
        """Remove e devolve o elemento do topo.

        Complexidade: O(1) amortizado. Levanta ``IndexError`` se a pilha
        estiver vazia.
        """
        if not self._itens:
            raise IndexError("A pilha está vazia: não há nada para desempilhar.")
        return self._itens.pop()

    def topo(self) -> T:
        """Devolve o elemento do topo sem removê-lo.

        Complexidade: O(1). Levanta ``IndexError`` se a pilha estiver vazia.
        """
        if not self._itens:
            raise IndexError("A pilha está vazia: não há elemento no topo.")
        return self._itens[-1]

    @property
    def vazia(self) -> bool:
        """Informa se a pilha não tem nenhum elemento.

        Complexidade: O(1).
        """
        return not self._itens

    @property
    def tamanho(self) -> int:
        """Quantidade de elementos na pilha.

        Complexidade: O(1).
        """
        return len(self._itens)

    def __len__(self) -> int:
        """Permite usar ``len(pilha)``.

        Complexidade: O(1).
        """
        return len(self._itens)


class Fila(Generic[T]):
    """Fila (FIFO): insere no fim e remove pela frente.

    Complexidade (n é o número de elementos):
        enfileirar      : O(1) amortizado
        desenfileirar   : O(1) amortizado
        frente          : O(1)
        vazia           : O(1)
        tamanho / len   : O(1)
    """

    __slots__ = ("_itens", "_inicio")

    def __init__(self, itens: Optional[List[T]] = None) -> None:
        """Cria a fila, opcionalmente já preenchida com os valores recebidos."""
        self._itens: List[T] = list(itens) if itens is not None else []
        self._inicio = 0

    def enfileirar(self, valor: T) -> None:
        """Coloca o valor no fim da fila.

        Complexidade: O(1) amortizado.
        """
        self._itens.append(valor)

    def desenfileirar(self) -> T:
        """Remove e devolve o elemento que está na frente da fila.

        Complexidade: O(1) amortizado. Levanta ``IndexError`` se a fila
        estiver vazia.
        """
        if self._inicio >= len(self._itens):
            raise IndexError("A fila está vazia: não há nada para desenfileirar.")
        valor = self._itens[self._inicio]
        self._inicio += 1
        self._descartar_consumidos()
        return valor

    def frente(self) -> T:
        """Devolve o elemento da frente da fila sem removê-lo.

        Complexidade: O(1). Levanta ``IndexError`` se a fila estiver vazia.
        """
        if self._inicio >= len(self._itens):
            raise IndexError("A fila está vazia: não há elemento na frente.")
        return self._itens[self._inicio]

    @property
    def vazia(self) -> bool:
        """Informa se a fila não tem nenhum elemento.

        Complexidade: O(1).
        """
        return self._inicio >= len(self._itens)

    @property
    def tamanho(self) -> int:
        """Quantidade de elementos na fila.

        Complexidade: O(1).
        """
        return len(self._itens) - self._inicio

    def __len__(self) -> int:
        """Permite usar ``len(fila)``.

        Complexidade: O(1).
        """
        return len(self._itens) - self._inicio

    def _descartar_consumidos(self) -> None:
        """Solta o trecho já consumido da lista interna.

        Só acontece quando o trecho consumido passa de metade da lista, o que
        mantém o custo amortizado em O(1) por operação.
        """
        if self._inicio > len(self._itens) // 2:
            self._itens = self._itens[self._inicio:]
            self._inicio = 0
