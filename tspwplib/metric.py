"""Function for metric and non-metric cost functions"""

import random
import networkx as nx
import numpy as np
from .exception import NoTreesException, NotConnectedException
from .types import SimpleEdgeList, SimpleEdgeFunction


def metricness(graph: nx.Graph, cost_attr: str = "cost") -> float:
    """Measures how metric a cost function is

    Args:
        graph: Must be undirected, connected and not a tree
        cost_attr: Name of cost attribute

    Returns:
        If a cost function is metric, return 1.0.
        If n-1 edges are metric and the remaining edges are non-metric, return 0.0.

    Raises:
        NotConnectedException: If the graph is not connected
        NoTreesException: If the graph is a tree

    Notes:
        Self loops are ignored from the metricness
    """
    if not nx.is_connected(graph):
        raise NotConnectedException("Make sure your graph is connected")
    if nx.is_tree(graph):
        raise NoTreesException("Make sure your graph is not a tree")
    path_cost = dict(nx.all_pairs_bellman_ford_path_length(graph, weight=cost_attr))
    num_metric = 0
    num_non_metric = 0
    num_self_loops = 0
    for (u, v), cost in nx.get_edge_attributes(graph, cost_attr).items():
        if u == v:
            num_self_loops += 1
        elif cost <= path_cost[u][v]:
            num_metric += 1
        else:
            num_non_metric += 1
    print(num_metric, "metric edges and", num_non_metric, "non metric edges")
    numerator = (float)(num_metric - graph.number_of_nodes() + 1)
    denominator = (float)(
        graph.number_of_edges() - graph.number_of_nodes() - num_self_loops + 1
    )
    return numerator / denominator


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


def semi_mst_cost(
    G: nx.Graph, cost_attr: str = "cost", seed: int = 0
) -> SimpleEdgeFunction:
    """Half of the non-MST-tree edges are left unchanged.
    The other half are assigned cost as described in mst_cost.

    The half of edges are chosen with uniform and independent probability.

    Args:
        G: Undirected, simple graph
        cost_attr: Name of the cost attribute of edges
        seed: Set the seed of the random number generator

    Returns
        A new cost function
    """
    # find the cost of the minimum spanning tree in G
    T = nx.minimum_spanning_tree(G, weight=cost_attr)
    tree_cost = dict(nx.all_pairs_bellman_ford_path_length(T, weight=cost_attr))

    # get edges not in the tree
    non_tree_edges = [(u, v) for u, v in G.edges() if not T.has_edge(u, v)]
    num_non_tree_edges = len(non_tree_edges)

    gen = np.random.default_rng(seed=seed)
    donot_change_edge_cost = set()
    while len(non_tree_edges) >= float(num_non_tree_edges) * 0.5:
        index = gen.integers(0, len(non_tree_edges) - 1)  # get random index
        donot_change_edge_cost.add(
            non_tree_edges.pop(index)
        )  # remove item at random index, add to set

    # set the cost of the new edges
    new_cost: SimpleEdgeFunction = {}
    for (u, v), cost in nx.get_edge_attributes(G, cost_attr).items():
        if (
            T.has_edge(u, v)
            or (u, v) in donot_change_edge_cost
            or (v, u) in donot_change_edge_cost
        ):
            new_cost[(u, v)] = cost
        else:
            new_cost[(u, v)] = cost + tree_cost[u][v]
    return new_cost
