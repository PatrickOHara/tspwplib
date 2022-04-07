"""Tests for creating metric and non-metric cost functions"""

import networkx as nx
import pytest
from tspwplib import build_path_to_oplib_instance, metricness, mst_cost, ProfitsProblem
from tspwplib.metric import semi_mst_cost


def test_mst_cost(oplib_root, generation, graph_name):
    """Test MST cost"""
    filepath = build_path_to_oplib_instance(oplib_root, generation, graph_name)
    problem = ProfitsProblem.load(filepath)
    G = problem.get_graph()
    new_cost = mst_cost(G, cost_attr="cost")
    T = nx.minimum_spanning_tree(G, weight="cost")

    for (u, v), cost in nx.get_edge_attributes(G, "cost").items():
        if u == v:
            assert cost == 0
        elif T.has_edge(u, v):
            assert new_cost[(u, v)] == cost
        else:
            assert new_cost[(u, v)] == cost + nx.shortest_path_length(
                T, u, v, weight="cost"
            )


def test_semi_mst_cost(oplib_root, generation, graph_name):
    """Test Semi MST cost"""
    filepath = build_path_to_oplib_instance(oplib_root, generation, graph_name)
    problem = ProfitsProblem.load(filepath)
    G = problem.get_graph()
    new_cost = semi_mst_cost(G, cost_attr="cost")
    T = nx.minimum_spanning_tree(G, weight="cost")
    tree_cost = sum(nx.get_edge_attributes(T, "cost").values())
    upper_bound_cost = sum(mst_cost(G).values())
    assert tree_cost < sum(new_cost.values()) < upper_bound_cost


@pytest.mark.parametrize(
    "edges,expected_metricness",
    [
        ([(0, 1, 1), (1, 2, 1), (2, 0, 5)], 0),
        ([(0, 1, 1), (1, 2, 1), (2, 0, 1)], 1),
        ([(0, 1, 1), (1, 2, 1), (2, 0, 5), (2, 3, 1)], 0.0),
        (
            [
                (0, 1, 1),
                (1, 2, 1),
                (2, 0, 5),
                (2, 3, 1),
                (3, 4, 1),
                (4, 2, 1),
                (1, 3, 5),
            ],
            1.0 / 3.0,
        ),
        (
            [
                (0, 1, 10),
                (1, 2, 1),
                (2, 3, 1),
                (3, 4, 1),
                (1, 4, 1),
                (4, 5, 1),
                (0, 5, 1),
            ],
            0.5,
        ),
    ],
)
def test_metricness(edges, expected_metricness):
    """Test metricness"""
    G = nx.Graph()
    G.add_weighted_edges_from(edges, weight="cost")
    assert metricness(G) == expected_metricness
