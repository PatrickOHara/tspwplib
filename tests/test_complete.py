"""Test that all existing instances are complete graphs"""

import networkx as nx
import tsplib95
from tspwplib import (
    is_complete,
    is_complete_with_self_loops,
    build_path_to_tsplib_instance,
)


def test_is_complete():
    """Test the is complete function"""
    for k in range(0, 10):
        graph = nx.complete_graph(k)
        assert is_complete(graph)
        assert sum(range(graph.number_of_nodes())) == graph.number_of_edges()


def test_is_complete_with_self_loops():
    """Test graph is complete and has self loops"""
    for k in range(1, 10):
        graph = nx.complete_graph(k)
        assert is_complete(graph)
        assert not is_complete_with_self_loops(graph)
        for u in graph:
            graph.add_edge(u, u)
        assert is_complete_with_self_loops(graph)


def test_tsplib_is_complete(tsplib_root, graph_name):
    """Test each instance of TSPLIB95 is a complete graph"""
    filepath = build_path_to_tsplib_instance(tsplib_root, graph_name)
    problem = tsplib95.load(filepath)
    graph = problem.get_graph()
    assert is_complete_with_self_loops(graph)
