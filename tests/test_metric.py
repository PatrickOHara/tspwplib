"""Tests for creating metric and non-metric cost functions"""

import networkx as nx
from tspwplib import build_path_to_oplib_instance, mst_cost, ProfitsProblem


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
