"""Fixtures for testing converting graphs"""

import networkx as nx
import pytest
from tspwplib import EdgeFunctionName, VertexFunctionName, VertexList


@pytest.fixture(scope="function", params=[3, 5, 10])
def undirected_complete_graph(request) -> nx.Graph:
    """Undirected complete graph on 3, 5 & 10 vertices"""
    graph = nx.complete_graph(request.param)
    nx.set_node_attributes(graph, 1, name=VertexFunctionName.prize)
    nx.set_edge_attributes(graph, 1, name=EdgeFunctionName.cost)
    return graph


@pytest.fixture(scope="function", params=[3, 5, 10])
def directed_complete_graph(request) -> nx.DiGraph:
    """Undirected complete graph on 3, 5 & 10 vertices"""
    graph = nx.complete_graph(request.param, nx.DiGraph())
    nx.set_node_attributes(graph, 1, name=VertexFunctionName.prize)
    nx.set_edge_attributes(graph, 1, name=EdgeFunctionName.cost)
    return graph


@pytest.fixture(scope="function")
def original_vertices() -> VertexList:
    """List of vertices in the original graph"""
    return list(range(3))


@pytest.fixture(scope="function")
def split_head_vertices() -> VertexList:
    """Split head vertices"""
    return list(range(6, 9))


@pytest.fixture(scope="function")
def split_tail_vertices() -> VertexList:
    """Split tail vertices"""
    return list(range(3, 6))


@pytest.fixture(scope="function")
def split_vertices() -> VertexList:
    """List of vertices in asymmetric graph"""
    return list(range(3, 9))
