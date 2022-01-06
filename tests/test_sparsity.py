"""Tests for sparsity"""

import pytest
from tspwplib import (
    ProfitsProblem,
    build_path_to_oplib_instance,
    sparsify_by_cost,
    sparsify_uid,
)


@pytest.mark.parametrize("k", [1, 2, 5, 10])
def test_sparsify_uid(oplib_root, generation, graph_name, k):
    """Test sparsity is created uniformly and independently"""
    filepath = build_path_to_oplib_instance(oplib_root, generation, graph_name)
    complete_problem = ProfitsProblem.load(filepath)
    complete_graph = complete_problem.get_graph()
    sparse_graph = sparsify_uid(complete_graph, k)
    assert sparse_graph.number_of_nodes() == complete_graph.number_of_nodes()
    assert sparse_graph.number_of_edges() == complete_graph.number_of_nodes() * k


@pytest.mark.parametrize("k", [1, 2, 5, 10])
def test_sparsity_by_cost(oplib_root, generation, graph_name, k):
    """Test sparsity where edge removal is weighted by cost"""
    filepath = build_path_to_oplib_instance(oplib_root, generation, graph_name)
    complete_problem = ProfitsProblem.load(filepath)
    complete_graph = complete_problem.get_graph()
    sparse_graph = sparsify_by_cost(complete_graph, k, cost_attr="cost")
    assert sparse_graph.number_of_nodes() == complete_graph.number_of_nodes()
    assert sparse_graph.number_of_edges() == complete_graph.number_of_nodes() * k
