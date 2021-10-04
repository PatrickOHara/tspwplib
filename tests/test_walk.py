"""Tests for walks"""

import pytest
import networkx as nx
from tspwplib import (
    EdgesNotAdjacentException,
    NotSimpleException,
    VertexFunctionName,
    edge_list_from_walk,
    is_simple_cycle,
    is_simple_path,
    is_walk,
    order_edge_list,
    remove_self_loops_from_edge_list,
    reorder_edge_list_from_root,
    total_cost_networkx,
    total_prize,
    vertex_set_from_edge_list,
    walk_from_edge_list,
)


def test_is_open_walk_is_walk(walk_graph, open_walk):
    """Test walks"""
    assert is_walk(walk_graph, open_walk)


def test_is_not_a_walk(walk_graph, not_a_walk):
    """Test invalid walks are detected"""
    assert not is_walk(walk_graph, not_a_walk)


def test_edge_list_from_walk():
    """Test edge list from any walk"""
    assert edge_list_from_walk([]) == []
    assert edge_list_from_walk([0]) == []
    assert edge_list_from_walk([0, 1, 3, 1, 2]) == [(0, 1), (1, 3), (3, 1), (1, 2)]


def test_vertex_set_from_edge_list():
    """Test a vertex set is returned from an edge list"""
    assert vertex_set_from_edge_list([]) == set()
    assert vertex_set_from_edge_list([(0, 1), (1, 2), (2, 2)]) == {0, 1, 2}


def test_order_edge_list():
    """Test edges can be ordered"""
    edges1 = [(0, 1), (1, 2), (2, 3)]
    edges2 = [(1, 0), (2, 1), (0, 2)]
    edges3 = [(1, 0), (2, 1), (0, 2), (3, 4), (4, 5), (3, 5)]
    edges4 = [(0, 1), (2, 3), (1, 2)]
    edges5 = [(0, 2), (2, 7), (4, 6), (6, 7), (0, 1), (1, 4)]
    assert order_edge_list(edges1) == edges1
    assert order_edge_list(edges2) == [(1, 0), (0, 2), (2, 1)]
    assert order_edge_list(edges4) == edges1
    assert order_edge_list(edges5)
    with pytest.raises(NotSimpleException):
        order_edge_list(edges3)


def test_reorder_edge_list_from_root():
    """Test edges are reordered starting and ending at root"""
    root = 0
    edges1 = [(2, 3), (1, 2), (0, 1)]
    edges2 = [(2, 1), (1, 0), (0, 2)]
    edges3 = []
    edges4 = [(1, 0), (2, 1), (0, 2)]
    ordered1 = reorder_edge_list_from_root(edges1, root)
    ordered2 = reorder_edge_list_from_root(edges2, root)
    ordered4 = reorder_edge_list_from_root(edges4, root)
    assert root in ordered1[0]
    assert root in ordered2[0]
    assert root in ordered2[len(ordered2) - 1]
    with pytest.raises(nx.NodeNotFound):
        reorder_edge_list_from_root(edges3, root)
    assert root in ordered4[0]
    assert root in ordered4[len(ordered4) - 1]


def test_walk_from_edge_list():
    """Test a walk is returned from an edge list"""
    assert walk_from_edge_list([]) == []
    assert walk_from_edge_list([(0, 1)]) == [0, 1]
    assert walk_from_edge_list([(0, 1), (2, 1)]) == [0, 1, 2]
    assert walk_from_edge_list([(1, 0), (2, 1), (0, 2)]) == [0, 1, 2, 0]
    with pytest.raises(EdgesNotAdjacentException):
        walk_from_edge_list([(0, 1), (2, 3)])
    with pytest.raises(EdgesNotAdjacentException):
        walk_from_edge_list([(0, 1), (2, 1), (0, 3)])
    with pytest.raises(EdgesNotAdjacentException):
        walk_from_edge_list([(0, 1), (2, 1), (1, 0)])


def test_is_simple_path(walk_graph, simple_path):
    """Test simple paths"""
    assert is_simple_path(walk_graph, simple_path)


def test_walk_is_not_simple_path(walk_graph, open_walk):
    """Test walks with repeated vertices are not simple paths"""
    if len(open_walk) > 1:
        assert not is_simple_path(walk_graph, open_walk)


def test_simple_cycle_is_not_simple_path(walk_graph, simple_cycle):
    """Test cycles are not simple paths"""
    if len(simple_cycle) > 1:
        assert not is_simple_path(walk_graph, simple_cycle)


def test_is_simple_cycle(walk_graph, simple_cycle):
    """Test cycles are simple"""
    assert is_simple_cycle(walk_graph, simple_cycle)


def test_path_is_not_simple_cycle(walk_graph, simple_path):
    """Test paths are not cycles"""
    if len(simple_path) > 1:
        assert not is_simple_cycle(walk_graph, simple_path)


def test_total_cost_networkx(weighted_walk_networkx_graph):
    """Test total cost"""
    assert total_cost_networkx(weighted_walk_networkx_graph, [0, 1, 2]) == 1 + 3
    assert total_cost_networkx(weighted_walk_networkx_graph, []) == 0
    assert (
        total_cost_networkx(weighted_walk_networkx_graph, [0, 1, 2, 1, 0])
        == 1 + 3 + 3 + 1
    )
    with pytest.raises(KeyError):
        total_cost_networkx(weighted_walk_networkx_graph, [0, 1, 2, 3])


def test_total_prize(weighted_walk_networkx_graph):
    """Test total prize"""
    prizes = nx.get_node_attributes(
        weighted_walk_networkx_graph, VertexFunctionName.prize
    )
    assert total_prize(prizes, [0, 1, 2]) == 3
    assert total_prize(prizes, []) == 0


def test_remove_self_loops_from_edge_list():
    """Test all self loops are removed"""
    edge_list = [(0, 1), (1, 3), (3, 1), (1, 2)]
    assert remove_self_loops_from_edge_list(edge_list) == edge_list
    with_self_loop = edge_list + [(5, 5), (6, 6)]
    assert remove_self_loops_from_edge_list(with_self_loop) == edge_list
