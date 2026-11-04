"""Algoritmos de ordenação que devolvem uma lista nova.

Nenhuma das funções altera a lista recebida: todas trabalham numa cópia e
devolvem o resultado. Assim dá para usar as duas vezes, como entrada e como
saída, sem medo de perder a ordem original.

Complexidade (n é o número de elementos):
    ordenacao_por_insercao : O(n²) no pior caso, O(n) se já está ordenada
    ordenacao_por_selecao  : O(n²) sempre
    ordenacao_por_bolha    : O(n²) no pior caso, O(n) se já está ordenada
    ordenacao_por_fusao    : O(n log n) sempre
    ordenacao_rapida       : O(n log n) em média, O(n²) no pior caso
    ordenacao_por_balde    : O(n + k), com k a faixa de valores
"""

from typing import List, TypeVar

T = TypeVar("T")


def ordenacao_por_insercao(lista: List[T]) -> List[T]:
    """Ordena a lista inserindo cada elemento na posição certa.

    Complexidade: O(n²) no pior caso e O(n) quando a lista já está ordenada,
    porque o laço interno não entra nenhuma vez.
    """
    resultado = list(lista)
    for indice in range(1, len(resultado)):
        valor = resultado[indice]
        posicao = indice - 1
        while posicao >= 0 and resultado[posicao] > valor:
            resultado[posicao + 1] = resultado[posicao]
            posicao -= 1
        resultado[posicao + 1] = valor
    return resultado


def ordenacao_por_selecao(lista: List[T]) -> List[T]:
    """Ordena a lista escolhendo a cada passo o menor valor restante.

    Complexidade: O(n²) sempre, porque o menor da parte não ordenada é
    procurado a cada passo.
    """
    resultado = list(lista)
    for indice in range(len(resultado)):
        menor = indice
        for candidato in range(indice + 1, len(resultado)):
            if resultado[candidato] < resultado[menor]:
                menor = candidato
        resultado[indice], resultado[menor] = resultado[menor], resultado[indice]
    return resultado


def ordenacao_por_bolha(lista: List[T]) -> List[T]:
    """Ordena a lista trocando pares vizinhos até não haver trocas.

    Complexidade: O(n²) no pior caso e O(n) quando a lista já está ordenada,
    porque o laço externo para assim que um passe inteiro não troca nada.
    """
    resultado = list(lista)
    for fim in range(len(resultado) - 1, 0, -1):
        trocou = False
        for indice in range(fim):
            if resultado[indice] > resultado[indice + 1]:
                resultado[indice], resultado[indice + 1] = (
                    resultado[indice + 1],
                    resultado[indice],
                )
                trocou = True
        if not trocou:
            break
    return resultado


def ordenacao_por_fusao(lista: List[T]) -> List[T]:
    """Ordena a lista dividindo ao meio e fundindo as partes já ordenadas.

    Complexidade: O(n log n) sempre, e O(n) de memória auxiliar.
    """
    if len(lista) <= 1:
        return list(lista)
    meio = len(lista) // 2
    esquerda = ordenacao_por_fusao(lista[:meio])
    direita = ordenacao_por_fusao(lista[meio:])
    return _fundir(esquerda, direita)


def ordenacao_rapida(lista: List[T]) -> List[T]:
    """Ordena a lista com quicksort de três partições.

    O pivô é o elemento do meio da parte que está sendo ordenada. Com esse
    pivô, uma lista já ordenada não cai no pior caso: a divisão fica sempre
    equilibrada em duas metades.

    Complexidade: O(n log n) em média e O(n²) no pior caso. As partições em
    três grupos (menores, iguais e maiores ao pivô) fazem com que valores
    repetidos não degradem o desempenho.
    """
    resultado = list(lista)
    _ordenar_rapida(resultado, 0, len(resultado) - 1)
    return resultado


def ordenacao_por_balde(lista: List[int]) -> List[int]:
    """Ordena uma lista de inteiros com ordenação por contagem.

    A função conta quantas vezes cada número aparece e reconstrói a lista a
    partir das contagens. Só funciona com inteiros; para outros tipos leva
    ``TypeError``.

    Complexidade: O(n + k), com n o número de elementos e k a diferença entre
    o maior e o menor valor.
    """
    if not lista:
        return []
    for valor in lista:
        if not isinstance(valor, int):
            raise TypeError(
                "A ordenação por balde só aceita números inteiros, "
                "mas recebeu {0!r}.".format(valor)
            )
    menor = min(lista)
    maior = max(lista)
    contagem = [0] * (maior - menor + 1)
    for valor in lista:
        contagem[valor - menor] += 1
    resultado: List[int] = []
    for deslocamento, quantidade in enumerate(contagem):
        resultado.extend([deslocamento + menor] * quantidade)
    return resultado


def _fundir(esquerda: List[T], direita: List[T]) -> List[T]:
    """Junta duas listas já ordenadas em uma só.

    Complexidade: O(len(esquerda) + len(direita)).
    """
    resultado: List[T] = []
    indice_esquerda = 0
    indice_direita = 0
    while indice_esquerda < len(esquerda) and indice_direita < len(direita):
        if esquerda[indice_esquerda] <= direita[indice_direita]:
            resultado.append(esquerda[indice_esquerda])
            indice_esquerda += 1
        else:
            resultado.append(direita[indice_direita])
            indice_direita += 1
    resultado.extend(esquerda[indice_esquerda:])
    resultado.extend(direita[indice_direita:])
    return resultado


def _ordenar_rapida(lista: List[T], inicio: int, fim: int) -> None:
    """Ordena, no lugar, o trecho da lista entre inicio e fim."""
    if inicio >= fim:
        return
    pivo = lista[(inicio + fim) // 2]
    limite_menor = inicio
    limite_maior = fim
    atual = inicio
    while atual <= limite_maior:
        if lista[atual] < pivo:
            lista[atual], lista[limite_menor] = lista[limite_menor], lista[atual]
            limite_menor += 1
            atual += 1
        elif lista[atual] > pivo:
            lista[atual], lista[limite_maior] = lista[limite_maior], lista[atual]
            limite_maior -= 1
        else:
            atual += 1
    _ordenar_rapida(lista, inicio, limite_menor - 1)
    _ordenar_rapida(lista, limite_maior + 1, fim)
