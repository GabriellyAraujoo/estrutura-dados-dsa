"""Grafo com lista de adjacência e algoritmos de travessia.

O grafo é não direcionado por padrão: uma aresta entre ``a`` e ``b`` vale nos
dois sentidos. Uma aresta direcionada pode ser criada passando
``direcionada=True``, e é ela que dá sentido a uma ordem topológica.

Os vértices são strings.

Complexidade das operações principais (v é o número de vértices e e o número
de arestas):
    adicionar_vertice          : O(1)
    adicionar_aresta            : O(1)
    vizinhos                    : O(1) para devolver a cópia da lista
    existe_aresta               : O(1)
    caminho_bfs                 : O(v + e)
    caminho_dfs                 : O(v + e)
    componentes_conexas         : O(v + e)
    ordem_topologica            : O(v + e)
    arvore_geradora_minima      : O(e log e), o e log v do union-find
"""

from typing import Dict, List, Optional, Set, Tuple


class Grafo:
    """Grafo não direcionado por padrão, com lista de adjacência.

    Complexidade (v é o número de vértices e e o de arestas):
        adicionar_vertice     : O(1)
        adicionar_aresta       : O(1)
        vizinhos               : O(1)
        existe_aresta          : O(1)
        caminho_bfs / dfs      : O(v + e)
        componentes_conexas    : O(v + e)
        ordem_topologica       : O(v + e)
        arvore_geradora_minima : O(e log e)
    """

    def __init__(self) -> None:
        """Cria o grafo vazio."""
        self._adjacencia: Dict[str, List[str]] = {}
        self._arestas: List[Tuple[str, str, bool, float]] = []

    def adicionar_vertice(self, vertice: str) -> None:
        """Adiciona um vértice ao grafo, se ele ainda não existir.

        Complexidade: O(1).
        """
        self._validar_vertice(vertice)
        if vertice not in self._adjacencia:
            self._adjacencia[vertice] = []

    def adicionar_aresta(
        self,
        origem: str,
        destino: str,
        peso: float = 1.0,
        direcionada: bool = False,
    ) -> None:
        """Cria uma aresta entre dois vértices.

        A aresta é não direcionada por padrão, valendo nos dois sentidos. Com
        ``direcionada=True`` a aresta vale só de ``origem`` para ``destino``.

        Os vértices são criados automaticamente se ainda não existirem. Uma
        aresta repetida é ignorada, para não duplicar vizinhança.

        Complexidade: O(1).
        """
        self._validar_vertice(origem)
        self._validar_vertice(destino)
        if origem == destino:
            raise ValueError(
                "Não é possível criar uma aresta de um vértice para ele mesmo."
            )
        if direcionada:
            ja_existe = destino in self._adjacencia.get(origem, [])
        else:
            ja_existe = (
                destino in self._adjacencia.get(origem, [])
                or origem in self._adjacencia.get(destino, [])
            )
        if ja_existe:
            return
        self.adicionar_vertice(origem)
        self.adicionar_vertice(destino)
        self._adjacencia[origem].append(destino)
        if not direcionada:
            self._adjacencia[destino].append(origem)
        self._arestas.append((origem, destino, direcionada, peso))

    def vizinhos(self, vertice: str) -> List[str]:
        """Devolve a cópia da lista de vizinhos do vértice.

        Complexidade: O(1) para montar a cópia, O(g) no tamanho da
        vizinhança.
        """
        if vertice not in self._adjacencia:
            raise KeyError("O vértice {0!r} não existe no grafo.".format(vertice))
        return list(self._adjacencia[vertice])

    def existe_aresta(self, origem: str, destino: str) -> bool:
        """Informa se existe aresta entre os dois vértices.

        Em arestas não direcionadas o resultado é o mesmo nos dois sentidos.
        Complexidade: O(1).
        """
        return destino in self._adjacencia.get(origem, [])

    def caminho_bfs(self, origem: str, destino: str) -> Optional[List[str]]:
        """Procura o caminho mais curto entre dois vértices com busca em largura.

        A busca em largura (BFS) visita os vértices por nível, então o
        primeiro caminho que chega ao destino é o mais curto em número de
        arestas.

        Devolve a lista de vértices do caminho, da origem ao destino, ou
        ``None`` quando não existe caminho. Complexidade: O(v + e).
        """
        if origem not in self._adjacencia or destino not in self._adjacencia:
            return None
        if origem == destino:
            return [origem]
        visitados = {origem}
        pais: Dict[str, Optional[str]] = {origem: None}
        fila: List[str] = [origem]
        cabeca = 0
        while cabeca < len(fila):
            atual = fila[cabeca]
            cabeca += 1
            for vizinho in self._adjacencia[atual]:
                if vizinho in visitados:
                    continue
                visitados.add(vizinho)
                pais[vizinho] = atual
                if vizinho == destino:
                    return _montar_caminho(pais, origem, destino)
                fila.append(vizinho)
        return None

    def caminho_dfs(self, origem: str, destino: str) -> Optional[List[str]]:
        """Procura um caminho entre dois vértices com busca em profundidade.

        A busca em profundidade (DFS) desce por um ramo até o fim antes de
        testar o próximo. O caminho devolvido é válido, mas não é garantido
        que seja o mais curto.

        Devolve a lista de vértices do caminho ou ``None`` quando não existe
        caminho. Complexidade: O(v + e).
        """
        if origem not in self._adjacencia or destino not in self._adjacencia:
            return None
        if origem == destino:
            return [origem]
        visitados = {origem}
        pais: Dict[str, Optional[str]] = {origem: None}
        pilha: List[str] = [origem]
        while pilha:
            atual = pilha.pop()
            for vizinho in reversed(self._adjacencia[atual]):
                if vizinho in visitados:
                    continue
                visitados.add(vizinho)
                pais[vizinho] = atual
                if vizinho == destino:
                    return _montar_caminho(pais, origem, destino)
                pilha.append(vizinho)
        return None

    def componentes_conexas(self) -> List[List[str]]:
        """Devolve as componentes conexas do grafo.

        Os vértices de cada componente vêm em ordem alfabética e as
        componentes também, para que o resultado seja sempre o mesmo.

        Complexidade: O(v + e).
        """
        adjacencia_fraca: Dict[str, Set[str]] = {
            vertice: set() for vertice in self._adjacencia
        }
        for origem, destino, _, _ in self._arestas:
            adjacencia_fraca[origem].add(destino)
            adjacencia_fraca[destino].add(origem)
        componentes: List[List[str]] = []
        visitados: Set[str] = set()
        for vertice in sorted(self._adjacencia):
            if vertice in visitados:
                continue
            componente: Set[str] = set()
            fila: List[str] = [vertice]
            cabeca = 0
            while cabeca < len(fila):
                atual = fila[cabeca]
                cabeca += 1
                if atual in componente:
                    continue
                componente.add(atual)
                fila.extend(adjacencia_fraca[atual] - componente)
            visitados |= componente
            componentes.append(sorted(componente))
        return componentes

    def ordem_topologica(self) -> List[str]:
        """Devolve uma ordem topológica dos vértices.

        Cada aresta é lida como uma restrição de ordem: a origem vem antes
        do destino. Como uma aresta não direcionada vale nos dois sentidos,
        ela forma um ciclo e um grafo com arestas não direcionadas nunca
        admite ordem topológica. Para obter uma, crie as aristas com
        ``direcionada=True``.

        Levanta ``ValueError`` quando o grafo tem ciclo. Complexidade:
        O(v + e).
        """
        grau_entrada: Dict[str, int] = {vertice: 0 for vertice in self._adjacencia}
        for origem, destino, direcionada, _ in self._arestas:
            grau_entrada[destino] += 1
            if not direcionada:
                grau_entrada[origem] += 1
        prontos: List[str] = sorted(
            vertice for vertice, grau in grau_entrada.items() if grau == 0
        )
        ordem: List[str] = []
        cabeca = 0
        while cabeca < len(prontos):
            atual = prontos[cabeca]
            cabeca += 1
            ordem.append(atual)
            for vizinho in self._adjacencia[atual]:
                grau_entrada[vizinho] -= 1
                if grau_entrada[vizinho] == 0:
                    prontos.append(vizinho)
        if len(ordem) != len(self._adjacencia):
            raise ValueError(
                "O grafo contém um ciclo e portanto não admite ordem topológica. "
                "Use arestas direcionadas para grafos acíclicos."
            )
        return ordem

    def arvore_geradora_minima(self) -> List[Tuple[str, str, float]]:
        """Calcula a árvore geradora mínima com o algoritmo de Kruskal.

        As arestas não direcionadas são ordenadas pelo peso e entram na
        árvore uma a uma, enquanto o union-find garante que não seja criado
        ciclo. Devolve a lista de arestas escolhidas, no formato
        ``(origem, destino, peso)``.

        Se o grafo não for conexo, o resultado é uma floresta geradora com uma
        árvore mínima por componente. Complexidade: O(e log e).
        """
        arestas_ordenadas = sorted(
            (
                (peso, posicao, origem, destino)
                for posicao, (origem, destino, direcionada, peso) in enumerate(self._arestas)
                if not direcionada
            ),
            key=lambda aresta: (aresta[0], aresta[1]),
        )
        conjuntos = _EstruturaUnionFind(self._adjacencia)
        escolhida: List[Tuple[str, str, float]] = []
        for peso, _, origem, destino in arestas_ordenadas:
            if conjuntos.unir(origem, destino):
                escolhida.append((origem, destino, peso))
        return escolhida

    @staticmethod
    def _validar_vertice(vertice: str) -> None:
        """Garante que o vértice é uma string. Complexidade: O(1)."""
        if not isinstance(vertice, str):
            raise TypeError(
                "Os vértices do grafo devem ser strings, mas recebeu "
                "{0!r}.".format(vertice)
            )


