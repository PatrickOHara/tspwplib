"""Test that all existing instances are complete graphs"""

import networkx as nx
import tsplib95
from tspwplib.utils import build_path_to_tsplib_instance


def test_tsplib_is_complete(tsplib_root, instance_name):
    """Test each instance of TSPLIB95 is a complete graph"""
    filepath = build_path_to_tsplib_instance(tsplib_root, instance_name)
    problem = tsplib95.load(filepath)
    graph = problem.get_graph()
    assert nx.complete_graph(graph)
