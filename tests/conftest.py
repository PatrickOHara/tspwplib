"""Fixtures for testing"""

import os
from pathlib import Path
import networkx as nx
import pytest
from tspwplib import (
    EdgeFunctionName,
    Generation,
    GraphName,
    VertexFunctionName,
    VertexList,
)

# pylint: disable=redefined-outer-name


def pytest_addoption(parser):
    """Options for filepaths for pytest-tspwplib"""
    group = parser.getgroup("tspwplib")
    group.addoption(
        "--tsplib-root",
        default=os.getenv("TSPLIB_ROOT"),
        required=False,
        type=str,
        help="Filepath to tsplib95 directory",
    )
    group.addoption(
        "--oplib-root",
        default=os.getenv("OPLIB_ROOT"),
        required=False,
        type=str,
        help="Filepath to oplib directory",
    )


@pytest.fixture(scope="function")
def tsplib_root(request) -> Path:
    """Root of tsplib95 data"""
    return Path(request.config.getoption("--tsplib-root"))


@pytest.fixture(scope="function")
def oplib_root(request) -> Path:
    """Root of the cloned OP lib"""
    return Path(request.config.getoption("--oplib-root"))


@pytest.fixture(
    scope="function",
    params=[
        GraphName.eil76,
        GraphName.st70,
        GraphName.att48,
    ],
)
def graph_name(request) -> GraphName:
    """Loop through valid instance names"""
    return request.param


@pytest.fixture(
    scope="function",
    params=[
        Generation.gen1,
        Generation.gen2,
        Generation.gen3,
    ],
)
def generation(request) -> Generation:
    """Loop through valid generations"""
    # NOTE generation 4 has different alpha values
    return request.param


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
    edge_attrs = {}
    for u, v in walk_graph.edges():
        edge_attrs[(u, v)] = {EdgeFunctionName.cost.value: u + v}
    nx.set_edge_attributes(walk_graph, edge_attrs)
    return walk_graph
