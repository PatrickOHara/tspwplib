"""Functions for complete graphs"""

import networkx as nx


def is_complete(G: nx.Graph) -> bool:
    """Check if the graph is complete

    Args:
        G: Simple graph

    Returns:
        True if the graph is complete, false otherwise

    Note:
        Assumes no self loops
    """
    for u in G:
        for v in G:
            if not G.has_edge(u, v) and u != v:
                return False
    return True


def is_complete_with_self_loops(G: nx.Graph) -> bool:
    """Check if the graph is complete, and every vertex has a self loop

    Args:
        G: Simple graph

    Returns:
        True if the graph is complete, false otherwise
    """
    for u in G:
        if not G.has_edge(u, u):
            return False
    return is_complete(G)
