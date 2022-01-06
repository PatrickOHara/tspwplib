"""Functions for creating a sparse graph from a complete graph"""

from copy import deepcopy
import random
import networkx as nx
from .types import Vertex


def sparsify_uid(G: nx.Graph, kappa: int, seed: int = 0) -> nx.Graph:
    """Remove edges with uniform and independent (uid) probability until
    the number of edges equals kappa * number of nodes

    Args:
        G: Graph
        kappa: Parameter independent of the input size
        seed: Set the random seed

    Returns:
        Graph with kappa * V edges where V is the number of nodes

    Notes:
        A copy of the graph is made and returned. The original graph is unedited.
    """
    random.seed(seed)
    graph_copy = deepcopy(G)
    vertex_list = list(graph_copy.nodes())
    while graph_copy.number_of_edges() > graph_copy.number_of_nodes() * kappa:
        # choose vertex randomly
        u = random.choice(vertex_list)
        if graph_copy.degree(u) > 0:
            # choose a neighbor randomly
            v = random.choice(list(graph_copy.neighbors(u)))
            # remove edge
            graph_copy.remove_edge(u, v)
    return graph_copy


def total_cost_of_adjacent_edges(
    G: nx.Graph, u: Vertex, cost_attr: str = "cost"
) -> int:
    """Get the total cost of edges adjacent to a vertex u"""
    total = 0
    for v in G.neighbors(u):
        total += G.get_edge_data(u, v)[cost_attr]
    return total


def sparsify_by_cost(
    G: nx.Graph, kappa: int, seed: int = 0, cost_attr: str = "cost"
) -> nx.Graph:
    """Given vertex i, remove an edge e=(i,j) with probability P[i,j]
    where the probability function is weighted according to the cost function:

    $P[i,j] = c(i,j) / C_i$

    where $C_i$ is the total cost of all edges adjacent to vertex i.

    Args:
        G: Graph
        kappa: Parameter independent of the input size
        seed: Set the random seed for reproducibility of graphs
        cost_attr: Name of the cost attribute on edges

    Returns:
        A deep copy of the original graph with edges removed
    """
    random.seed(seed)
    graph_copy = deepcopy(G)
    vertex_list = list(graph_copy.nodes())
    while graph_copy.number_of_edges() > graph_copy.number_of_nodes() * kappa:
        # choose vertex randomly
        u = random.choice(vertex_list)

        if graph_copy.degree(u) > 0:
            # draw a random number from uniform and independent distribution (UID)
            threshold = random.random()

            # the total cost of all adjacent edges is the denominator
            cost_of_edges = float(
                total_cost_of_adjacent_edges(graph_copy, u, cost_attr=cost_attr)
            )
            chosen_vertex = None

            if cost_of_edges == 0:
                chosen_vertex = random.choice(list(graph_copy.neighbors(u)))

            else:
                # iterate over neighbors to check if the edge has been selected
                probability_so_far = 0.0
                for v in graph_copy.neighbors(u):
                    # weight probability of choosing an edges by the cost
                    edge_prob = (
                        float(graph_copy.get_edge_data(u, v)[cost_attr]) / cost_of_edges
                    )
                    if probability_so_far + edge_prob >= threshold:
                        # edge found! break here
                        chosen_vertex = v
                        break
                    probability_so_far += edge_prob
            graph_copy.remove_edge(u, chosen_vertex)
    return graph_copy
