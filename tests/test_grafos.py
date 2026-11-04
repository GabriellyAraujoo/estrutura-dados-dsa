"""Testes do grafo com lista de adjacência."""

import pytest

from dsa import Grafo


def _grafo_de_tres_cidades():
    """Cria o grafo A - B - C - D, com A ligado a D."""
    grafo = Grafo()
    grafo.adicionar_aresta("A", "B")
    grafo.adicionar_aresta("B", "C")
    grafo.adicionar_aresta("C", "D")
    grafo.adicionar_aresta("A", "D")
    return grafo


def test_adicionar_vertice_cria_o_vertice():
    grafo = Grafo()
    grafo.adicionar_vertice("A")
    assert grafo.vizinhos("A") == []


def test_adicionar_vertice_repetido_nao_duplica():
    grafo = Grafo()
    grafo.adicionar_vertice("A")
    grafo.adicionar_vertice("A")
    grafo.adicionar_aresta("A", "B")
    assert grafo.vizinhos("A") == ["B"]


def test_adicionar_vertice_nao_string_lanca_typeerror():
    grafo = Grafo()
    with pytest.raises(TypeError):
        grafo.adicionar_vertice(10)


def test_aresta_nao_direcionada_vale_nos_dois_sentidos():
    grafo = Grafo()
    grafo.adicionar_aresta("A", "B")
    assert grafo.vizinhos("A") == ["B"]
    assert grafo.vizinhos("B") == ["A"]


def test_aresta_direcionada_vale_somente_do_comeco_para_o_fim():
    grafo = Grafo()
    grafo.adicionar_aresta("A", "B", direcionada=True)
    assert grafo.vizinhos("A") == ["B"]
    assert grafo.vizinhos("B") == []


def test_adicionar_aresta_nao_duplica_a_vizinhança():
    grafo = Grafo()
    grafo.adicionar_aresta("A", "B")
    grafo.adicionar_aresta("A", "B")
    grafo.adicionar_aresta("B", "A")
    assert grafo.vizinhos("A") == ["B"]
    assert grafo.vizinhos("B") == ["A"]


def test_adicionar_aresta_cria_os_vertices_que_faltam():
    grafo = Grafo()
    grafo.adicionar_aresta("A", "B")
    assert grafo.vizinhos("A") == ["B"]
    assert grafo.vizinhos("B") == ["A"]


def test_adicionar_aresta_de_um_vertice_para_si_mesmo_lanca_valueerror():
    grafo = Grafo()
    with pytest.raises(ValueError):
        grafo.adicionar_aresta("A", "A")


def test_adicionar_aresta_com_vertice_nao_string_lanca_typeerror():
    grafo = Grafo()
    with pytest.raises(TypeError):
        grafo.adicionar_aresta("A", 2)


def test_existe_aresta_responde_nos_dois_sentidos():
    grafo = Grafo()
    grafo.adicionar_aresta("A", "B")
    assert grafo.existe_aresta("A", "B") is True
    assert grafo.existe_aresta("B", "A") is True


def test_existe_aresta_falsa_quando_nao_ha_aresta():
    grafo = Grafo()
    grafo.adicionar_aresta("A", "B")
    assert grafo.existe_aresta("A", "C") is False


def test_vizinhos_de_vertice_inexistente_lanca_keyerror():
    grafo = Grafo()
    with pytest.raises(KeyError):
        grafo.vizinhos("Z")


def test_vizinhos_devolve_uma_copia_da_lista():
    grafo = Grafo()
    grafo.adicionar_aresta("A", "B")
    vizinhos = grafo.vizinhos("A")
    vizinhos.append("C")
    assert grafo.vizinhos("A") == ["B"]


def test_caminho_bfs_devolve_o_caminho_mais_curto():
    grafo = _grafo_de_tres_cidades()
    caminho = grafo.caminho_bfs("A", "C")
    assert caminho is not None
    assert caminho[0] == "A"
    assert caminho[-1] == "C"
    assert len(caminho) == 3
    for origem, destino in zip(caminho, caminho[1:]):
        assert grafo.existe_aresta(origem, destino)


def test_caminho_bfs_encontra_o_atalho_e_nao_o_caminho_longo():
    grafo = Grafo()
    grafo.adicionar_aresta("1", "2")
    grafo.adicionar_aresta("2", "3")
    grafo.adicionar_aresta("3", "4")
    grafo.adicionar_aresta("4", "5")
    grafo.adicionar_aresta("1", "5")
    assert grafo.caminho_bfs("1", "5") == ["1", "5"]


def test_caminho_bfs_entre_vertices_iguais():
    grafo = _grafo_de_tres_cidades()
    assert grafo.caminho_bfs("A", "A") == ["A"]


def test_caminho_bfs_sem_caminho_devolve_none():
    grafo = Grafo()
    grafo.adicionar_aresta("A", "B")
    grafo.adicionar_aresta("C", "D")
    assert grafo.caminho_bfs("A", "D") is None


