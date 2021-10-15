"""Functions for walks in a graph"""

import itertools
from typing import Dict, Iterable, Mapping, Set

import networkx as nx
from .exception import EdgesNotAdjacentException, NotSimpleException
from .types import (
    EdgeFunction,
    EdgeFunctionName,
    EdgeList,
    Vertex,
    VertexList,
    VertexLookup,
)


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


def vertex_set_from_edge_list(edge_list: EdgeList) -> Set[Vertex]:
    """Get a set of vertices from a list of edges

    Args:
        edge_list: List of edges

    Returns:
        Set of vertices in the edge list
    """
    return set(itertools.chain.from_iterable(edge_list))


def __add_vertex_to_occurence(
    first_occurence: Dict[Vertex, int],
    second_occurence: Dict[Vertex, int],
    vertex: Vertex,
    index: int,
) -> None:
    """Add vertex to either the first or second occurence lookup"""
    if vertex in first_occurence:
        second_occurence[vertex] = index
    elif vertex not in first_occurence:
        first_occurence[vertex] = index
    else:
        message = f"Vertex {vertex} appears in more than two edges. Walk is not simple."
        raise NotSimpleException(message)


def order_edge_list(unordered_edges: EdgeList) -> EdgeList:
    """Given a list of unordered edges, return an ordered edge list
    such that every two adjacent edge in the list are also adjacent in
    the input graph.

    Note that the list of edges should form a simple path or cycle.

    Args:
        unordered_edges: List of unique edges in no particular order

    Returns:
        List of unique edges that are adjacent in the graph

    Raises:
        NotSimpleException: If the list of edges is not a simple path or cycle
    """
    # create a lookup table of the first and second occurence of each vertex in the edge list
    first_occurence: VertexLookup = {}
    second_occurence: VertexLookup = {}
    for i, edge in enumerate(unordered_edges):
        __add_vertex_to_occurence(first_occurence, second_occurence, edge[0], i)
        __add_vertex_to_occurence(first_occurence, second_occurence, edge[1], i)

    # use the lookup tables to place the edges in the correct order in the edge list
    ordered_edges = []
    j = 0
    target_index = -1
    found_source = False
    first_vertex = 0
    for i, edge in enumerate(unordered_edges):
        u = edge[0]
        v = edge[1]
        if not found_source and u not in second_occurence:
            j = i
            found_source = True
        elif found_source and u not in second_occurence:
            target_index = i
            break
        elif not found_source and v not in second_occurence:
            j = i
            found_source = True
            first_vertex = 1
        elif found_source and v not in second_occurence:
            target_index = i
            break
    prev = unordered_edges[j][first_vertex]
    visited = [False] * len(unordered_edges)

    for i in range(len(unordered_edges)):
        edge = unordered_edges[j]
        print(edge)
        if visited[j]:
            raise NotSimpleException()
        visited[j] = True
        u = edge[0]
        v = edge[1]
        ordered_edges.append(edge)
        if j == target_index:
            break

        # if u == prev then follow v
        if u == prev and j == first_occurence[v]:
            j = second_occurence[v]
            prev = v
        elif u == prev and j == second_occurence[v]:
            j = first_occurence[v]
            prev = v
        # if v == prev then follow u
        elif v == prev and j == first_occurence[u]:
            j = second_occurence[u]
            prev = u
        elif v == prev and j == second_occurence[u]:
            j = first_occurence[u]
            prev = u

    return ordered_edges


def reorder_edge_list_from_root(edge_list: EdgeList, root: Vertex) -> EdgeList:
    """Reorder a list of edges such that the root vertex is in the first (and last) edge

    Args:
        edge_list: List of unique, adjacent edges
        root: Root vertex

    Returns:
        List of edges. The first (and last) edge will contain the root vertex.

    Raises:
        nx.NodeNotFound: If the root vertex is not in any edges.
    """
    root_index = -1
    not_found = nx.NodeNotFound(f"Root vertex {root} not found in edge list")
    n = len(edge_list)
    if n == 0:
        raise not_found
    if n > 1 and root in edge_list[0] and root in edge_list[n - 1]:
        return edge_list
    for i in range(n):
        edge = edge_list[i]
        if root in edge:
            root_index = i
    if root_index == -1:
        raise not_found
    reordered_edges = edge_list[root_index:] + edge_list[:root_index]
    return reordered_edges


def walk_from_edge_list(edge_list: EdgeList) -> VertexList:
    """Get a walk from a list of unique, adjacent edges

    Args:
        edge_list: List of unique edges that are adjacent in the graph

    Returns:
        List of vertices in walk of edges

    Raises:
        EdgesNotAdjacentException: When two edges in the walk are not adjacent
    """
    walk: VertexList = []
    if len(edge_list) == 0:
        return walk

    first_edge = edge_list[0]
    if len(edge_list) == 1:
        walk.append(first_edge[0])
        walk.append(first_edge[1])
        return walk

    second_edge = edge_list[1]
    if first_edge[0] == second_edge[0] or first_edge[0] == second_edge[1]:
        current = first_edge[0]
        walk.append(first_edge[1])
    else:
        current = first_edge[1]
        walk.append(first_edge[0])

    for i in range(1, len(edge_list)):
        walk.append(current)
        edge = edge_list[i]
        u = edge[0]
        v = edge[1]
        if u == current:
            current = v
        elif v == current:
            current = u
        else:
            message = f"Edges in the edge list must be adjacent, but edge {u} - {v}"
            message += (
                f" is not adjacent to vertex {current} from previous edge in list."
            )
            raise EdgesNotAdjacentException(message)
    walk.append(current)
    return walk


def is_walk(G: nx.Graph, walk: VertexList) -> bool:
    """Is the walk a sequence of adjacent vertices in the graph?

    Args:
        G: input graph
        walk: Ordered sequence of vertices

    Returns:
        True if all vertices are adjacent in the graph
    """
    edge_list = edge_list_from_walk(walk)
    return all(G.has_edge(edge[0], edge[1]) for edge in edge_list)


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


def total_prize(prizes: Mapping[Vertex, int], vertices: Iterable[Vertex]) -> int:
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


def total_cost(costs: EdgeFunction, edges: EdgeList) -> int:
    """Total cost of edges

    Args:
        costs: Mapping from edges to costs
        edges: List of edges

    Returns:
        Total cost of edges
    """
    sum_cost = 0
    for edge in edges:
        try:
            sum_cost += costs[edge]
        except KeyError:
            try:
                u = edge[0]
                v = edge[1]
                sum_cost += costs[(v, u)]
            except KeyError as second_key_error:
                raise KeyError(
                    "Edge ({u},{v}) or ({v},{u}) do not exist in costs map".format(
                        u=u, v=v
                    )
                ) from second_key_error
        except Exception as error:
            raise KeyError(f"{edge} does not exist in cost map") from error
    return sum_cost


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


def remove_self_loops_from_edge_list(edge_list: EdgeList) -> EdgeList:
    """Return a new edge list with no self loops

    Args:
        edge_list: List of edges

    Returns:
        Edge list with no self loops
    """
    return [edge for edge in edge_list if edge[0] != edge[1]]
