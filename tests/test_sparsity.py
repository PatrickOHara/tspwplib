"""Tests for sparsity"""

import networkx as nx
from tsplib95.models import StandardProblem
from tspwplib.sparsity import remove_random_edges_from_graph
from tspwplib.utils import build_path_to_tsplib_instance

def test_remove_gamma_edges_from_graph(tsplib_root, instance_name):
    """Test the right number of edges are removed"""
    filepath = build_path_to_tsplib_instance(tsplib_root, instance_name)
    problem = StandardProblem.load(filepath)
    complete_graph = problem.get_graph()
    assert nx.complete_graph(complete_graph)
    smaller_graph = remove_random_edges_from_graph(complete_graph, edge_removal_probability=0.5)
    assert not nx.complete_graph(smaller_graph)
    assert nx.is_connected(smaller_graph)

def test_measure_sparsity_metrics():
    """Test the sparsity of graphs is measured correctly"""
