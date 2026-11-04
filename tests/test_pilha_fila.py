"""Testes da pilha e da fila."""

import pytest

from dsa import Fila, Pilha


def test_pilha_devolve_o_ultimo_que_entrou():
    pilha = Pilha()
    pilha.empilhar(1)
    pilha.empilhar(2)
    pilha.empilhar(3)
    assert pilha.desempilhar() == 3
    assert pilha.desempilhar() == 2
    assert pilha.desempilhar() == 1


def test_pilha_topo_mostra_sem_remover():
    pilha = Pilha()
    pilha.empilhar("a")
    pilha.empilhar("b")
    assert pilha.topo() == "b"
    assert pilha.tamanho == 2


def test_pilha_nova_esta_vazia():
    pilha = Pilha()
    assert pilha.vazia is True
    assert pilha.tamanho == 0
    assert len(pilha) == 0


def test_pilha_com_elementos_nao_esta_vazia():
    pilha = Pilha()
    pilha.empilhar(1)
    assert pilha.vazia is False
    assert pilha.tamanho == 1
    assert len(pilha) == 1


def test_pilha_desempilhar_vazia_lanca_indexerror():
    pilha = Pilha()
    with pytest.raises(IndexError) as erro:
        pilha.desempilhar()
    assert "vazia" in str(erro.value)


def test_pilha_topo_vazio_lanca_indexerror():
    pilha = Pilha()
    with pytest.raises(IndexError) as erro:
        pilha.topo()
    assert "vazia" in str(erro.value)


def test_pilha_esvazia_ao_remover_tudo():
    pilha = Pilha()
    pilha.empilhar(1)
    pilha.desempilhar()
    assert pilha.vazia is True


def test_pilha_empilha_e_desempilha_muitos_elementos():
    pilha = Pilha()
    for numero in range(100):
        pilha.empilhar(numero)
    for numero in reversed(range(100)):
        assert pilha.desempilhar() == numero
    assert pilha.vazia is True


def test_fila_devolve_o_primeiro_que_entrou():
    fila = Fila()
    fila.enfileirar(1)
    fila.enfileirar(2)
    fila.enfileirar(3)
    assert fila.desenfileirar() == 1
    assert fila.desenfileirar() == 2
    assert fila.desenfileirar() == 3


def test_fila_frente_mostra_sem_remover():
    fila = Fila()
    fila.enfileirar("a")
    fila.enfileirar("b")
    assert fila.frente() == "a"
    assert fila.tamanho == 2


def test_fila_nova_esta_vazia():
    fila = Fila()
    assert fila.vazia is True
    assert fila.tamanho == 0
    assert len(fila) == 0


def test_fila_com_elementos_nao_esta_vazia():
    fila = Fila()
    fila.enfileirar(1)
    assert fila.vazia is False
    assert fila.tamanho == 1
    assert len(fila) == 1


def test_fila_desenfileirar_vazia_lanca_indexerror():
    fila = Fila()
    with pytest.raises(IndexError) as erro:
        fila.desenfileirar()
    assert "vazia" in str(erro.value)


def test_fila_frente_vazia_lanca_indexerror():
    fila = Fila()
    with pytest.raises(IndexError) as erro:
        fila.frente()
    assert "vazia" in str(erro.value)


def test_fila_esvazia_ao_remover_tudo():
    fila = Fila()
    fila.enfileirar(1)
    fila.desenfileirar()
    assert fila.vazia is True
    assert len(fila) == 0


def test_fila_mantem_a_ordem_de_entrada():
    fila = Fila()
    for numero in range(50):
        fila.enfileirar(numero)
    for numero in range(50):
        assert fila.desenfileirar() == numero
    assert fila.vazia is True


def test_fila_intercala_enfileirar_e_desenfileirar():
    fila = Fila()
    fila.enfileirar(1)
    fila.enfileirar(2)
    assert fila.desenfileirar() == 1
    fila.enfileirar(3)
    assert fila.desenfileirar() == 2
    assert fila.desenfileirar() == 3
    assert fila.vazia is True


def test_pilha_e_fila_guardam_o_que_foi_passado_no_construtor():
    pilha = Pilha([1, 2, 3])
    fila = Fila([1, 2, 3])
    assert pilha.topo() == 3
    assert fila.frente() == 1
