"""Functions for creating a sparse graph from a complete graph"""

from copy import deepcopy
import random
import networkx as nx


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
