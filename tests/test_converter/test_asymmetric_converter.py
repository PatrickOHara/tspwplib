"""Test converting asymmetric graphs to / from directed & undirected graphs"""

import pytest
import networkx as nx
from tspwplib import EdgeFunctionName, VertexFunctionName
from tspwplib.converter import (
    asymmetric_from_directed,
    asymmetric_from_undirected,
    biggest_vertex_id_from_graph,
    get_original_from_split_vertex,
    get_original_path_from_split_path,
    head_prize,
    is_split_vertex_pair,
    is_vertex_split_head,
    is_vertex_split_tail,
    split_head,
    split_tail,
    tail_prize,
)


def original_and_asymmetric_comparison(
    original_graph: nx.Graph, asymmetric_graph: nx.DiGraph
) -> None:
    """Compare original and asymmetric graph"""
    biggest_vertex = biggest_vertex_id_from_graph(original_graph)
    for vertex, vertex_data in original_graph.nodes(data=True):
        head = split_head(biggest_vertex, vertex)
        tail = split_tail(biggest_vertex, vertex)
        assert asymmetric_graph.has_node(head)
        assert asymmetric_graph.has_node(tail)
        assert asymmetric_graph.has_edge(tail, head)
        assert len(list(asymmetric_graph.predecessors(head))) == 1
        assert len(list(asymmetric_graph.successors(tail))) == 1
        # check node data
        head_data = asymmetric_graph.nodes(data=True)[head]
        tail_data = asymmetric_graph.nodes(data=True)[tail]
        assert vertex_data.keys() == head_data.keys()
        assert vertex_data.keys() == tail_data.keys()
        assert (
            vertex_data[VertexFunctionName.prize]
            == head_data[VertexFunctionName.prize] + tail_data[VertexFunctionName.prize]
        )
        # check edge data
        edge_data = asymmetric_graph[tail][head]
        assert edge_data[EdgeFunctionName.cost] == 0

    for u, v, original_edge_data in original_graph.edges(data=True):
        head_of_u = split_head(biggest_vertex, u)
        tail_of_v = split_tail(biggest_vertex, v)
        assert asymmetric_graph.has_edge(head_of_u, tail_of_v)
        # check edge data
        edge_data = asymmetric_graph[head_of_u][tail_of_v]
        for key, value in original_edge_data.items():
            assert key in edge_data
            assert edge_data[key] == value


def test_asymmetric_from_directed(directed_complete_graph):
    """Test asymmetric graphs can be created from directed graphs"""
    asymmetric_graph = asymmetric_from_directed(directed_complete_graph)
    original_and_asymmetric_comparison(directed_complete_graph, asymmetric_graph)
    assert nx.is_strongly_connected(asymmetric_graph)


def test_asymmetric_from_undirected(undirected_complete_graph):
    """Test asymmetric graphs can be created from undirected graphs"""
    asymmetric_graph = asymmetric_from_undirected(undirected_complete_graph)
    original_and_asymmetric_comparison(undirected_complete_graph, asymmetric_graph)
    assert nx.is_strongly_connected(asymmetric_graph)


def test_biggest_vertex_id_from_graph(undirected_complete_graph):
    """Test the biggest vertex id is returned"""
    for u in undirected_complete_graph:
        assert u <= biggest_vertex_id_from_graph(undirected_complete_graph)


def test_get_original_from_split_vertex(
    original_vertices, split_head_vertices, split_tail_vertices
):
    """Test we can return the original vertex"""
    biggest_vertex = max(original_vertices)
    for i, original in enumerate(original_vertices):
        assert original == get_original_from_split_vertex(
            biggest_vertex, split_head_vertices[i]
        )
        assert original == get_original_from_split_vertex(
            biggest_vertex, split_tail_vertices[i]
        )


@pytest.mark.parametrize(
    "split_path,original_path",
    [
        ([3, 6, 4, 7, 5, 8], [0, 1, 2]),
        ([6, 4, 7, 5], [0, 1, 2]),
        ([], []),
        ([8, 3], [2, 0]),
        ([5, 8, 3, 6, 5], [2, 0, 2]),
    ],
)
def test_get_original_path_from_split_path(
    original_vertices,
    split_path,
    original_path,
):
    """Test we get the path from the original graph given split path"""
    biggest_vertex = max(original_vertices)
    assert original_path == get_original_path_from_split_path(
        biggest_vertex, split_path
    )


def test_is_split_vertex_pair(
    original_vertices, split_head_vertices, split_tail_vertices
):
    """Test if a pair of split vertices are a pair"""
    biggest_vertex = max(original_vertices)
    for original, head, tail in zip(
        original_vertices, split_head_vertices, split_tail_vertices
    ):
        assert is_split_vertex_pair(biggest_vertex, tail, head)
        assert not is_split_vertex_pair(biggest_vertex, tail, original)


def test_is_vertex_split_head(
    original_vertices, split_head_vertices, split_tail_vertices
):
    """Test split vertices are correctly identified as heads"""
    biggest_vertex = max(original_vertices)
    for original, head, tail in zip(
        original_vertices, split_head_vertices, split_tail_vertices
    ):
        assert is_vertex_split_head(biggest_vertex, head)
        assert not is_vertex_split_head(biggest_vertex, original)
        assert not is_vertex_split_head(biggest_vertex, tail)


def test_is_vertex_split_tail(
    original_vertices, split_head_vertices, split_tail_vertices
):
    """Test split vertices are correctly identfied as tails"""
    biggest_vertex = max(original_vertices)
    for original, head, tail in zip(
        original_vertices, split_head_vertices, split_tail_vertices
    ):
        assert not is_vertex_split_tail(biggest_vertex, head)
        assert not is_vertex_split_tail(biggest_vertex, original)
        assert is_vertex_split_tail(biggest_vertex, tail)


def test_split_head(original_vertices, split_head_vertices):
    """Test we split head correctly"""
    biggest_vertex = max(original_vertices)
    for original, head in zip(original_vertices, split_head_vertices):
        assert split_head(biggest_vertex, original) == head


def test_split_tail(original_vertices, split_tail_vertices):
    """Test we split tails correctly"""
    biggest_vertex = max(original_vertices)
    for original, tail in zip(original_vertices, split_tail_vertices):
        assert split_tail(biggest_vertex, original) == tail


@pytest.mark.parametrize("prize, prize_of_tail", [(8, 4), (7, 3), (0, 0)])
def test_tail_prize(prize, prize_of_tail):
    """Test prizes of tail are split correctly"""
    assert isinstance(tail_prize(prize), int)
    assert tail_prize(prize) == prize_of_tail


@pytest.mark.parametrize("prize, prize_of_head", [(8, 4), (7, 4), (0, 0)])
def test_head_prize(prize, prize_of_head):
    """Test prizes of head are split correctly"""
    assert isinstance(head_prize(prize), int)
    assert head_prize(prize) == prize_of_head
