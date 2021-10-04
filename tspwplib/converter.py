"""Converting between different types of graphs"""


from copy import deepcopy
import math
from typing import Dict, List, Tuple
import networkx as nx
import pandas as pd
from .exception import UnexpectedSelfLoopException
from .types import EdgeFunctionName, Vertex, VertexFunctionName, VertexList


def to_vertex_dataframe(graph: nx.Graph) -> pd.DataFrame:
    """Convert graph vertices to pandas dataframe

    Args:
        graph: Input graph

    Returns:
        pandas dataframe with vertex set as index
    """
    vertex_data = list(map(lambda x: dict(vertex=x[0], **x[1]), graph.nodes(data=True)))
    vertex_df = pd.DataFrame(vertex_data)
    vertex_df = vertex_df.set_index("vertex")
    return vertex_df


def asymmetric_from_directed(G: nx.DiGraph) -> nx.DiGraph:
    """Create asymmetric directed graph from directed graph

    Split every node u two nodes u1 and u2.
    We add a directed arc between u1 and u2.
    Any previous inward edge v->u is now v->u1 and any outward edge from u is now u2->v.

    Args:
        G: Directed graph

    Returns:
        Directed asymmetric graph
    """
    asymmetric_graph = nx.DiGraph()
    nodes_for_adding: List[Tuple[Vertex, Dict]] = []
    edges_for_adding: List[Tuple[Vertex, Vertex, Dict]] = []
    # deepcopy when not a view
    asymmetric_graph.graph.update(deepcopy(G.graph))

    # find the id of the biggest vertex
    biggest_vertex = biggest_vertex_id_from_graph(G)

    for vertex, data in G.nodes(data=True):
        # split the vertex into two
        head = split_head(biggest_vertex, vertex)
        tail = split_tail(biggest_vertex, vertex)

        # the data is copied to both vertices
        tail_data = data.copy()
        head_data = data.copy()

        # split the value of the prize
        prize: int = data.get(VertexFunctionName.prize, 0)
        tail_data[VertexFunctionName.prize] = tail_prize(prize)
        head_data[VertexFunctionName.prize] = head_prize(prize)

        # add vertex to asymmetric graph with new data
        nodes_for_adding.append((head, head_data))
        nodes_for_adding.append((tail, tail_data))

        # add zero-cost edge from tail to head
        edge = (tail, head, {EdgeFunctionName.cost.value: 0})
        edges_for_adding.append(edge)

    for u, v, edge_data in G.edges(data=True):
        # add edge from head of u to tail of v with data
        u_head = split_head(biggest_vertex, u)
        v_tail = split_tail(biggest_vertex, v)
        edge_uv = (u_head, v_tail, edge_data)
        edges_for_adding.append(edge_uv)

    # add nodes and edges then return graph
    asymmetric_graph.add_nodes_from(nodes_for_adding)
    asymmetric_graph.add_edges_from(edges_for_adding)
    return asymmetric_graph


def asymmetric_from_undirected(G: nx.Graph) -> nx.DiGraph:
    """Create asymmetric directed graph from undirected graph

    Args:
        G: Undirected graph

    Returns:
        Directed asymmetric graph
    """
    directed_graph = G.to_directed()
    return asymmetric_from_directed(directed_graph)


def biggest_vertex_id_from_graph(G: nx.Graph) -> Vertex:
    """Return the vertex with the largest integer id

    Args:
        G: Graph

    Returns:
        Vertex with biggest id
    """
    return max(G)


def get_original_from_split_vertex(
    biggest_vertex: Vertex, split_vertex: Vertex
) -> Vertex:
    """Return the original vertex id given a split vertex (may be head or tail)

    Args:
        biggest_vertex: The vertex with the biggest id in the original graph
        split_vertex: A split vertex in asymmetric graph

    Returns:
        ID of the vertex in the original graph
    """
    if is_vertex_split_head(biggest_vertex, split_vertex):
        return split_vertex - 2 * (biggest_vertex + 1)
    # else split tail
    return split_vertex - biggest_vertex - 1


def get_original_path_from_split_path(
    biggest_vertex: Vertex, split_path: VertexList
) -> VertexList:
    """Get the path in the original graph given a path of split vertices in the asymmetric graph

    Args:
        biggest_vertex: The vertex with the biggest id in the original graph
        split_path: A path of split vertices in the asymmetric directed graph

    Returns:
        A path of vertices in the original graph
    """
    original_path = []
    previous_vertex = -1
    for split_vertex in split_path:
        original_vertex = get_original_from_split_vertex(biggest_vertex, split_vertex)
        if is_vertex_split_tail(biggest_vertex, split_vertex):
            original_path.append(original_vertex)
        elif (
            is_vertex_split_head(biggest_vertex, split_vertex)
            and previous_vertex != original_vertex
        ):
            original_path.append(original_vertex)
        previous_vertex = original_vertex
    return original_path


