# Estruturas de Dados e Algoritmos em Python

Implementação do zero das estruturas de dados e dos algoritmos que aparecem com mais
frequência em entrevistas técnicas para vagas júnior: listas encadeadas, pilhas e
filas, árvores binárias de busca, tabelas hash, ordenação, grafos e algoritmos de
busca.

Tudo aqui foi escrito à mão, em Python 3.9, sem usar nenhuma biblioteca de estrutura
de dados pronta (nem `collections.deque`, nem `heapq`). Cada estrutura tem testes
próprios, os testes rodam em todas as versões do Python da CI e a complexidade de
cada operação está escrita no docstring da função correspondente.

## O que tem dentro

| Módulo | O que implementa | Complexidade |
| --- | --- | --- |
| `dsa/linked_list.py` | `ListaDupla`, lista duplamente encadeada genérica, com inserção e remoção nas pontas, busca, inversão e comparação por conteúdo | inserir e remover nas pontas O(1); buscar, remover e inverter O(n) |
| `dsa/pilha_fila.py` | `Pilha` (LIFO) e `Fila` (FIFO) | empilhar, desempilhar, enfileirar e desenfileirar O(1) amortizado; topo, frente, tamanho e `len` O(1) |
| `dsa/arvore_binaria.py` | `ArvoreBinaria`, árvore binária de busca, com inserção, busca, remoção (nos três casos: sem filhos, com um filho e com dois filhos), percurso em ordem, altura, contagem, mínimo, máximo e teste de balanceamento | inserir, buscar e remover O(h), sendo O(log n) em árvore balanceada; percurso em ordem e contagem O(n) |
| `dsa/tabela_hash.py` | `TabelaHash` com encadeamento, que cresce sozinha quando a carga passa de 75% da capacidade | inserir, buscar e remover O(1) em média; redimensionar O(n) |
| `dsa/ordenacao.py` | ordenação por inserção, seleção, bolha, fusão, rápida e por balde (contagem), todas devolvendo uma lista nova | inserção e bolha O(n²) no pior caso; seleção O(n²); fusão O(n log n); rápida O(n log n) em média; balde O(n + k) |
| `dsa/grafos.py` | `Grafo` com lista de adjacência, busca em largura, busca em profundidade, componentes conexas, ordem topológica e árvore geradora mínima (Kruskal com union-find) | busca, componentes e ordem topológica O(v + e); árvore geradora mínima O(e log e) |
| `dsa/busca.py` | busca linear, binária, ternária, por salto e uma busca que escolhe automaticamente entre a linear e a binária | linear O(n); binária O(log n); ternária O(log₃ n); por salto O(√n) |

A complexidade citada em cada função está no docstring dela, com a notação O e o
significado das letras (n é o número de elementos, h é a altura da árvore, v e e são
número de vértices e de arestas).

## Como rodar

Precisa de Python 3.9 ou mais novo. Os testes usam `pytest`:

```bash
git clone https://github.com/GabriellyAraujoo/estrutura-dados-dsa.git
cd estrutura-dados-dsa
python3 -m pip install -r requirements-dev.txt
python3 -m pytest -v
```

Um exemplo de uso, que roda direto no terminal:

```python
from dsa import ArvoreBinaria, Fila, Grafo, ListaDupla, TabelaHash, ordenacao_rapida

# Lista duplamente encadeada
lista = ListaDupla([3, 1, 2])
lista.inserir_fim(4)
print(lista)              # 3 -> 1 -> 2 -> 4
print(list(lista.inverter()))   # [4, 2, 1, 3]

# Ordenação que não altera a lista de entrada
numeros = [8, 3, 7, 1]
print(ordenacao_rapida(numeros))   # [1, 3, 7, 8]
print(numeros)                    # [8, 3, 7, 1]

# Árvore binária de busca
arvore = ArvoreBinaria()
for valor in [50, 30, 70, 20, 40]:
    arvore.inserir(valor)
print(arvore.emprumar())          # [20, 30, 40, 50, 70]
print(arvore.altura())            # 3

# Tabela hash com encadeamento
tabela = TabelaHash()
tabela.inserir("nome", "Ana")
tabela.inserir("cidade", "Brasilia")
print(tabela.buscar("nome"))      # Ana
print(tabela.buscar("idade"))     # None

# Fila e grafo
fila = Fila(["a", "b", "c"])
print(fila.desenfileirar())       # a

grafo = Grafo()
grafo.adicionar_aresta("A", "B")
grafo.adicionar_aresta("B", "C")
print(grafo.caminho_bfs("A", "C"))   # ['A', 'B', 'C']
print(grafo.componentes_conexas())   # [['A', 'B', 'C']]
```

## Decisões de implementação

**Lista duplamente encadeada em vez de lista do Python.** A lista do Python é um
array: é rápida, mas inserir ou remover no começo custa O(n), porque todos os
elementos são deslocados. Neste projeto a `ListaDupla` guarda ponteiros para o
anterior e o próximo, e por isso inserir e remover nas pontas custa O(1). É a mesma
razão pela qual a fila usa um índice de início em vez de `pop(0)`, que também
deslocaria tudo. O preço disso é mais memória por elemento e um uso de memória que
não é contígua, então a estrutura perde para a lista do Python em acesso aleatório.

**Union-find no Kruskal.** A árvore geradora mínima escolhe a aresta mais barata
que não fecha ciclo. Para saber se uma aresta fecharia ciclo é preciso saber se os
dois vértices já estão no mesmo conjunto, e o union-find responde a isso com
compressão de caminho e união por tamanho, tudo em tempo praticamente constante.
Sem ele, o Kruskal teria de refazer uma busca de conectividade a cada aresta.

**Pivô do meio na ordenação rápida.** Escolher o primeiro ou o último elemento como
pivô faz a quicksort cair em O(n²) justamente nos casos mais comuns, como uma lista
já ordenada. O pivô do meio divide a lista em duas metades, então o pior caso
desaparece na prática. Usei a variante de três partições (menores, iguais e maiores
que o pivô), que também resolve o problema de valores repetidos, que com a partição
comum degrada o desempenho.

**Ordenações que devolvem uma lista nova.** Nenhuma função de ordenação altera a
lista recebida. Isso custa uma cópia a cada chamada, mas evita a surpresa clássica
de uma função que "consome" o argumento, e deixa o comportamento previsível para
quem usa a biblioteca.

## O que eu quero revisar depois

- **Balanceamento da árvore.** Hoje a árvore binária de busca fica degenerada em
  O(n) quando recebe valores já ordenados. Quero implementar a rotação
  esquerda/direita e o AVL, com os casos de inserção e remoção rebalanceando a
  árvore, e medir a diferença de altura entre as duas versões.
- **Testes de desempenho.** Hoje os testes verificam o comportamento, e não a
  velocidade. Quero medir o tempo de cada algoritmo com listas de tamanho
  crescente para confirmar na prática os custos que estão nos docstrings.
- **Estruturas de dados persistentes (imutáveis).** Quero entender a versão
  imutável da lista encadeada e da árvore, em que cada operação devolve uma
  estrutura nova compartilhando o que não mudou, e usá-la para comparar snapshots.
