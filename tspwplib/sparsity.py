"""Functions for creating and measuring the sparsity of graphs.

To calculate the k-degeneracy of a graph you can use networkx:
```python
degeneracy(G) = max(networkx.core_number(G).values())
```
"""

import random
from typing import Dict
import networkx as nx


def remove_random_edges_from_graph(
    G: nx.Graph, edge_removal_probability: float = 0.5
) -> nx.Graph:
    """Remove edges from the graph to make it more sparse.
    Edges are removed randomly with uniform and indepedent probability.

    Args:
        G: Complete graph
        edge_removal_probability: Probability of removing an edge from G

    Returns:
        New graph with edge removed
    """
    # make copy of graph to avoid editing original copy
    H = G.copy()

    # for each edge in G, remove in H if random number if less than edge removal prob
    for u, v in G.edges():
        if random.random() < edge_removal_probability:
            H.remove_edge(u, v)
    return H


def measure_sparsity_metrics(G: nx.Graph) -> Dict[str, float]:
    """Calculate metrics for how sparse a graph is"""
    return dict(
        degeneracy=max(nx.core_number(G).values()),
        degree_ratio=sum(nx.degree(G).values()) / (2 * G.number_of_edges()),
    )
