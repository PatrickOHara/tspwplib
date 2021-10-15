"""Script for generating a tsplib style txt file from londonaq CSV"""

import json
from pathlib import Path

import networkx as nx
import pandas as pd
import typer

from tspwplib import split_graph_from_properties
from tspwplib.problem import BaseTSP
from tspwplib.types import (
    EdgeWeightFormat,
    LondonaqGraphName,
    LondonaqLocationShort,
    LondonaqTimestamp,
)
from tspwplib.utils import londonaq_comment, londonaq_graph_name

OLD_EDGE_LOOKUP_JSON = "old_edge_lookup.json"
OLD_NODE_LOOKUP_JSON = "old_node_lookup.json"


def generate_londonaq_dataset(
    dataset_dir: Path,
    name: LondonaqGraphName,
    comment: str,
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
    nodes_df = nodes_df.set_index("node")
    edges_df = pd.read_csv(edges_filepath)

    # split edges then relabel the nodes
    edges_df = edges_df.set_index(["source", "target", "key"])
    edge_attrs = edges_df.to_dict("index")
    split_graph = split_graph_from_properties(
        edge_attrs,
        edge_attr_to_split="cost",
        edge_attr_to_vertex="length",
        new_vertex_attr="demand",
        old_edge_attr="old_edge",
    )
    normalize_map = {node: i for i, node in enumerate(split_graph.nodes())}
    normalized_graph = nx.relabel_nodes(split_graph, normalize_map, copy=True)

    # save the node and edge mappings to a json file
    old_edges = {
        (normalize_map[u], normalize_map[v]): data["old_edge"]
        for u, v, data in split_graph.edges(data=True)
    }
    old_vertices = {new: old for old, new in normalize_map.items()}

    # convert tuples to lists when dumping
    json_old_edges = {list(key): list(value) for key, value in old_edges.items()}
    with open(dataset_dir / old_edge_lookup, "w", encoding="UTF-8") as json_file:
        json.dump(json_old_edges, json_file)
    with open(dataset_dir / old_node_lookup, "w", encoding="UTF-8") as json_file:
        json.dump(old_vertices, json_file)

    # get depots
    depots = list(nodes_df.loc[nodes_df.is_depot].index.map(normalize_map))
    nx.set_node_attributes(normalized_graph, False, "is_depot")
    for v in depots:
        normalized_graph.nodes[v]["is_depot"] = True

    # NOTE (not implemented yet) get node co-ordinates

    # get TSP representation
    tsp = BaseTSP.from_networkx(
        name,
        comment,
        "PCTSP",
        normalized_graph,
        edge_weight_format=EdgeWeightFormat.LOWER_DIAG_ROW,
        weight_attr_name="cost",
    )

    # save to txt file
    problem = tsp.to_tsplib95()
    txt_filepath = dataset_dir / f"{name}.txt"
    problem.save(txt_filepath)
    return tsp


def to_pandas_nodelist(G: nx.Graph) -> pd.DataFrame:
    """Move node attributes to a pandas dataframe. Node ID is stored in 'node' column."""
    return pd.DataFrame([{"node": node, **data} for node, data in G.nodes(data=True)])


def main(location: LondonaqLocationShort, dataset_dir: Path):
    """Entrypoint for generating londonaq dataset"""
    timestamp_id: LondonaqTimestamp = LondonaqTimestamp.A
    name = londonaq_graph_name(location, timestamp_id)
    comment = londonaq_comment(location, timestamp_id)
    generate_londonaq_dataset(
        dataset_dir / name.value,
        name,
        comment,
        edges_csv_filename=name.value + "_edges.csv",
        nodes_csv_filename=name.value + "_nodes.csv",
    )


if __name__ == "__main__":
    typer.run(main)
