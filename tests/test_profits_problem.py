"""Test the TSP with Profits Problem class"""

import math
import pytest
import networkx as nx
from tspwplib import (
    Generation,
    ProfitsProblem,
    EdgeFunctionName,
    OptimalSolutionTSP,
    VertexFunctionName,
    build_path_to_oplib_instance,
    is_pctsp_yes_instance,
)


def test_parse_profits_problem(oplib_root, generation, graph_name):
    """Test an OP instance can be parsed"""
    filepath = build_path_to_oplib_instance(oplib_root, generation, graph_name)
    assert "COST_LIMIT" in ProfitsProblem.fields_by_keyword
    assert "NODE_SCORE_SECTION" in ProfitsProblem.fields_by_keyword

    problem = ProfitsProblem.load(filepath)
    assert problem.is_complete()


def test_get_cost_limit(oplib_root, generation, graph_name, alpha):
    """Test we can get the cost limit"""
    filepath = build_path_to_oplib_instance(oplib_root, generation, graph_name)
    problem = ProfitsProblem.load(filepath)
    expected_cost_limit = math.ceil(OptimalSolutionTSP[graph_name] * (alpha / 100.0))
    assert problem.get_cost_limit() == expected_cost_limit


def test_get_node_score(oplib_root, generation, graph_name):
    """Test every node has a prize"""
    filepath = build_path_to_oplib_instance(oplib_root, generation, graph_name)
    problem = ProfitsProblem.load(filepath)
    node_scores = problem.get_node_score()
    assert isinstance(node_scores, dict)
    for vertex in problem.get_nodes():
        assert vertex in node_scores
        value = node_scores[vertex]
        assert value >= 0


def test_get_graph(oplib_root, generation, graph_name):
    """Test we can load a graph with prizes"""
    filepath = build_path_to_oplib_instance(oplib_root, generation, graph_name)
    problem = ProfitsProblem.load(filepath)
    graph = problem.get_graph()
    prizes = problem.get_node_score()

    assert nx.complete_graph(graph)

    for vertex in range(1, graph.number_of_nodes() + 1):
        assert vertex in graph

    for vertex, data in graph.nodes(data=True):
        assert data[VertexFunctionName.prize] == prizes[vertex]

    # check every edge has an attribute called 'cost'
    for _, _, data in graph.edges(data=True):
        assert EdgeFunctionName.cost in data

    # bool and list breaks pyintergraph so we avoid it
    valid_types = [str, int, float, bool]
    for _, _, data in graph.edges(data=True):
        for _, value in data.items():
            assert type(value) in valid_types

    for _, data in graph.nodes(data=True):
        for _, value in data.items():
            assert type(value) in valid_types

    assert graph.graph["root"] == 1


def test_get_root_vertex(oplib_root, generation, graph_name):
    """Test the root vertex is 1 when un-normalized (0 when normalized)"""
    filepath = build_path_to_oplib_instance(oplib_root, generation, graph_name)
    problem = ProfitsProblem.load(filepath)
    assert problem.get_root_vertex(normalize=False) == 1
    assert problem.get_root_vertex(normalize=True) == 0


def test_get_total_prize(oplib_root, graph_name):
    """Test total prize"""
    generation = Generation.gen1
    filepath = build_path_to_oplib_instance(oplib_root, generation, graph_name)
    problem = ProfitsProblem.load(filepath)
    assert problem.get_total_prize() == problem.number_of_nodes()


def test_get_quota(oplib_root, graph_name):
    """Test the quota is calculated properly"""
    generation = Generation.gen1
    filepath = build_path_to_oplib_instance(oplib_root, generation, graph_name)
    problem = ProfitsProblem.load(filepath)
    assert problem.get_quota(10) == int(0.1 * problem.number_of_nodes())
    assert problem.get_quota(50) == int(0.5 * problem.number_of_nodes())
    assert problem.get_quota(90) == int(0.9 * problem.number_of_nodes())
    assert problem.get_quota(100) == int(1.0 * problem.number_of_nodes())
    assert problem.get_quota(0) == int(0.0 * problem.number_of_nodes())
    with pytest.raises(ValueError):
        problem.get_quota(-1)
    with pytest.raises(ValueError):
        problem.get_quota(101)


def test_is_pctsp_yes_instance(
    oplib_root,
    generation,
    graph_name,
):
    """Test a yes instance is correctly identified"""
    filepath = build_path_to_oplib_instance(oplib_root, generation, graph_name)
    problem = ProfitsProblem.load(filepath)
    graph = problem.get_graph(normalize=True)
    quota = problem.get_quota(100)
    root = problem.get_root_vertex(True)
    edge_list = []
    num_nodes = graph.number_of_nodes()
    for i in range(num_nodes):
        edge_list.append((i, (i + 1) % num_nodes))
    assert is_pctsp_yes_instance(graph, quota, root, edge_list)
