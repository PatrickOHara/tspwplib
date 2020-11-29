"""Functions for creating and measuring the sparsity of graphs.

To calculate the k-degeneracy of a graph you can use networkx:
```python
degeneracy(G) = max(networkx.core_number(G).values())
```
"""

from typing import Dict
import networkx as nx

def remove_gamma_edges_from_graph(G: nx.Graph, gamma: float) -> nx.Graph:
    """Remove edges from the graph to make it more sparse

    Args:
        G: Complete graph
        gamma: Fraction of edges to remove

    Returns:
        New graph with edge removed
    """

def measure_sparsity_metrics(G: nx.Graph) -> Dict[str, float]:
    """Calculate metrics for how sparse a graph is"""
    return dict(
        degeneracy=max(nx.core_number(G).values()),
        degree_ratio=sum(nx.degree(G).values()) / (2 * G.number_of_edges())
    )
