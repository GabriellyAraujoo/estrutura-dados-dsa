"""Árvore binária de busca (BST).

Cada nó guarda um valor e, no máximo, dois filhos. Na subárvore esquerda ficam
os valores menores que o do nó e na direita os maiores. Essa regra é o que
permite buscar, inserir e remover em tempo logarítmico quando a árvore está
balanceada.

Complexidade das operações principais (h é a altura da árvore, n o número
de nós):
    inserir / buscar / remover : O(h), O(log n) em árvore balanceada
    emprumar                   : O(n)
    altura / contar            : O(n)
    minimo / maximo            : O(h)
    esta_balanceada            : O(n)
"""

from typing import Generic, List, Optional, Tuple, TypeVar

T = TypeVar("T")


class No(Generic[T]):
    """Nó de uma árvore binária de busca.

    Guarda o valor e os dois filhos. Um filho ausente é representado por
    ``None``.
    """

    __slots__ = ("valor", "esquerda", "direita")

    def __init__(self, valor: T) -> None:
        self.valor = valor
        self.esquerda: Optional["No[T]"] = None
        self.direita: Optional["No[T]"] = None

    def __repr__(self) -> str:
        return "No({0!r})".format(self.valor)


class ArvoreBinaria(Generic[T]):
    """Árvore binária de busca.

    Os valores precisam ser comparáveis entre si (``<`` e ``>``), porque é
    essa comparação que define o lugar de cada valor na árvore.

    Complexidade (h é a altura, n o número de nós):
        inserir / buscar / remover : O(h), O(log n) em árvore balanceada
        emprumar                   : O(n)
        altura / contar            : O(n)
        minimo / maximo            : O(h)
        esta_balanceada            : O(n)
    """

    __slots__ = ("raiz",)

    def __init__(self) -> None:
        """Cria a árvore vazia."""
        self.raiz: Optional[No[T]] = None

    def inserir(self, valor: T) -> bool:
        """Insere o valor na árvore, ignorando duplicados.

        Complexidade: O(h), onde h é a altura da árvore. Devolve ``True``
        quando o valor entrou e ``False`` quando já existia.
        """
        if self.raiz is None:
            self.raiz = No(valor)
            return True
        no = self.raiz
        while True:
            if valor == no.valor:
                return False
            if valor < no.valor:
                if no.esquerda is None:
                    no.esquerda = No(valor)
                    return True
                no = no.esquerda
            else:
                if no.direita is None:
                    no.direita = No(valor)
                    return True
                no = no.direita

    def buscar(self, valor: T) -> bool:
        """Informa se o valor está na árvore.

        Complexidade: O(h), onde h é a altura da árvore.
        """
        no = self.raiz
        while no is not None:
            if valor == no.valor:
                return True
            if valor < no.valor:
                no = no.esquerda
            else:
                no = no.direita
        return False

    def remover(self, valor: T) -> bool:
        """Remove o valor da árvore.

        Complexidade: O(h), onde h é a altura da árvore. Devolve ``True``
        quando removeu e ``False`` quando o valor não existia.

        Há três casos: nó sem filhos (basta desligá-lo da árvore), nó com um
        único filho (o filho ocupa o lugar do pai) e nó com dois filhos (o
        valor do sucessor em ordem, o menor da subárvore direita, é copiado
        para o nó e o sucessor é removido da direita).
        """
        if self.raiz is None:
            return False
        raiz, removido = self._remover(self.raiz, valor)
        self.raiz = raiz
        return removido

    def emprumar(self) -> List[T]:
        """Percorre a árvore em ordem e devolve os valores em ordem crescente.

        Complexidade: O(n), com n o número de nós.
        """
        valores: List[T] = []
        self._emprumar(self.raiz, valores)
        return valores

    def altura(self) -> int:
        """Altura da árvore em número de níveis.

        Uma árvore vazia tem altura 0 e uma árvore com um único nó tem
        altura 1. Complexidade: O(n).
        """
        return self._altura(self.raiz)

    def contar(self) -> int:
        """Quantidade de nós da árvore.

        Complexidade: O(n).
        """
        return self._contar(self.raiz)

    def minimo(self) -> Optional[T]:
        """Menor valor da árvore ou ``None`` se ela estiver vazia.

        Complexidade: O(h), onde h é a altura da árvore.
        """
        if self.raiz is None:
            return None
        no = self.raiz
        while no.esquerda is not None:
            no = no.esquerda
        return no.valor

    def maximo(self) -> Optional[T]:
        """Maior valor da árvore ou ``None`` se ela estiver vazia.

        Complexidade: O(h), onde h é a altura da árvore.
        """
        if self.raiz is None:
            return None
        no = self.raiz
        while no.direita is not None:
            no = no.direita
        return no.valor

    def esta_balanceada(self) -> bool:
        """Informa se todos os nós estão balanceados.

        Um nó está balanceado quando a altura das duas subárvores filhas
        difere em no máximo 1. Complexidade: O(n).
        """
        return self._altura_balanceada(self.raiz) != -1

    @staticmethod
    def _remover(no: Optional[No[T]], valor: T) -> Tuple[Optional[No[T]], bool]:
        """Remove o valor da subárvore e devolve a nova raiz e se removeu."""
        if no is None:
            return None, False
        if valor < no.valor:
            no.esquerda, removido = ArvoreBinaria._remover(no.esquerda, valor)
            return no, removido
        if valor > no.valor:
            no.direita, removido = ArvoreBinaria._remover(no.direita, valor)
            return no, removido
        if no.esquerda is None:
            return no.direita, True
        if no.direita is None:
            return no.esquerda, True
        sucessor = no.direita
        while sucessor.esquerda is not None:
            sucessor = sucessor.esquerda
        no.valor = sucessor.valor
        no.direita, _ = ArvoreBinaria._remover(no.direita, sucessor.valor)
        return no, True

    @staticmethod
    def _emprumar(no: Optional[No[T]], valores: List[T]) -> None:
        """Percorre em ordem (esquerda, nó, direita) recolhendo os valores."""
        if no is None:
            return
        ArvoreBinaria._emprumar(no.esquerda, valores)
        valores.append(no.valor)
        ArvoreBinaria._emprumar(no.direita, valores)

    @staticmethod
    def _altura(no: Optional[No[T]]) -> int:
        """Altura da subárvore em número de níveis."""
        if no is None:
            return 0
        altura_esquerda = ArvoreBinaria._altura(no.esquerda)
        altura_direita = ArvoreBinaria._altura(no.direita)
        return 1 + max(altura_esquerda, altura_direita)

    @staticmethod
    def _contar(no: Optional[No[T]]) -> int:
        """Conta os nós da subárvore."""
        if no is None:
            return 0
        return 1 + ArvoreBinaria._contar(no.esquerda) + ArvoreBinaria._contar(no.direita)

    @staticmethod
    def _altura_balanceada(no: Optional[No[T]]) -> int:
        """Devolve a altura da subárvore ou -1 se ela não estiver balanceada."""
        if no is None:
            return 0
        altura_esquerda = ArvoreBinaria._altura_balanceada(no.esquerda)
        if altura_esquerda == -1:
            return -1
        altura_direita = ArvoreBinaria._altura_balanceada(no.direita)
        if altura_direita == -1:
            return -1
        if abs(altura_esquerda - altura_direita) > 1:
            return -1
        return 1 + max(altura_esquerda, altura_direita)
