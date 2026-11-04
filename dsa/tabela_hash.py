"""Tabela hash com encadeamento (separate chaining).

Cada posição da tabela (o balde) guarda uma lista de pares (chave, valor).
Quando duas chaves caem no mesmo balde, elas convivem na mesma lista, e é por
isso que a estrutura se chama encadeamento.

A tabela cresce sozinha: quando a quantidade de itens passa de 75% da
capacidade, a capacidade dobra e todos os itens são redistribuídos. Isso
mantém as listas de balde curtas e o custo de busca perto de O(1).

Complexidade das operações principais (n é o número de itens e c a
capacidade):
    inserir       : O(1) amortizado
    buscar        : O(1) em média, O(n) no pior caso
    remover       : O(1) em média
    contem        : O(1) em média
    redimensionar : O(n)
    tamanho       : O(1)
"""

from typing import Dict, Generic, List, Optional, Tuple, TypeVar

K = TypeVar("K")
V = TypeVar("V")

LIMIAR_CARGA = 0.75


class TabelaHash(Generic[K, V]):
    """Tabela hash com encadeamento por balde.

    Complexidade (n é o número de itens e c a capacidade):
        inserir       : O(1) amortizado
        buscar        : O(1) em média, O(n) no pior caso
        remover       : O(1) em média
        contem        : O(1) em média
        redimensionar : O(n)
        tamanho       : O(1)
    """

    __slots__ = ("_capacidade", "_baldes", "_tamanho")

    def __init__(self, capacidade_inicial: int = 8) -> None:
        """Cria a tabela com a capacidade inicial informada.

        Levanta ``ValueError`` se a capacidade inicial for menor que 1.
        """
        if capacidade_inicial < 1:
            raise ValueError("A capacidade inicial deve ser no mínimo 1.")
        self._capacidade = capacidade_inicial
        self._baldes: Dict[int, List[Tuple[K, V]]] = {}
        self._tamanho = 0

    def inserir(self, chave: K, valor: V) -> None:
        """Insere ou atualiza o valor da chave.

        Se a chave já existir, o valor é substituído e o tamanho da tabela
        não muda. Complexidade: O(1) amortizado.
        """
        if (self._tamanho + 1) / self._capacidade > LIMIAR_CARGA:
            self.redimensionar()
        indice = self._indice(chave)
        balde = self._baldes.setdefault(indice, [])
        for posicao, par in enumerate(balde):
            if par[0] == chave:
                balde[posicao] = (chave, valor)
                return
        balde.append((chave, valor))
        self._tamanho += 1

    def buscar(self, chave: K) -> Optional[V]:
        """Devolve o valor da chave ou ``None`` se ela não existir.

        Complexidade: O(1) em média, O(n) no pior caso.
        """
        for chave_guardada, valor in self._baldes.get(self._indice(chave), []):
            if chave_guardada == chave:
                return valor
        return None

    def remover(self, chave: K) -> bool:
        """Remove a chave da tabela.

        Complexidade: O(1) em média. Devolve ``True`` se removeu e ``False``
        se a chave não existia.
        """
        indice = self._indice(chave)
        balde = self._baldes.get(indice)
        if not balde:
            return False
        for posicao, par in enumerate(balde):
            if par[0] == chave:
                del balde[posicao]
                self._tamanho -= 1
                if not balde:
                    del self._baldes[indice]
                return True
        return False

    def contem(self, chave: K) -> bool:
        """Informa se a chave está na tabela.

        Complexidade: O(1) em média.
        """
        for chave_guardada, _ in self._baldes.get(self._indice(chave), []):
            if chave_guardada == chave:
                return True
        return False

    @property
    def tamanho(self) -> int:
        """Quantidade de pares (chave, valor) guardados na tabela.

        Complexidade: O(1).
        """
        return self._tamanho

    @property
    def capacidade(self) -> int:
        """Quantidade de baldes da tabela.

        Complexidade: O(1).
        """
        return self._capacidade

    def redimensionar(self, nova_capacidade: Optional[int] = None) -> None:
        """Muda a capacidade da tabela e redistribui todos os itens.

        Sem argumento, a capacidade dobra. Com argumento, usa a capacidade
        informada (precisa ser no mínimo 1). Complexidade: O(n).
        """
        if nova_capacidade is None:
            nova_capacidade = self._capacidade * 2
        if nova_capacidade < 1:
            raise ValueError("A capacidade deve ser no mínimo 1.")
        itens = [
            (chave, valor)
            for balde in self._baldes.values()
            for chave, valor in balde
        ]
        self._capacidade = nova_capacidade
        self._baldes = {}
        for chave, valor in itens:
            indice = self._indice(chave)
            self._baldes.setdefault(indice, []).append((chave, valor))

    def __len__(self) -> int:
        """Permite usar ``len(tabela)``.

        Complexidade: O(1).
        """
        return self._tamanho

    def _indice(self, chave: K) -> int:
        """Índice do balde onde a chave fica guardada."""
        return hash(chave) % self._capacidade
