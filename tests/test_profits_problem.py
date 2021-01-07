"""Test the TSP with Profits Problem class"""

import math
import networkx as nx
from tspwplib.problem import ProfitsProblem
from tspwplib.types import EdgeFunctionName, OptimalSolutionTSP, VertexFunctionName
from tspwplib.utils import build_path_to_oplib_instance


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

    # check every edge has an attribute called 'weight'
    for _, _, data in graph.edges(data=True):
        assert EdgeFunctionName.weight in data