class _EstruturaUnionFind:
    """Estrutura union-find com compressão de caminho e união por tamanho.

    Serve para saber se dois vértices já estão no mesmo conjunto e para
    juntá-los, que é exatamente o que o algoritmo de Kruskal precisa.

    Complexidade: O(1) amortizado por operação, com o caminho comprimido.
    """

    def __init__(self, elementos) -> None:
        """Cria um conjunto para cada elemento informado."""
        self._pai: Dict[str, str] = {}
        self._tamanho: Dict[str, int] = {}
        for elemento in elementos:
            self._pai[elemento] = elemento
            self._tamanho[elemento] = 1

    def encontrar(self, elemento: str) -> str:
        """Devolve o representante do conjunto do elemento.

        Comprime o caminho percorrido, para que as próximas buscas fiquem
        mais curtas. Complexidade: O(1) amortizado.
        """
        raiz = elemento
        while self._pai[raiz] != raiz:
            raiz = self._pai[raiz]
        atual = elemento
        while atual != raiz:
            proximo = self._pai[atual]
            self._pai[atual] = raiz
            atual = proximo
        return raiz

    def unir(self, primeiro: str, segundo: str) -> bool:
        """Junta os conjuntos dos dois elementos.

        Devolve ``True`` quando os conjuntos eram diferentes (e a união
        aconteceu) e ``False`` quando já estavam juntos. Complexidade:
        O(1) amortizado.
        """
        raiz_primeiro = self.encontrar(primeiro)
        raiz_segundo = self.encontrar(segundo)
        if raiz_primeiro == raiz_segundo:
            return False
        if self._tamanho[raiz_primeiro] < self._tamanho[raiz_segundo]:
            raiz_primeiro, raiz_segundo = raiz_segundo, raiz_primeiro
        self._pai[raiz_segundo] = raiz_primeiro
        self._tamanho[raiz_primeiro] += self._tamanho[raiz_segundo]
        return True


def _montar_caminho(pais: Dict[str, Optional[str]], origem: str, destino: str) -> List[str]:
    """Remonta o caminho a partir do mapa de pais montado na busca.

    Complexidade: O(comprimento do caminho).
    """
    caminho: List[str] = [destino]
    atual = destino
    while atual != origem:
        pai = pais[atual]
        if pai is None:
            return []
        caminho.append(pai)
        atual = pai
    caminho.reverse()
    return caminho
