"""Testes da tabela hash com encadeamento."""

import pytest

from dsa import TabelaHash


def test_inserir_e_buscar_valor():
    tabela = TabelaHash()
    tabela.inserir("nome", "Ana")
    tabela.inserir("cidade", "Brasilia")
    assert tabela.buscar("nome") == "Ana"
    assert tabela.buscar("cidade") == "Brasilia"


def test_buscar_chave_ausente_devolve_none():
    tabela = TabelaHash()
    tabela.inserir("nome", "Ana")
    assert tabela.buscar("idade") is None


def test_buscar_em_tabela_vazia_devolve_none():
    assert TabelaHash().buscar("qualquer") is None


def test_inserir_chave_existente_atualiza_o_valor():
    tabela = TabelaHash()
    tabela.inserir("nome", "Ana")
    tabela.inserir("nome", "Beatriz")
    assert tabela.buscar("nome") == "Beatriz"
    assert tabela.tamanho == 1


def test_remover_chave_existente_devolve_true():
    tabela = TabelaHash()
    tabela.inserir("nome", "Ana")
    assert tabela.remover("nome") is True
    assert tabela.buscar("nome") is None
    assert tabela.tamanho == 0


def test_remover_chave_ausente_devolve_false():
    tabela = TabelaHash()
    tabela.inserir("nome", "Ana")
    assert tabela.remover("idade") is False
    assert tabela.tamanho == 1


def test_remover_em_tabela_vazia_devolve_false():
    assert TabelaHash().remover("nome") is False


def test_contem_informa_se_a_chave_existe():
    tabela = TabelaHash()
    tabela.inserir("nome", "Ana")
    assert tabela.contem("nome") is True
    assert tabela.contem("idade") is False


def test_contem_em_tabela_vazia():
    assert TabelaHash().contem("nome") is False


def test_tamanho_e_len_conferem_a_quantidade_de_itens():
    tabela = TabelaHash()
    assert tabela.tamanho == 0
    assert len(tabela) == 0
    tabela.inserir("a", 1)
    tabela.inserir("b", 2)
    assert tabela.tamanho == 2
    assert len(tabela) == 2


def test_capacidade_inicial_e_respeitada():
    tabela = TabelaHash(capacidade_inicial=4)
    assert tabela.capacidade == 4


def test_capacidade_inicial_invalida_lanca_valueerror():
    with pytest.raises(ValueError):
        TabelaHash(capacidade_inicial=0)


def test_redimensionar_dobra_a_capacidade():
    tabela = TabelaHash(capacidade_inicial=4)
    tabela.redimensionar()
    assert tabela.capacidade == 8


def test_redimensionar_aceita_uma_capacidade_especifica():
    tabela = TabelaHash(capacidade_inicial=4)
    tabela.redimensionar(16)
    assert tabela.capacidade == 16


def test_redimensionar_com_capacidade_invalida_lanca_valueerror():
    tabela = TabelaHash()
    with pytest.raises(ValueError):
        tabela.redimensionar(0)


def test_tabela_cresce_quando_passa_do_limiar_de_carga():
    tabela = TabelaHash(capacidade_inicial=4)
    capacidade_inicial = tabela.capacidade
    for indice in range(10):
        tabela.inserir("chave{0}".format(indice), indice)
    assert tabela.capacidade > capacidade_inicial
    assert tabela.capacidade >= tabela.tamanho


def test_itens_sao_preservados_apos_o_crescimento():
    tabela = TabelaHash(capacidade_inicial=4)
    for indice in range(50):
        tabela.inserir("chave{0}".format(indice), indice)
    assert tabela.tamanho == 50
    for indice in range(50):
        assert tabela.buscar("chave{0}".format(indice)) == indice


def test_itens_sao_preservados_apos_redimensionamento_manual():
    tabela = TabelaHash(capacidade_inicial=4)
    tabela.inserir("a", 1)
    tabela.inserir("b", 2)
    tabela.redimensionar(64)
    assert tabela.buscar("a") == 1
    assert tabela.buscar("b") == 2
    assert tabela.tamanho == 2


def test_chaves_iguais_ficam_no_mesmo_balde_e_nao_duplicam():
    tabela = TabelaHash(capacidade_inicial=8)
    tabela.inserir("igual", 1)
    tabela.inserir("igual", 2)
    assert tabela.tamanho == 1
    assert tabela.buscar("igual") == 2


def test_tabela_aceita_chaves_e_valores_de_tipos_diferentes():
    tabela = TabelaHash()
    tabela.inserir(1, "um")
    tabela.inserir("1", "texto um")
    assert tabela.buscar(1) == "um"
    assert tabela.buscar("1") == "texto um"
    assert tabela.tamanho == 2


def test_valores_none_sao_aceitos():
    tabela = TabelaHash()
    tabela.inserir("vazio", None)
    assert tabela.buscar("vazio") is None
    assert tabela.contem("vazio") is True
    assert tabela.tamanho == 1
