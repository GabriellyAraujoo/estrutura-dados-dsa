"""Lista duplamente encadeada genérica.

Uma lista duplamente encadeada guarda cada elemento em um nó que conhece o
próximo e o anterior. Por isso dá para percorrer a lista nos dois sentidos
sem precisar de índices, como acontece em uma lista do Python (que é um array
encadeado por blocos de memória).

Complexidade das operações principais (n é o número de elementos):
    inserir_inicio / inserir_fim : O(1)
    remover(valor)               : O(n) para achar o valor + O(1) para religar
    buscar / contem              : O(n)
    inverter                     : O(n)
    __len__ / tamanho            : O(1)
"""

from typing import Generic, Iterator, List, Optional, TypeVar

T = TypeVar("T")


class _No(Generic[T]):
    """Nó interno da lista, com ponteiros para os vizinhos."""

    __slots__ = ("valor", "anterior", "proximo")

    def __init__(self, valor: T) -> None:
        self.valor = valor
        self.anterior: Optional["_No[T]"] = None
        self.proximo: Optional["_No[T]"] = None

    def __repr__(self) -> str:
        return "No({0!r})".format(self.valor)


class ListaDupla(Generic[T]):
    """Lista duplamente encadeada com sentinelas de cabeça e cauda.

    Os extremos da lista são mantidos em memória, então inserir e remover nas
    pontas custa tempo constante, ao contrário de uma lista do Python onde
    ``insert(0, valor)`` precisa deslocar todos os elementos.

    Complexidade (n é o número de elementos):
        inserir_inicio / inserir_fim : O(1)
        remover(valor)               : O(n)
        buscar(valor) / contem       : O(n)
        inverter()                   : O(n)
        len(lista) / lista.tamanho   : O(1)
    """

    __slots__ = ("_cabeca", "_cauda", "_tamanho")

    def __init__(self, valores: Optional[List[T]] = None) -> None:
        """Cria a lista, opcionalmente já preenchida com os valores recebidos."""
        self._cabeca: Optional[_No[T]] = None
        self._cauda: Optional[_No[T]] = None
        self._tamanho = 0
        if valores is not None:
            for valor in valores:
                self.inserir_fim(valor)

    def inserir_inicio(self, valor: T) -> "ListaDupla[T]":
        """Insere o valor na primeira posição.

        Complexidade: O(1). Devolve a própria lista para permitir encadeamento
        (``lista.inserir_inicio(1).inserir_inicio(2)``).
        """
        novo = _No(valor)
        novo.proximo = self._cabeca
        if self._cabeca is None:
            self._cauda = novo
        else:
            self._cabeca.anterior = novo
        self._cabeca = novo
        self._tamanho += 1
        return self

    def inserir_fim(self, valor: T) -> "ListaDupla[T]":
        """Insere o valor na última posição.

        Complexidade: O(1). Devolve a própria lista para permitir encadeamento.
        """
        novo = _No(valor)
        novo.anterior = self._cauda
        if self._cauda is None:
            self._cabeca = novo
        else:
            self._cauda.proximo = novo
        self._cauda = novo
        self._tamanho += 1
        return self

    def remover(self, valor: T) -> bool:
        """Remove a primeira ocorrência do valor.

        Complexidade: O(n) para localizar o valor e O(1) para religar os
        vizinhos. Devolve ``True`` se removeu e ``False`` se o valor não
        estava na lista.
        """
        no = self._no_com_valor(valor)
        if no is None:
            return False
        if no.anterior is None:
            self._cabeca = no.proximo
        else:
            no.anterior.proximo = no.proximo
        if no.proximo is None:
            self._cauda = no.anterior
        else:
            no.proximo.anterior = no.anterior
        no.anterior = None
        no.proximo = None
        self._tamanho -= 1
        return True

    def buscar(self, valor: T) -> Optional[T]:
        """Devolve o valor procurado ou ``None`` se ele não existir.

        Complexidade: O(n).
        """
        no = self._no_com_valor(valor)
        if no is None:
            return None
        return no.valor

    def contem(self, valor: T) -> bool:
        """Informa se o valor está na lista.

        Complexidade: O(n).
        """
        return self._no_com_valor(valor) is not None

    @property
    def tamanho(self) -> int:
        """Quantidade de elementos da lista.

        Complexidade: O(1).
        """
        return self._tamanho

    def __len__(self) -> int:
        """Permite usar ``len(lista)``.

        Complexidade: O(1).
        """
        return self._tamanho

    def __iter__(self) -> Iterator[T]:
        """Percorre a lista do primeiro ao último elemento.

        Complexidade: O(n) para percorrer tudo.
        """
        no = self._cabeca
        while no is not None:
            yield no.valor
            no = no.proximo

    def __str__(self) -> str:
        """Representação legível, por exemplo ``1 -> 2 -> 3``."""
        return " -> ".join(str(valor) for valor in self)

    def __repr__(self) -> str:
        """Representação usada pelo interpretador e pelos testes."""
        return "ListaDupla({0!r})".format(list(self))

    def __eq__(self, outro: object) -> bool:
        """Compara duas listas pelo conteúdo, na mesma ordem.

        Duas listas com os mesmos elementos em ordens diferentes não são
        iguais, porque a posição de cada elemento faz parte do conteúdo.
        """
        if not isinstance(outro, ListaDupla):
            return NotImplemented
        if len(self) != len(outro):
            return False
        return list(self) == list(outro)

    def inverter(self) -> "ListaDupla[T]":
        """Devolve uma nova lista com os elementos na ordem inversa.

        A lista original não é alterada. Complexidade: O(n).
        """
        invertida: "ListaDupla[T]" = ListaDupla()
        for valor in self:
            invertida.inserir_inicio(valor)
        return invertida

    def _no_com_valor(self, valor: T) -> Optional[_No[T]]:
        """Procura o primeiro nó que guarda o valor. Complexidade: O(n)."""
        no = self._cabeca
        while no is not None:
            if no.valor == valor:
                return no
            no = no.proximo
        return None
