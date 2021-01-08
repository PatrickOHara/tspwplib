"""Convert graph vertices to pandas dataframe"""

import networkx as nx
import pandas as pd


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
