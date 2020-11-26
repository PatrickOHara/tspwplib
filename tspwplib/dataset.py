"""Functions and classes for datasets"""

from pathlib import Path
import tsplib95
from .types import InstanceName


def load_tsplib_dataset(root: Path, name: InstanceName):
    """Load a TSP lib problem"""
    problem = tsplib95.load(root / (name.value + ".tsp"))
    return problem
