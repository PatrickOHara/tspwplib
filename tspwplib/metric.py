"""Function for metric and non-metric cost functions"""

import random
import networkx as nx
from .types import SimpleEdgeList, SimpleEdgeFunction


def uniform_random_cost(
    edge_list: SimpleEdgeList, min_value: int = 1, max_value: int = 100, seed: int = 0
) -> SimpleEdgeFunction:
    """Generate a cost function for each edge drawn from a uniform and independant probability

    Args:
        edge_list: List of edges in graph
        min_value: Minimum value the cost can take (inclusive)
        max_value: Maximum value the cost can take (inclusive)
        seed: Set the seed of the random number generator

    Returns:
        Edge cost function
    """
    cost: SimpleEdgeFunction = {}
    random.seed(seed)
    for u, v in edge_list:
        cost[(u, v)] = random.randint(min_value, max_value)
    return cost


def mst_cost(G: nx.Graph, cost_attr: str = "cost") -> SimpleEdgeFunction:
    """Find the minimum spanning tree of G.
    The cost of edges in the tree remains unchanged.
    The cost of edges not in the tree is equal to the cost of the minimum spanning tree
    plus the original cost of the edges.

    Args:
        G: Undirected, simple graph
        cost_attr: Name of the cost attribute of edges

    Returns
        A new cost function
    """
    # find the cost of the minimum spanning tree in G
    T = nx.minimum_spanning_tree(G, weight=cost_attr)
    tree_cost = dict(nx.all_pairs_bellman_ford_path_length(T, weight=cost_attr))

    # set the cost of the new edges
    new_cost: SimpleEdgeFunction = {}
    for (u, v), cost in nx.get_edge_attributes(G, cost_attr).items():
        if T.has_edge(u, v):
            new_cost[(u, v)] = cost
        else:
            new_cost[(u, v)] = cost + tree_cost[u][v]
    return new_cost
