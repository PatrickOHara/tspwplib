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
)


def test_parse_profits_problem(oplib_root, generation, graph_name, alpha):
    """Test an OP instance can be parsed"""
    filepath = build_path_to_oplib_instance(
        oplib_root, generation, graph_name, alpha=alpha
    )
    assert "COST_LIMIT" in ProfitsProblem.fields_by_keyword
    assert "NODE_SCORE_SECTION" in ProfitsProblem.fields_by_keyword

    problem = ProfitsProblem.load(filepath)
    assert problem.is_complete()


def test_get_cost_limit(oplib_root, generation, graph_name, alpha):
    """Test we can get the cost limit"""
    filepath = build_path_to_oplib_instance(
        oplib_root, generation, graph_name, alpha=alpha
    )
    problem = ProfitsProblem.load(filepath)
    expected_cost_limit = math.ceil(
        OptimalSolutionTSP[graph_name] * (alpha.value / 100.0)
    )
    assert problem.get_cost_limit() == expected_cost_limit


def test_get_node_score(oplib_root, generation, graph_name, alpha):
    """Test every node has a prize"""
    filepath = build_path_to_oplib_instance(
        oplib_root, generation, graph_name, alpha=alpha
    )
    problem = ProfitsProblem.load(filepath)
    node_scores = problem.get_node_score()
    assert isinstance(node_scores, dict)
    for vertex in problem.get_nodes():
        assert vertex in node_scores
        value = node_scores[vertex]
        assert value >= 0


def test_get_graph(oplib_root, generation, graph_name, alpha):
    """Test we can load a graph with prizes"""
    filepath = build_path_to_oplib_instance(
        oplib_root, generation, graph_name, alpha=alpha
    )
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
    valid_types = [str, int, float]
    for _, _, data in graph.edges(data=True):
        for _, value in data.items():
            assert type(value) in valid_types

    for _, data in graph.nodes(data=True):
        for _, value in data.items():
            assert type(value) in valid_types

    assert graph.graph["root"] == 1


def test_get_graph_tool(oplib_root, generation, graph_name, alpha):
    """Test returning graph tool undirected weighted graph"""
    filepath = build_path_to_oplib_instance(
        oplib_root, generation, graph_name, alpha=alpha
    )
    problem = ProfitsProblem.load(filepath)
    gt_graph = problem.get_graph_tool()
    nx_graph = problem.get_graph(normalize=True)
    assert nx_graph.has_node(0)
    assert 0 in gt_graph.get_vertices()
    assert gt_graph.num_vertices() == nx_graph.number_of_nodes()
    assert gt_graph.num_edges() == nx_graph.number_of_edges()

    # check cost
    for u, v, data in nx_graph.edges(data=True):
        gt_edge = gt_graph.edge(u, v, add_missing=False)
        assert gt_edge
        assert gt_graph.ep.cost[gt_edge] == data["cost"]
    # check prize on vertices
    for u, data in nx_graph.nodes(data=True):
        assert data["prize"] == gt_graph.vertex_properties.prize[u]


def test_get_root_vertex(oplib_root, generation, graph_name, alpha):
    """Test the root vertex is 1 when un-normalized (0 when normalized)"""
    filepath = build_path_to_oplib_instance(
        oplib_root, generation, graph_name, alpha=alpha
    )
    problem = ProfitsProblem.load(filepath)
    assert problem.get_root_vertex(normalize=False) == 1
    assert problem.get_root_vertex(normalize=True) == 0


def test_get_total_prize(oplib_root, graph_name, alpha):
    """Test total prize"""
    generation = Generation.gen1
    filepath = build_path_to_oplib_instance(
        oplib_root, generation, graph_name, alpha=alpha
    )
    problem = ProfitsProblem.load(filepath)
    assert problem.get_total_prize() == problem.number_of_nodes()


def test_get_quota(oplib_root, graph_name, alpha):
    """Test the quota is calculated properly"""
    generation = Generation.gen1
    filepath = build_path_to_oplib_instance(
        oplib_root, generation, graph_name, alpha=alpha
    )
    problem = ProfitsProblem.load(filepath)
    assert problem.get_quota(10) == int(0.1 * problem.number_of_nodes())
    assert problem.get_quota(50) == int(0.5 * problem.number_of_nodes())
    assert problem.get_quota(90) == int(0.9 * problem.number_of_nodes())
    assert problem.get_quota(100) == int(1.0 * problem.number_of_nodes())
    assert problem.get_quota(0) == int(0.0 * problem.number_of_nodes())
    with pytest.raises(ValueError):
        problem.get_quota(-1)
        problem.get_quota(101)
