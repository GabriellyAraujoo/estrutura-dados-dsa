"""Testes da lista duplamente encadeada."""

from dsa import ListaDupla


def test_inserir_inicio_coloca_valor_no_comeco():
    lista = ListaDupla()
    lista.inserir_inicio(2)
    lista.inserir_inicio(1)
    assert list(lista) == [1, 2]


def test_inserir_fim_coloca_valor_no_fim():
    lista = ListaDupla()
    lista.inserir_fim(1)
    lista.inserir_fim(2)
    assert list(lista) == [1, 2]


def test_insercao_devolve_a_propria_lista_para_encadear():
    lista = ListaDupla()
    resultado = lista.inserir_inicio(1).inserir_inicio(2).inserir_fim(3)
    assert resultado is lista
    assert list(lista) == [2, 1, 3]


def test_inserir_em_lista_vazia():
    lista = ListaDupla()
    lista.inserir_fim(10)
    assert list(lista) == [10]
    assert lista.tamanho == 1


def test_construtor_recebe_valores_iniciais():
    lista = ListaDupla([1, 2, 3])
    assert list(lista) == [1, 2, 3]
    assert len(lista) == 3


def test_remover_remove_a_primeira_ocorrencia():
    lista = ListaDupla([1, 2, 2, 3])
    assert lista.remover(2) is True
    assert list(lista) == [1, 2, 3]


def test_remover_valor_inexistente_devolve_false():
    lista = ListaDupla([1, 2, 3])
    assert lista.remover(99) is False
    assert list(lista) == [1, 2, 3]


def test_remover_em_lista_vazia_devolve_false():
    lista = ListaDupla()
    assert lista.remover(1) is False


def test_remover_primeiro_e_ultimo_elementos():
    lista = ListaDupla([1, 2, 3])
    assert lista.remover(1) is True
    assert lista.remover(3) is True
    assert list(lista) == [2]
    lista.remover(2)
    assert list(lista) == []
    assert lista.tamanho == 0


def test_buscar_devolve_o_valor_quando_existe():
    lista = ListaDupla(["a", "b"])
    assert lista.buscar("b") == "b"


def test_buscar_devolve_none_quando_nao_existe():
    lista = ListaDupla([1, 2, 3])
    assert lista.buscar(42) is None


def test_buscar_em_lista_vazia_devolve_none():
    lista = ListaDupla()
    assert lista.buscar(1) is None


def test_contem_informa_se_o_valor_existe():
    lista = ListaDupla([1, 2, 3])
    assert lista.contem(2) is True
    assert lista.contem(9) is False


def test_tamanho_e_len_conferem_a_quantidade_de_elementos():
    lista = ListaDupla()
    assert lista.tamanho == 0
    assert len(lista) == 0
    lista.inserir_fim(1)
    lista.inserir_fim(2)
    assert lista.tamanho == 2
    assert len(lista) == 2


def test_iteracao_percorre_na_ordem_da_insercao():
    lista = ListaDupla([1, 2, 3])
    assert [valor for valor in lista] == [1, 2, 3]


def test_iteracao_em_lista_vazia_nao_falha():
    lista = ListaDupla()
    assert list(lista) == []


def test_str_mostra_os_valores_em_fila():
    lista = ListaDupla([1, 2, 3])
    assert str(lista) == "1 -> 2 -> 3"


def test_str_de_lista_vazia():
    lista = ListaDupla()
    assert str(lista) == ""


def test_inverter_devolve_nova_lista_na_ordem_reversa():
    lista = ListaDupla([1, 2, 3])
    invertida = lista.inverter()
    assert list(invertida) == [3, 2, 1]
    assert invertida is not lista


def test_inverter_nao_altera_a_lista_original():
    lista = ListaDupla([1, 2, 3])
    lista.inverter()
    assert list(lista) == [1, 2, 3]


def test_inverter_de_lista_vazia():
    lista = ListaDupla()
    assert list(lista.inverter()) == []


def test_igualdade_compara_o_conteudo():
    assert ListaDupla([1, 2, 3]) == ListaDupla([1, 2, 3])


def test_igualdade_com_conteudos_diferentes():
    assert ListaDupla([1, 2, 3]) != ListaDupla([1, 2, 4])


def test_igualdade_considera_a_ordem():
    assert ListaDupla([1, 2, 3]) != ListaDupla([3, 2, 1])


def test_igualdade_com_tamanhos_diferentes():
    assert ListaDupla([1, 2]) != ListaDupla([1, 2, 3])


def test_igualdade_com_outro_tipo_devolve_false():
    assert (ListaDupla([1, 2]) == [1, 2]) is False


def test_remover_apos_inverter():
    lista = ListaDupla([1, 2, 3])
    invertida = lista.inverter()
    assert invertida.remover(2) is True
    assert list(invertida) == [3, 1]
    assert list(lista) == [1, 2, 3]


def test_lista_aceita_valores_de_tipos_diferentes():
    lista = ListaDupla()
    lista.inserir_fim("texto")
    lista.inserir_fim(7)
    lista.inserir_fim(3.5)
    assert list(lista) == ["texto", 7, 3.5]
    assert lista.buscar(7) == 7
    assert lista.contem(3.5) is True
