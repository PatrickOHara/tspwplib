"""Function for metric and non-metric cost functions"""

import random
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
