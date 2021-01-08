"""Functions for walks in a graph"""

import networkx as nx
from .types import EdgeList, VertexList


def edge_list_from_walk(walk: VertexList) -> EdgeList:
    """Get ordered list of edges from an ordered list of vertices

    Args:
        walk: Ordered list of vertices that represent a walk in the graph

    Returns:
        List of edges in the same order as the walk
    """
    edge_list: EdgeList = []
    if len(walk) <= 1:
        return edge_list
    for i in range(len(walk) - 1):
        vertex = walk[i]
        next_vertex = walk[i + 1]
        edge_list.append((vertex, next_vertex))
    return edge_list


def is_walk(G: nx.Graph, walk: VertexList) -> bool:
    """Is the walk a sequence of adjacent vertices in the graph?

    Args:
        G: input graph
        walk: Ordered sequence of vertices

    Returns:
        True if all vertices are adjacent in the graph
    """
    edge_list = edge_list_from_walk(walk)
    return all([G.has_edge(u, v) for u, v in edge_list])


def is_simple_cycle(G: nx.Graph, cycle: VertexList) -> bool:
    """Is the cycle simple in the graph?

    Args:
        G: input graph
        cycle: Ordered sequence of vertices

    Returns:
        True if the cycle is simple in the graph
    """
    cycle_length = len(cycle)
    if cycle_length <= 1:
        return True
    return (
        is_walk(G, cycle)
        and cycle_length == len(set(cycle)) + 1
        and cycle[0] == cycle[cycle_length - 1]
    )


def is_simple_path(G: nx.Graph, path: VertexList) -> bool:
    """Is the path simple in the graph?

    Args:
        G: input graph
        path: Ordered sequence of vertices

    Returns:
        True if the path is simple in the graph
    """
    return is_walk(G, path) and len(path) == len(set(path))
