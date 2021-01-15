"""Fixtures for testing"""

import graph_tool as gt
import networkx as nx
import pytest
from tspwplib import EdgeFunctionName, VertexFunctionName, VertexList

# pylint: disable=redefined-outer-name


@pytest.fixture(scope="function", params=[[], [0], [0, 1, 3, 1, 2]])
def open_walk(request) -> VertexList:
    """Open walk that may repeat vertices"""
    return request.param


@pytest.fixture(scope="function", params=[[], [0], [0, 1, 3, 1, 0]])
def closed_walk(request) -> VertexList:
    """Walk that starts and ends at same vertex"""
    return request.param


@pytest.fixture(scope="function", params=[[0, 2, 1], [0, 4, 1]])
def not_a_walk(request) -> VertexList:
    """Not a walk"""
    return request.param


@pytest.fixture(scope="function", params=[[], [0], [0, 1, 3, 0]])
def simple_cycle(request) -> VertexList:
    """Simple cycle"""
    return request.param


@pytest.fixture(scope="function", params=[[], [0], [0, 1, 2]])
def simple_path(request) -> VertexList:
    """Simple path"""
    return request.param


@pytest.fixture(scope="function")
def walk_graph() -> nx.Graph:
    """Graph for testing walks"""
    return nx.Graph([(0, 1), (0, 3), (1, 2), (1, 3)])


@pytest.fixture(scope="function")
def weighted_walk_networkx_graph(walk_graph) -> nx.Graph:
    """Walk graph with cost on edges and prize on vertices"""
    for vertex in walk_graph:
        walk_graph.nodes[vertex][VertexFunctionName.prize] = vertex
    edge_attrs = dict()
    for u, v in walk_graph.edges():
        edge_attrs[(u, v)] = {EdgeFunctionName.cost.value: u + v}
    nx.set_edge_attributes(walk_graph, edge_attrs)
    return walk_graph


@pytest.fixture(scope="function")
def weighted_walk_graph_tool() -> gt.Graph:
    """Graph tool with prize and cost"""
    graph = gt.Graph(directed=False)
    graph.add_edge(0, 1)
    graph.add_edge(0, 3)
    graph.add_edge(1, 2)
    graph.add_edge(1, 3)
    cost = graph.new_edge_property("int")
    cost[graph.edge(0, 1)] = 1
    cost[graph.edge(0, 3)] = 3
    cost[graph.edge(1, 2)] = 3
    cost[graph.edge(1, 3)] = 4

    prize = graph.new_vertex_property("int")
    for i in range(graph.num_vertices()):
        prize[i] = i

    graph.ep.cost = cost
    graph.vp.prize = prize
    return graph
