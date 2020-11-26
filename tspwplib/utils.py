"""Useful functions for parsing"""

from pathlib import Path
from .types import Alpha, Generation


def build_path_to_oplib_instance(
    oplib_root: Path, generation: Generation, name: str, alpha: Alpha = Alpha.fifty
) -> Path:
    """Build a filepath to a oplib instance"""
    filename: str = name + "-" + generation.value + "-" + str(alpha.value) + ".oplib"
    return oplib_root / "instances" / generation.value / filename
