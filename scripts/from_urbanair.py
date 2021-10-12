import json
from pathlib import Path

import networkx as nx
import pandas as pd
import tsplib95
import typer

from tspwplib import split_graph_from_properties
from tspwplib.problem import BaseTSP
from tspwplib.types import EdgeWeightFormat, LondonaqLocation, LondonaqTimestamp


def choose_root(G):
    # choose the root vertex
    root = None
    root_found = False

    for vertex in G.nodes():
        if not root_found and G.degree(vertex) > 2:
            root_found = True
            root = vertex
        else:
            root
    return root


OLD_EDGE_LOOKUP_JSON = "old_edge_lookup.json"
OLD_NODE_LOOKUP_JSON = "old_node_lookup.json"


def generate_londonaq_dataset(
    dataset_dir: Path,
    location_id: LondonaqLocation,
    timestamp_id: LondonaqTimestamp,
    edges_csv_filename: str = "edges.csv",
    nodes_csv_filename: str = "nodes.csv",
    old_edge_lookup: str = OLD_EDGE_LOOKUP_JSON,
    old_node_lookup: str = OLD_NODE_LOOKUP_JSON,
) -> BaseTSP:
    """Generate a londonaq dataset"""
    # get the CSV files for edges and nodes
    dataset_dir.mkdir(parents=False, exist_ok=True)
    edges_filepath = dataset_dir / edges_csv_filename
    nodes_filepath = dataset_dir / nodes_csv_filename
    if not edges_filepath.exists():
        raise FileNotFoundError(edges_filepath)
    if not nodes_filepath.exists():
        raise FileNotFoundError(nodes_filepath)
    nodes_df = pd.read_csv(nodes_filepath)
    edges_df = pd.read_csv(edges_filepath)

    # split edges then relabel the nodes
    edges_df = edges_df.set_index(["source", "target", "key"])
    edge_attrs = edges_df.to_dict("index")
    split_graph = split_graph_from_properties(edge_attrs)
    normalize_map = {node: i for i, node in enumerate(split_graph.nodes())}
    normalized_graph = nx.relabel_nodes(split_graph, normalize_map, copy=True)

    # save the node and edge mappings to a json file
    old_edge_lookup = {
        (normalize_map[u], normalize_map[v]): data["old_edge"]
        for u, v, data in split_graph.edges(data=True)
    }
    old_vertex_lookup = {new: old for old, new in normalize_map.items()}
    with open(dataset_dir / old_edge_lookup, "w", encoding="UTF-8") as f:
        json.dump(old_edge_lookup, f)
    with open(dataset_dir / old_node_lookup, "w", encoding="UTF-8") as f:
        json.dump(old_vertex_lookup, f)

    # TODO get root vertex
    root = 0

    # TODO get node co-ordinates

    # get TSP representation

    # save to txt file


def to_pandas_nodelist(G: nx.Graph) -> pd.DataFrame:
    """Move node attributes to a pandas dataframe. Node ID is stored in 'node' column."""
    return pd.DataFrame([{"node": node, **data} for node, data in G.nodes(data=True)])


def main():
    dataset_dir = Path("/", "Users", "patrick", "Datasets", "pctsp", "londonaq")

    root_vertex = choose_root(normalized_graph)
    nx.set_node_attributes(normalized_graph, False, "is_depot")
    normalized_graph.nodes[root_vertex]["is_depot"] = True

    ndf = to_pandas_nodelist(normalized_graph)
    ndf = ndf.rename(columns={"prize": "demand"})
    ndf["demand"] = ndf["demand"].apply(lambda x: int(round(x)))
    edf = nx.to_pandas_edgelist(normalized_graph)
    edf = edf.rename(columns={"cost": "weight"})
    edf["weight"] = edf["weight"].apply(lambda x: int(round(x)))

    name = "londonaq_tiny"
    comment = "Prize-collecting TSP on air quality dataset in London."
    problem_type = "PCTSP"
    problem = BaseTSP.from_dataframes(
        name,
        comment,
        problem_type,
        edf,
        ndf,
        edge_weight_format=EdgeWeightFormat.LOWER_DIAG_ROW,
    )
    graph = problem.get_graph()

    tsplib = problem.to_tsplib95()
    tsplib.save("test.txt")
    loaded_tsplib = tsplib95.models.StandardProblem.load("test.txt")


if __name__ == "__main__":
    typer.run(main)
