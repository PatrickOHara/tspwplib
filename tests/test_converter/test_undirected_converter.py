"""Tests for converting to an undirected graph"""

import networkx as nx
from tspwplib.converter import (
    biggest_vertex_id_from_graph,
    new_dummy_vertex,
    old_vertex_from_dummy,
    to_simple_undirected,
)


def test_new_dummy_vertex():
    """New dummy vertex test"""
    biggest = 2
    assert new_dummy_vertex(0, 0, biggest) == 0
    assert new_dummy_vertex(0, 1, biggest) == -1
    assert new_dummy_vertex(0, 2, biggest) == -4
    assert new_dummy_vertex(1, 1, biggest) == -2
    assert new_dummy_vertex(2, 2, biggest) == -6


def test_old_dummy_vertex():
    """Test getting the old vertex ID from a dummy vertex"""
    biggest = 2
    assert old_vertex_from_dummy(0, 0, biggest) == 0
    assert old_vertex_from_dummy(-1, 1, biggest) == 0
    assert old_vertex_from_dummy(-4, 2, biggest) == 0
    assert old_vertex_from_dummy(-2, 1, biggest) == 1
    assert old_vertex_from_dummy(-6, 2, biggest) == 2


def test_to_simple_undirected(undirected_complete_graph):
    """Test converting a multi graph to a simple graph (both undirected)"""
    G = nx.MultiGraph(undirected_complete_graph)
    G.add_edge(0, 2, cost=1)
    G.add_edge(1, 2, cost=1)
    simple_graph = to_simple_undirected(G)
    for v in G:
        assert simple_graph.has_node(v)
    biggest = biggest_vertex_id_from_graph(G)
    dummy0 = new_dummy_vertex(0, 1, biggest)
    dummy1 = new_dummy_vertex(1, 1, biggest)
    assert simple_graph.has_node(dummy0)
    assert simple_graph.has_node(dummy1)
    assert simple_graph.has_edge(dummy0, 2)
    assert simple_graph.has_edge(dummy1, 2)