def test_caminho_bfs_com_vertice_inexistente_devolve_none():
    grafo = _grafo_de_tres_cidades()
    assert grafo.caminho_bfs("A", "Z") is None
    assert grafo.caminho_bfs("Z", "A") is None


def test_caminho_dfs_encontra_um_caminho_valido():
    grafo = _grafo_de_tres_cidades()
    caminho = grafo.caminho_dfs("A", "C")
    assert caminho is not None
    assert caminho[0] == "A"
    assert caminho[-1] == "C"
    assert set(caminho) == {"A", "C", "D"} or set(caminho) == {"A", "B", "C"}


def test_caminho_dfs_sem_caminho_devolve_none():
    grafo = Grafo()
    grafo.adicionar_aresta("A", "B")
    grafo.adicionar_aresta("C", "D")
    assert grafo.caminho_dfs("A", "D") is None


def test_caminho_dfs_com_vertice_inexistente_devolve_none():
    grafo = _grafo_de_tres_cidades()
    assert grafo.caminho_dfs("Z", "A") is None


def test_componentes_conexas_separa_os_grupos():
    grafo = Grafo()
    grafo.adicionar_aresta("A", "B")
    grafo.adicionar_aresta("C", "D")
    grafo.adicionar_aresta("E", "F")
    assert grafo.componentes_conexas() == [["A", "B"], ["C", "D"], ["E", "F"]]


def test_componentes_conexas_em_grafo_conectado():
    grafo = _grafo_de_tres_cidades()
    assert grafo.componentes_conexas() == [["A", "B", "C", "D"]]


def test_componentes_conexas_de_grafo_vazio():
    assert Grafo().componentes_conexas() == []


def test_componentes_conexas_de_grafo_com_vertice_isolado():
    grafo = Grafo()
    grafo.adicionar_vertice("A")
    grafo.adicionar_aresta("B", "C")
    assert grafo.componentes_conexas() == [["A"], ["B", "C"]]


def test_ordem_topologica_respeita_as_arestas_direcionadas():
    grafo = Grafo()
    grafo.adicionar_aresta("a", "b", direcionada=True)
    grafo.adicionar_aresta("a", "c", direcionada=True)
    grafo.adicionar_aresta("b", "d", direcionada=True)
    grafo.adicionar_aresta("c", "d", direcionada=True)
    ordem = grafo.ordem_topologica()
    assert ordem.index("a") < ordem.index("b")
    assert ordem.index("b") < ordem.index("d")
    assert ordem.index("c") < ordem.index("d")
    assert len(ordem) == 4


def test_ordem_topologica_com_ciclo_lanca_valueerror():
    grafo = Grafo()
    grafo.adicionar_aresta("a", "b", direcionada=True)
    grafo.adicionar_aresta("b", "c", direcionada=True)
    grafo.adicionar_aresta("c", "a", direcionada=True)
    with pytest.raises(ValueError):
        grafo.ordem_topologica()


def test_ordem_topologica_de_grafo_sem_arestas():
    grafo = Grafo()
    grafo.adicionar_vertice("a")
    grafo.adicionar_vertice("b")
    assert sorted(grafo.ordem_topologica()) == ["a", "b"]


def test_arvore_geradora_minima_escolhe_as_arestas_mais_baratas():
    grafo = Grafo()
    grafo.adicionar_aresta("A", "B", peso=1.0)
    grafo.adicionar_aresta("B", "C", peso=2.0)
    grafo.adicionar_aresta("A", "C", peso=5.0)
    arvore = grafo.arvore_geradora_minima()
    arestas = {(origem, destino) for origem, destino, _ in arvore}
    assert arestas == {("A", "B"), ("B", "C")}
    assert len(arvore) == 2


def test_arvore_geradora_minima_nao_cria_ciclo():
    grafo = Grafo()
    grafo.adicionar_aresta("A", "B", peso=1.0)
    grafo.adicionar_aresta("B", "C", peso=2.0)
    grafo.adicionar_aresta("C", "A", peso=3.0)
    arvore = grafo.arvore_geradora_minima()
    assert len(arvore) == 2


def test_arvore_geradora_minima_de_grafo_sem_arestas():
    grafo = Grafo()
    grafo.adicionar_vertice("A")
    assert grafo.arvore_geradora_minima() == []


def test_arvore_geradora_minima_desconectada_devolve_uma_floresta():
    grafo = Grafo()
    grafo.adicionar_aresta("A", "B", peso=1.0)
    grafo.adicionar_aresta("C", "D", peso=1.0)
    arvore = grafo.arvore_geradora_minima()
    assert len(arvore) == 2


def test_arvore_geradora_minima_devolve_o_peso_de_cada_aresta():
    grafo = Grafo()
    grafo.adicionar_aresta("A", "B", peso=4.0)
    grafo.adicionar_aresta("B", "C", peso=7.0)
    arvore = grafo.arvore_geradora_minima()
    pesos = sorted(peso for _, _, peso in arvore)
    assert pesos == [4.0, 7.0]
