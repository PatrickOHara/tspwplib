"""Useful functions for parsing"""

from pathlib import Path
from .types import Alpha, Generation, GraphName


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
