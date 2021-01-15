"""Tests for walks"""

import pytest
import networkx as nx
from tspwplib import (
    VertexFunctionName,
    edge_list_from_walk,
    is_simple_cycle,
    is_simple_path,
    is_walk,
    total_cost_graph_tool,
    total_cost_networkx,
    total_prize,
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


def test_total_cost_graph_tool(weighted_walk_graph_tool):
    """Test total cost"""
    assert total_cost_graph_tool(weighted_walk_graph_tool, [0, 1, 2]) == 1 + 3
    assert total_cost_graph_tool(weighted_walk_graph_tool, []) == 0
    assert (
        total_cost_graph_tool(weighted_walk_graph_tool, [0, 1, 2, 1, 0])
        == 1 + 3 + 3 + 1
    )
    with pytest.raises(KeyError):
        total_cost_graph_tool(weighted_walk_graph_tool, [0, 1, 2, 3])
