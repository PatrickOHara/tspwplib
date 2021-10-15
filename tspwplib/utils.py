"""Useful functions for parsing"""

from itertools import chain
from pathlib import Path
from typing import List
import networkx as nx
from .types import (
    Alpha,
    Generation,
    GraphName,
    LondonaqGraphName,
    LondonaqLocation,
    LondonaqTimestamp,
)


def build_path_to_oplib_instance(
    oplib_root: Path,
    generation: Generation,
    name: GraphName,
    alpha: int = Alpha.fifty.value,
) -> Path:
    """Build a filepath to a oplib instance

    Args:
        oplib_root: The directory of the clones oplib
        generation: Generation of OPLib instance
        name: Graph instance name
        alpha: Percent of the total cost to set the cost limit to.
            Not useful for instances of Prize-collecting TSPs.
            Default is 50.
            Note if you change to a different value, make sure the file exists

    Returns:
        Path to the OPLib instance
    """
    filename: str = name + "-" + generation.value + "-" + str(alpha) + ".oplib"
    return oplib_root / "instances" / generation.value / filename


def build_path_to_tsplib_instance(tsplib_root: Path, name: GraphName) -> Path:
    """Build a filepath to a tsplib instance

    Args:
        tsplib_root: Directory containing TSP txt instances
        name: Name of the instance

    Returns:
        Filepath to the TSP instance
    """
    filename = name.value + ".tsp"
    return tsplib_root / filename


def edge_attribute_names(G: nx.Graph) -> List[str]:
    """Get the names of all edge attributes

    Args:
        G: Graph

    Returns:
        List of attribute names
    """
    return list(set(chain.from_iterable(d.keys() for *_, d in G.edges(data=True))))


def node_attribute_names(G: nx.Graph) -> List[str]:
    """Get the names of all node attributes

    Args:
        G: Graph

    Returns:
        List of node attribute names
    """
    return list(set(chain.from_iterable(d.keys() for _, d in G.nodes(data=True))))


def londonaq_graph_name(
    location_id: LondonaqLocation, timestamp_id: LondonaqTimestamp
) -> LondonaqGraphName:
    """Get a londonaq graph name"""
    return LondonaqGraphName["laq" + location_id.name + timestamp_id.name]


def londonaq_comment(
    location_id: LondonaqLocation, timestamp_id: LondonaqTimestamp
) -> str:
    """Get a comment for a londonaq dataset"""
    comment = f"A London air quality dataset starting at {location_id.value}. "
    comment += f"The UTC timestamp for the air quality forecast is {timestamp_id.value.isoformat()}"
    return comment
