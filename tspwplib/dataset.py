from pathlib import Path
import tsplib95


def load_tsplib_dataset(root: Path, name: str):
    problem = tsplib95.load(root / (name + ".tsp"))
    return problem
