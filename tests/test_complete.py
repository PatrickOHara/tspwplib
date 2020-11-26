"""Test that all existing instances are complete graphs"""

import networkx as nx
from tspwplib.dataset import load_tsplib_dataset


def test_tsplib_is_complete(tsplib_root, instance_name):
    """Test each instance of TSPLIB95 is a complete graph"""
    problem = load_tsplib_dataset(tsplib_root, instance_name)
    graph = problem.get_graph()
    assert nx.complete_graph(graph)
