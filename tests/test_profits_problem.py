"""Test the TSP with Profits Problem class"""

import math
import networkx as nx
from tspwplib.problem import ProfitsProblem
from tspwplib.types import OptimalSolutionTSP
from tspwplib.utils import build_path_to_oplib_instance


def test_parse_profits_problem(oplib_root, generation, instance_name, alpha):
    """Test an OP instance can be parsed"""
    filepath = build_path_to_oplib_instance(
        oplib_root, generation, instance_name, alpha=alpha
    )
    assert "COST_LIMIT" in ProfitsProblem.fields_by_keyword

    problem = ProfitsProblem.load(filepath)
    assert problem.is_complete()
    graph = problem.get_graph()
    assert nx.complete_graph(graph)


def test_get_cost_limit(oplib_root, generation, instance_name, alpha):
    """Test we can get the cost limit"""
    filepath = build_path_to_oplib_instance(
        oplib_root, generation, instance_name, alpha=alpha
    )
    problem = ProfitsProblem.load(filepath)
    # total_cost = sum([problem.get_weight(source, target) for source, target in problem.get_edges()])

    expected_cost_limit = math.ceil(
        OptimalSolutionTSP[instance_name] * (alpha.value / 100.0)
    )
    assert problem.get_cost_limit() == expected_cost_limit
