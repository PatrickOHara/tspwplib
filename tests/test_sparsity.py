"""Tests for sparsity"""

from tsplib95.models import StandardProblem
from tspwplib import (
    is_complete_with_self_loops,
    remove_random_edges_from_graph,
    build_path_to_tsplib_instance,
)


def test_remove_random_edges_from_graph(
    tsplib_root, graph_name, edge_removal_probability
):
    """Test the right number of edges are removed"""
    filepath = build_path_to_tsplib_instance(tsplib_root, graph_name)
    problem = StandardProblem.load(filepath)
    complete_graph = problem.get_graph()
    assert is_complete_with_self_loops(complete_graph)
    smaller_graph = remove_random_edges_from_graph(
        complete_graph, edge_removal_probability=edge_removal_probability
    )
    # edge cases
    if edge_removal_probability == 0:
        assert smaller_graph.number_of_edges() == complete_graph.number_of_edges()
    elif edge_removal_probability == 1.0:
        assert smaller_graph.number_of_edges() == 0
    # sufficient number of nodes for randomness to not have big effect
    elif smaller_graph.number_of_nodes() > 10:
        assert not is_complete_with_self_loops(smaller_graph)
        num_edges_lower_bound = complete_graph.number_of_edges() * (
            1 - edge_removal_probability - 0.1
        )
        num_edges_upper_bound = complete_graph.number_of_edges() * (
            1 - edge_removal_probability + 0.1
        )
        assert (
            num_edges_lower_bound
            <= smaller_graph.number_of_edges()
            <= num_edges_upper_bound
        )


def test_measure_sparsity_metrics():
    """Test the sparsity of graphs is measured correctly"""
