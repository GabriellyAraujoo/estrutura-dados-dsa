"""Testes dos algoritmos de busca em listas."""

import pytest

from dsa import (
    busca_binaria,
    busca_em_lista_ordenada,
    busca_linear,
    busca_por_salto,
    busca_ternaria,
)

LISTA_ORDENADA = [2, 4, 6, 8, 10, 12, 14, 16, 18, 20]
BUSCAS_ORDENADAS = [busca_binaria, busca_ternaria, busca_por_salto]


@pytest.mark.parametrize("busca", BUSCAS_ORDENADAS)
def test_busca_encontra_o_alvo_presente(busca):
    indice = busca(LISTA_ORDENADA, 12)
    assert indice != -1
    assert LISTA_ORDENADA[indice] == 12


@pytest.mark.parametrize("busca", BUSCAS_ORDENADAS)
def test_busca_devolve_menos_um_quando_o_alvo_nao_existe(busca):
    assert busca(LISTA_ORDENADA, 13) == -1


@pytest.mark.parametrize("busca", BUSCAS_ORDENADAS)
def test_busca_em_lista_vazia_devolve_menos_um(busca):
    assert busca([], 5) == -1


@pytest.mark.parametrize("busca", BUSCAS_ORDENADAS)
def test_busca_em_lista_com_um_elemento(busca):
    assert busca([7], 7) == 0
    assert busca([7], 8) == -1


@pytest.mark.parametrize("busca", BUSCAS_ORDENADAS)
def test_busca_encontra_o_primeiro_e_o_ultimo_elemento(busca):
    assert busca(LISTA_ORDENADA, 2) == 0
    assert busca(LISTA_ORDENADA, 20) == len(LISTA_ORDENADA) - 1


@pytest.mark.parametrize("busca", BUSCAS_ORDENADAS)
def test_busca_encontra_o_alvo_menor_que_o_primeiro(busca):
    assert busca(LISTA_ORDENADA, 1) == -1


@pytest.mark.parametrize("busca", BUSCAS_ORDENADAS)
def test_busca_encontra_o_alvo_maior_que_o_ultimo(busca):
    assert busca(LISTA_ORDENADA, 21) == -1


def test_busca_linear_encontra_o_alvo_presente():
    indice = busca_linear([3, 1, 4, 1, 5], 4)
    assert indice == 2


def test_busca_linear_devolve_menos_um_quando_o_alvo_nao_existe():
    assert busca_linear([3, 1, 4], 9) == -1


def test_busca_linear_em_lista_vazia_devolve_menos_um():
    assert busca_linear([], 1) == -1


def test_busca_linear_funciona_com_lista_desordenada():
    assert busca_linear([9, 3, 7, 1], 7) == 2


def test_busca_linear_devolve_a_primeira_ocorrencia():
    assert busca_linear([1, 2, 2, 2], 2) == 1


def test_busca_em_lista_ordenada_encontra_o_alvo_em_lista_pequena():
    pequena = list(range(10))
    indice = busca_em_lista_ordenada(pequena, 7)
    assert indice == 7


def test_busca_em_lista_ordenada_encontra_o_alvo_em_lista_grande():
    grande = list(range(1000))
    indice = busca_em_lista_ordenada(grande, 731)
    assert indice == 731


def test_busca_em_lista_ordenada_usa_a_linear_abaixo_do_limiar(monkeypatch):
    chamadas = []

    def linear(lista, alvo):
        chamadas.append("linear")
        return -1

    def binaria(lista, alvo):
        chamadas.append("binaria")
        return -1

    monkeypatch.setattr("dsa.busca.busca_linear", linear)
    monkeypatch.setattr("dsa.busca.busca_binaria", binaria)
    busca_em_lista_ordenada(list(range(10)), 5)
    assert chamadas == ["linear"]


def test_busca_em_lista_ordenada_usa_a_binaria_acima_do_limiar(monkeypatch):
    chamadas = []

    def linear(lista, alvo):
        chamadas.append("linear")
        return -1

    def binaria(lista, alvo):
        chamadas.append("binaria")
        return -1

    monkeypatch.setattr("dsa.busca.busca_linear", linear)
    monkeypatch.setattr("dsa.busca.busca_binaria", binaria)
    busca_em_lista_ordenada(list(range(100)), 50)
    assert chamadas == ["binaria"]


def test_busca_em_lista_ordenada_devolve_menos_um_quando_o_alvo_nao_existe():
    lista = list(range(100))
    assert busca_em_lista_ordenada(lista, 150) == -1


def test_busca_em_lista_ordenada_em_lista_vazia():
    assert busca_em_lista_ordenada([], 1) == -1


def test_busca_em_lista_ordenada_encontra_o_alvo_em_lista_pequena_e_grande():
    for tamanho in (5, 100):
        lista = list(range(tamanho))
        assert busca_em_lista_ordenada(lista, tamanho - 1) == tamanho - 1
        assert busca_em_lista_ordenada(lista, tamanho) == -1


def test_busca_por_salto_encontra_o_alvo_em_lista_grande():
    lista = list(range(0, 1000, 2))
    indice = busca_por_salto(lista, 500)
    assert indice == 250


def test_busca_binaria_devolve_menos_um_em_lista_nao_ordenada_e_fora_do_intervalo():
    assert busca_binaria([1, 3, 5, 7, 9], 0) == -1
