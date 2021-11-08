"""Script for generating a tsplib style txt file from londonaq CSV"""

import itertools
import json
from pathlib import Path

import networkx as nx
import pandas as pd
import typer

from urbanroute import frames_from_urbanair_api

from tspwplib import split_graph_from_properties
from tspwplib.problem import BaseTSP
from tspwplib.types import (
    EdgeWeightFormat,
    LondonaqGraphName,
    LondonaqLocation,
    LondonaqLocationShort,
    LondonaqTimestamp,
    LondonaqTimestampId,
)
from tspwplib.utils import londonaq_comment, londonaq_graph_name

OLD_EDGE_LOOKUP_JSON = "old_edge_lookup.json"
OLD_NODE_LOOKUP_JSON = "old_node_lookup.json"


def csv_from_urbanair_api(
    username: str,
    password: str,
    location: LondonaqLocation,
    distance: int,
    timestamp: LondonaqTimestamp,
    csv_output_dir: Path,
    csv_prefix: str,
) -> None:
    """Write CSV files of nodes and edges from urbanair API."""
    csv_output_dir.mkdir(exist_ok=True, parents=False)
    print(location.value)
    edges_df, nodes_df = frames_from_urbanair_api(
        username, password, location.value, distance, timestamp.value
    )
    # output is a CSV file representing an undirected simple graph
    edges_df.to_csv(csv_output_dir / (csv_prefix + "_edges.csv"), index=False)
    nodes_df.to_csv(
        csv_output_dir / (csv_prefix + "_nodes.csv"), index=True, index_label="node"
    )


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
    json_old_edges = {
        key[0]: {key[1]: list(old_edges[key])} for key in old_edges.keys()
    }
    with open(dataset_dir / old_edge_lookup, "w", encoding="UTF-8") as json_file:
        json.dump(json_old_edges, json_file)
    with open(dataset_dir / old_node_lookup, "w", encoding="UTF-8") as json_file:
        json.dump(old_vertices, json_file)

    # get depots
    depots = list(nodes_df.loc[nodes_df.is_depot].index.map(normalize_map))
    nx.set_node_attributes(normalized_graph, False, "is_depot")
    for v in depots:
        normalized_graph.nodes[v]["is_depot"] = True

    # round cost and demand
    for _, data in normalized_graph.nodes(data=True):
        data["demand"] = round(data["demand"])
    for _, _, data in normalized_graph.edges(data=True):
        data["cost"] = round(data["cost"])

    # NOTE (not implemented yet) get node co-ordinates

    # get TSP representation
    tsp = BaseTSP.from_networkx(
        name,
        comment,
        "PCTSP",
        normalized_graph,
        edge_weight_format=EdgeWeightFormat.FULL_MATRIX,
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


app = typer.Typer(name="generate")

LONDONAQ_TINY_QUOTA = 200
LONDONAQ_SMALL_QUOTA = 500


@app.command(name="onlyone")
def generate_only_one_dataset(
    username: str,
    password: str,
    location_short: LondonaqLocationShort,
    timestamp_id: LondonaqTimestampId,
    dataset_dir: Path,
):
    """Generate only one dataset given the location and timestamp"""
    timestamp = LondonaqTimestamp[timestamp_id]
    print("location short:", location_short)
    location = LondonaqLocation[location_short]
    print("location:", location.name)
    name = londonaq_graph_name(location, timestamp)
    print("New thread for", name)
    comment = londonaq_comment(location, timestamp)
    if location_short == LondonaqLocationShort.tiny:
        distance = LONDONAQ_TINY_QUOTA
    else:
        distance = LONDONAQ_SMALL_QUOTA
    csv_from_urbanair_api(
        username,
        password,
        location,
        distance,
        timestamp,
        dataset_dir / name.value,
        name,
    )
    generate_londonaq_dataset(
        dataset_dir / name.value,
        name,
        comment,
        edges_csv_filename=name.value + "_edges.csv",
        nodes_csv_filename=name.value + "_nodes.csv",
    )
    print("Finished", name)


@app.command(name="all")
def generate_all_datasets(username: str, password: str, dataset_dir: Path):
    """Generate all urbanair datasets"""
    for timestamp_id, location in itertools.product(
        LondonaqTimestampId, LondonaqLocationShort
    ):
        generate_only_one_dataset(
            username, password, location, timestamp_id, dataset_dir
        )


if __name__ == "__main__":
    app()
