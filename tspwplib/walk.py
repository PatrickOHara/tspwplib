"""Functions for walks in a graph"""

from typing import Mapping

import graph_tool as gt
import networkx as nx
from .types import Edge, EdgeFunctionName, EdgeList, Vertex, VertexList


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


def total_prize(prizes: Mapping[Vertex, int], vertices: VertexList) -> int:
    """Total prize of vertices

    Args:
        prizes: A mapping from vertices to prizes, e.g. dict, property map
        vertices: List of vertices in the prizes map

    Returns:
        Total prize of vertices
    """
    sum_prize: int = 0
    for vertex in vertices:
        sum_prize += prizes[vertex]
    return sum_prize


def total_cost(costs: Mapping[Edge, int], edges: EdgeList) -> int:
    """Total cost of edges

    Args:
        costs: Mapping from edges to costs
        edges: List of edges

    Returns:
        Total cost of edges
    """
    sum_cost: int = 0
    for edge in edges:
        try:
            sum_cost += costs[edge]
        except KeyError:
            try:
                u, v = edge
                sum_cost += costs[(v, u)]
            except KeyError as second_key_error:
                raise KeyError(
                    "Edge ({u},{v}) or ({v},{u}) do not exist in costs map".format(
                        u=u, v=v
                    )
                ) from second_key_error
        except Exception as error:
            raise KeyError(
                "{edge} does not exist in cost map".format(edge=edge)
            ) from error
    return sum_cost


def total_cost_graph_tool(graph: gt.Graph, walk: VertexList) -> int:
    """Get the total cost of edges in a walk of the graph-tool graph

    Args:
        graph: Undirected input graph
        walk: A sequence of adjacent vertices

    Returns:
        Total cost of edges in walk
    """
    edges_in_tour = edge_list_from_walk(walk)
    gt_edges = [graph.edge(*e) for e in edges_in_tour]
    return total_cost(graph.ep.cost, gt_edges)


def total_cost_networkx(graph: nx.Graph, walk: VertexList) -> int:
    """Get the total cost of edges in a walk of the networkx graph

    Args:
        graph: Undirected input graph with cost attribute
        walk: A sequence of adjacent vertices

    Returns:
        Total cost of edges in the walk
    """
    edges_in_tour = edge_list_from_walk(walk)
    cost_attr = nx.get_edge_attributes(graph, EdgeFunctionName.cost.value)
    return total_cost(cost_attr, edges_in_tour)