def is_split_vertex_pair(biggest_vertex: Vertex, tail: Vertex, head: Vertex) -> bool:
    """Does the arc (tail, head) represent a split vertex in the original graph?

    Args:
        biggest_vertex: The vertex with the biggest id in the original graph
        tail: Tail of edge in directed graph
        head: Head of edge in directed graph

    Returns:
        True if the arc (tail, head) represents a split vertex in the original graph
    """
    return (
        head - tail == biggest_vertex + 1
        and is_vertex_split_head(biggest_vertex, head)
        and is_vertex_split_tail(biggest_vertex, tail)
    )


def is_vertex_split_tail(biggest_vertex: Vertex, vertex: Vertex) -> bool:
    """Is the vertex a tail in the asymmetric graph?

    Args:
        biggest_vertex: The vertex with the biggest id in the original graph
        vertex: A potential tail of an edge in directed graph

    Returns:
        True if the vertex is a tail
    """
    return biggest_vertex + 1 <= vertex < 2 * (biggest_vertex + 1)


def is_vertex_split_head(biggest_vertex: Vertex, split_vertex: Vertex) -> bool:
    """Is the vertex a head in the asymmetric graph?

    Args:
        biggest_vertex: The vertex with the biggest id in the original graph
        split_vertex: A potential head of an edge in directed graph

    Returns:
        True if the vertex is a head
    """
    return 2 * (biggest_vertex + 1) <= split_vertex < 3 * (biggest_vertex + 1)


def split_head(biggest_vertex: Vertex, original_vertex: Vertex) -> Vertex:
    """Get the split head of the vertex

    Args:
        biggest_vertex: The vertex with the biggest id in the original graph
        original_vertex: Vertex in the original graph

    Returns:
        New split vertex that is a head of all arcs in the asymmetric graph
    """
    return 2 * (biggest_vertex + 1) + original_vertex


def split_tail(biggest_vertex: Vertex, original_vertex: Vertex) -> Vertex:
    """Get the split tail of the vertex

    Args:
        biggest_vertex: The vertex with the biggest id in the original graph
        original_vertex: Vertex in the original graph

    Returns:
        New split vertex that is a tail of all arcs in the asymmetric graph
    """
    return biggest_vertex + 1 + original_vertex


def head_prize(prize: int) -> int:
    """Get the prize of the split head

    Args:
        prize: The prize of a vertex

    Returns
        Split head prize
    """
    if prize % 2 == 1:
        return math.ceil(prize / 2.0)
    return int(prize / 2)


def tail_prize(prize: int) -> int:
    """Get the prize of the split tail

    Args:
        prize: The prize of a vertex

    Returns
        Split tail prize
    """
    return math.floor(prize / 2.0)


def new_dummy_vertex(vertex: int, key: int, biggest: int) -> int:
    """New dummy vertex ID

    Args:
        vertex: Vertex ID
        key: Edge key
        biggest: Biggest vertex ID

    Returns:
        ID of a new negative dummy vertex if key is greater than one.
        Otherwise return the same vertex ID as the input.
    """
    if key > 0:
        return -((biggest + 1) * (key - 1)) - vertex - 1
    return vertex


def old_vertex_from_dummy(dummy: int, key: int, biggest) -> int:
    """Old vertex ID from the dummy vertex ID"""
    if dummy < 0:
        return -(dummy + (biggest + 1) * (key - 1) + 1)
    return dummy


def to_simple_undirected(G: nx.MultiGraph) -> nx.Graph:
    """Given an undirected multigraph, multi edges to create a simple undirected graph.

    Args:
        G: Undirected networkx multi graph.

    Returns:
        Undirected networkx simple graph with no multi edges.

    Notes:
        Assumes the vertex ids are integers.
    """
    if not isinstance(G, nx.MultiGraph) and isinstance(G, nx.Graph):
        return G
    if isinstance(G, nx.DiGraph):
        raise TypeError("Directed graphs are not valid for this method")
    simple_graph = nx.Graph()

    # copy graph attributes to new graph
    for key, value in simple_graph.graph.items():
        simple_graph.graph[key] = value

    # copy vertex attributes
    for v, data in G.nodes(data=True):
        simple_graph.add_node(v, **data)

    biggest = biggest_vertex_id_from_graph(G)

    for u, v, k, data in G.edges.data(keys=True):
        if u == v and k > 0:
            message = "Self loop found with key greater than zero: "
            message += "implies there is more than one self loop on this vertex."
            raise UnexpectedSelfLoopException(message)

        # the first multi edge - add all data to new graph edge
        if k == 0:
            simple_graph.add_edge(u, v, **data)

        # multi edge - create new vertex for the source if it does not yet exist
        elif k > 0:
            vertex_data = G.nodes[u]
            dummy = new_dummy_vertex(u, k, biggest)
            simple_graph.add_node(dummy, **vertex_data)
            simple_graph.add_edge(u, dummy, **data)
            simple_graph.add_edge(dummy, v, **data)
        else:
            raise ValueError("Negative key for edge.")

    return simple_graph
