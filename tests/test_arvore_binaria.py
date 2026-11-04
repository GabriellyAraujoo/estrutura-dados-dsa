"""Testes da árvore binária de busca."""

import pytest

from dsa import ArvoreBinaria


def _arvore_com(valores):
    """Cria uma árvore preenchida com os valores informados."""
    arvore = ArvoreBinaria()
    for valor in valores:
        arvore.inserir(valor)
    return arvore


def test_inserir_em_arvore_vazia():
    arvore = ArvoreBinaria()
    assert arvore.inserir(10) is True
    assert arvore.raiz is not None
    assert arvore.raiz.valor == 10


def test_inserir_ignora_duplicados():
    arvore = _arvore_com([5, 3, 8])
    assert arvore.inserir(5) is False
    assert arvore.contar() == 3


def test_inserir_organiza_os_valores_pelas_filas():
    arvore = _arvore_com([5, 3, 8, 1])
    assert arvore.raiz.valor == 5
    assert arvore.raiz.esquerda.valor == 3
    assert arvore.raiz.direita.valor == 8
    assert arvore.raiz.esquerda.esquerda.valor == 1


def test_buscar_encontra_valor_existente():
    arvore = _arvore_com([5, 3, 8])
    assert arvore.buscar(3) is True
    assert arvore.buscar(8) is True


def test_buscar_devolve_false_para_valor_inexistente():
    arvore = _arvore_com([5, 3, 8])
    assert arvore.buscar(7) is False


def test_buscar_em_arvore_vazia():
    arvore = ArvoreBinaria()
    assert arvore.buscar(1) is False


def test_emprumar_devolve_os_valores_em_ordem_crescente():
    arvore = _arvore_com([5, 3, 8, 1, 4, 7, 9])
    assert arvore.emprumar() == [1, 3, 4, 5, 7, 8, 9]


def test_emprumar_em_arvore_vazia():
    arvore = ArvoreBinaria()
    assert arvore.emprumar() == []


def test_emprumar_de_arvore_com_um_elemento():
    arvore = _arvore_com([42])
    assert arvore.emprumar() == [42]


def test_altura_de_arvore_vazia_e_zero():
    assert ArvoreBinaria().altura() == 0


def test_altura_de_arvore_com_um_elemento_e_um():
    assert _arvore_com([1]).altura() == 1


def test_altura_conta_os_niveis():
    arvore = _arvore_com([5, 3, 8, 1, 4])
    assert arvore.altura() == 3


def test_altura_cresce_cada_vez_que_desce_um_nivel():
    arvore = ArvoreBinaria()
    alturas = []
    for valor in [1, 2, 3, 4]:
        arvore.inserir(valor)
        alturas.append(arvore.altura())
    assert alturas == [1, 2, 3, 4]


def test_contar_de_arvore_vazia():
    assert ArvoreBinaria().contar() == 0


def test_contar_conta_todos_os_nos():
    arvore = _arvore_com([5, 3, 8, 1, 4, 7, 9])
    assert arvore.contar() == 7


def test_remover_no_sem_filhos():
    arvore = _arvore_com([5, 3, 8])
    assert arvore.remover(3) is True
    assert arvore.raiz.esquerda is None
    assert arvore.emprumar() == [5, 8]


def test_remover_no_com_um_filho_substitui_pelo_filho():
    arvore = _arvore_com([5, 3, 8, 1])
    assert arvore.remover(3) is True
    assert arvore.raiz.esquerda.valor == 1
    assert arvore.emprumar() == [1, 5, 8]


def test_remover_no_com_dois_filhos_usa_o_sucessor_em_ordem():
    arvore = _arvore_com([5, 3, 8, 1, 4, 7, 9])
    assert arvore.remover(5) is True
    assert arvore.raiz.valor == 7
    assert arvore.emprumar() == [1, 3, 4, 7, 8, 9]


def test_remover_valor_inexistente_devolve_false():
    arvore = _arvore_com([5, 3, 8])
    assert arvore.remover(99) is False
    assert arvore.contar() == 3


def test_remover_em_arvore_vazia_devolve_false():
    assert ArvoreBinaria().remover(1) is False


def test_remover_a_raiz_de_arvore_com_um_elemento():
    arvore = _arvore_com([1])
    assert arvore.remover(1) is True
    assert arvore.raiz is None
    assert arvore.contar() == 0


def test_minimo_devolve_o_menor_valor():
    arvore = _arvore_com([5, 3, 8, 1, 9])
    assert arvore.minimo() == 1


def test_maximo_devolve_o_maior_valor():
    arvore = _arvore_com([5, 3, 8, 1, 9])
    assert arvore.maximo() == 9


def test_minimo_e_maximo_em_arvore_vazia_devolvem_none():
    arvore = ArvoreBinaria()
    assert arvore.minimo() is None
    assert arvore.maximo() is None


def test_minimo_e_maximo_em_arvore_com_um_elemento():
    arvore = _arvore_com([7])
    assert arvore.minimo() == 7
    assert arvore.maximo() == 7


def test_arvore_balanceada_esta_balanceada():
    arvore = _arvore_com([5, 3, 8, 1, 4])
    assert arvore.esta_balanceada() is True


def test_arvore_desbalanceada_nao_esta_balanceada():
    arvore = _arvore_com([1, 2, 3, 4, 5])
    assert arvore.esta_balanceada() is False


def test_arvore_vazia_esta_balanceada():
    assert ArvoreBinaria().esta_balanceada() is True


def test_arvore_com_um_elemento_esta_balanceada():
    assert _arvore_com([1]).esta_balanceada() is True


def test_remover_deixa_a_arvore_balanceada():
    arvore = _arvore_com([5, 3, 8, 1, 4, 7, 9])
    arvore.remover(9)
    arvore.remover(1)
    assert arvore.esta_balanceada() is True
    assert arvore.emprumar() == [3, 4, 5, 7, 8]


def test_arvore_trabalha_com_textos():
    arvore = _arvore_com(["banana", "abacaxi", "caju"])
    assert arvore.emprumar() == ["abacaxi", "banana", "caju"]
    assert arvore.minimo() == "abacaxi"
    assert arvore.buscar("caju") is True


def test_no_guarda_valor_e_filhos():
    arvore = _arvore_com([2, 1, 3])
    no = arvore.raiz
    assert no.valor == 2
    assert no.esquerda.valor == 1
    assert no.direita.valor == 3
    with pytest.raises(AttributeError):
        no.novo_atributo = 1
