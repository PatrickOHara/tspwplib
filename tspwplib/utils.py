"""Useful functions for parsing"""

from pathlib import Path
from .types import Alpha, Generation, InstanceName


def build_path_to_oplib_instance(
    oplib_root: Path,
    generation: Generation,
    name: InstanceName,
    alpha: Alpha = Alpha.fifty,
) -> Path:
    """Build a filepath to a oplib instance"""
    filename: str = name + "-" + generation.value + "-" + str(alpha.value) + ".oplib"
    return oplib_root / "instances" / generation.value / filename


def build_path_to_tsplib_instance(tsplib_root: Path, name: InstanceName) -> Path:
    """Build a filepath to a tsplib instance"""
    filename = name.value + ".tsp"
    return tsplib_root / filename
