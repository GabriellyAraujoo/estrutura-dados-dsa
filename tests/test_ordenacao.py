"""Testes dos algoritmos de ordenação."""

import pytest

from dsa import (
    ordenacao_por_bolha,
    ordenacao_por_balde,
    ordenacao_por_fusao,
    ordenacao_por_insercao,
    ordenacao_por_selecao,
    ordenacao_rapida,
)

ALGORITMOS = [
    ordenacao_por_insercao,
    ordenacao_por_selecao,
    ordenacao_por_bolha,
    ordenacao_por_fusao,
    ordenacao_rapida,
]


@pytest.mark.parametrize("algoritmo", ALGORITMOS)
def test_ordena_lista_embaralhada(algoritmo):
    assert algoritmo([5, 3, 8, 1, 9, 2]) == [1, 2, 3, 5, 8, 9]


@pytest.mark.parametrize("algoritmo", ALGORITMOS)
def test_ordena_lista_vazia(algoritmo):
    assert algoritmo([]) == []


@pytest.mark.parametrize("algoritmo", ALGORITMOS)
def test_ordena_lista_com_um_elemento(algoritmo):
    assert algoritmo([7]) == [7]


@pytest.mark.parametrize("algoritmo", ALGORITMOS)
def test_ordena_lista_ja_ordenada(algoritmo):
    assert algoritmo([1, 2, 3, 4, 5]) == [1, 2, 3, 4, 5]


@pytest.mark.parametrize("algoritmo", ALGORITMOS)
def test_ordena_lista_em_ordem_descrescente(algoritmo):
    assert algoritmo([5, 4, 3, 2, 1]) == [1, 2, 3, 4, 5]


@pytest.mark.parametrize("algoritmo", ALGORITMOS)
def test_ordena_lista_com_valores_repetidos(algoritmo):
    assert algoritmo([3, 1, 3, 2, 1]) == [1, 1, 2, 3, 3]


@pytest.mark.parametrize("algoritmo", ALGORITMOS)
def test_nao_altera_a_lista_de_entrada(algoritmo):
    original = [5, 3, 8, 1]
    copia = list(original)
    algoritmo(original)
    assert original == copia


@pytest.mark.parametrize("algoritmo", ALGORITMOS)
def test_devolve_uma_lista_nova(algoritmo):
    original = [2, 1]
    resultado = algoritmo(original)
    assert resultado is not original


@pytest.mark.parametrize("algoritmo", ALGORITMOS)
def test_ordena_lista_grande(algoritmo):
    original = list(range(200, 0, -1))
    assert algoritmo(original) == list(range(1, 201))


def test_insercao_mantem_a_ordem_dos_valores_repetidos():
    assert ordenacao_por_insercao([2, 2, 1, 2]) == [1, 2, 2, 2]


def test_selecao_mantem_a_ordem_dos_valores_repetidos():
    assert ordenacao_por_selecao([2, 2, 1, 2]) == [1, 2, 2, 2]


def test_bolha_mantem_a_ordem_dos_valores_repetidos():
    assert ordenacao_por_bolha([2, 2, 1, 2]) == [1, 2, 2, 2]


def test_fusao_mantem_a_ordem_dos_valores_repetidos():
    assert ordenacao_por_fusao([2, 2, 1, 2]) == [1, 2, 2, 2]


def test_rapida_mantem_a_ordem_dos_valores_repetidos():
    assert ordenacao_rapida([2, 2, 1, 2]) == [1, 2, 2, 2]


def test_rapida_nao_cai_no_pior_com_lista_ja_ordenada():
    original = list(range(500))
    assert ordenacao_rapida(original) == list(range(500))


def test_ordenacao_por_balde_ordena_lista_embaralhada():
    assert ordenacao_por_balde([5, 3, 8, 1, 9, 2]) == [1, 2, 3, 5, 8, 9]


def test_ordenacao_por_balde_ordena_lista_vazia():
    assert ordenacao_por_balde([]) == []


def test_ordenacao_por_balde_ordena_lista_com_um_elemento():
    assert ordenacao_por_balde([4]) == [4]


def test_ordenacao_por_balde_aceita_valores_negativos():
    assert ordenacao_por_balde([3, -2, 0, -8, 5]) == [-8, -2, 0, 3, 5]


def test_ordenacao_por_balde_aceita_valores_repetidos():
    assert ordenacao_por_balde([2, 1, 2, 1]) == [1, 1, 2, 2]


def test_ordenacao_por_balde_nao_altera_a_lista_de_entrada():
    original = [3, 1, 2]
    copia = list(original)
    ordenacao_por_balde(original)
    assert original == copia


def test_ordenacao_por_balde_com_valor_nao_inteiro_lanca_typeerror():
    with pytest.raises(TypeError):
        ordenacao_por_balde([1, 2.5, 3])


def test_ordenacao_por_balde_com_texto_lanca_typeerror():
    with pytest.raises(TypeError):
        ordenacao_por_balde(["a", "b"])
