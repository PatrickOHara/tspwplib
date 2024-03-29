"""Functions for calculating edge and vertex weights"""

from typing import List, Callable
import numpy as np
import numpy.typing as npt
from .types import Vertex


def generation_one_prize() -> int:
    """Returns 1 for every vertex"""
    return 1


def generation_two_prize(vertex: Vertex) -> int:
    """Returns a prize that relatively random"""
    return int(1 + (7141 * vertex + 73) % 100)


def generation_three_prize_list(
    dist_fn: Callable[[npt.NDArray, npt.NDArray], int],
    vertex_coords: npt.ArrayLike,
    root_vertex_index: int = 0,
) -> List[int]:
    """Generate a prize map from the vertex coordinates using the generation three prize function"""
    # get the distance from the root vertex to every other vertex
    root_coord = vertex_coords[root_vertex_index]

    distances = np.apply_along_axis(dist_fn, 1, vertex_coords, root_coord)
    max_distance = np.max(distances)
    if np.isclose(max_distance, 0):
        raise ValueError("Maximum distance from any vertex to the root vertex is zero.")
    return [
        generation_three_prize(dist_fn, coord, root_coord, max_distance)
        for coord in vertex_coords
    ]


def generation_three_prize(
    dist_fn: Callable[[npt.NDArray, npt.NDArray], int],
    vertex_coord: npt.NDArray,
    root_coord: npt.NDArray,
    max_distance: float,
) -> int:
    """Vertices have larger prizes when they are further away from the root vertex"""
    return int(1 + np.floor((99 / max_distance) * dist_fn(vertex_coord, root_coord)))


def euc_2d(i: npt.NDArray, j: npt.NDArray) -> int:
    """The rounded Euclidean distance / L2 norm between two co-ordinates"""
    return int(np.round(np.linalg.norm(i - j, ord=2)))
