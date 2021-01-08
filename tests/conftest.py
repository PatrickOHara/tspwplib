"""Fixtures for testing"""

import networkx as nx
import pytest
from tspwplib import VertexList


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
