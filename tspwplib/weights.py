"""Functions for calculating edge and vertex weights"""

from typing import List
import numpy as np
import numpy.typing as npt
from .types import Vertex


def generation_one_prize() -> int:
    """Returns 1 for every vertex"""
    return 1


def generation_two_prize(vertex: Vertex) -> int:
    """Returns a prize that relatively random"""
    return int(1 + (7141 * vertex + 73) % 100)

def __euclidean_distance_oplib(coord1: npt.NDArray, coord2: npt.NDArray) -> int:
    xd = coord1[0] - coord2[0]
    yd = coord1[1] - coord2[1]
    return (int) (np.sqrt( xd*xd + yd*yd) + 0.5)

def generation_three_prize_list(
    vertex_coords: npt.ArrayLike,
    root_vertex_index: int = 0,
) -> List[int]:
    """Generate a prize map from the vertex coordinates using the generation three prize function"""
    # get the distance from the root vertex to every other vertex
    root_coord = vertex_coords[root_vertex_index]
    max_distance = np.max(np.linalg.norm(root_coord - vertex_coords, axis=1, ord=2))
    if np.isclose(max_distance, 0):
        raise ValueError("Maximum distance from any vertex to the root vertex is zero.")
    return [
        generation_three_prize(coord, root_coord, max_distance)
        for coord in vertex_coords
    ]


def generation_three_prize(
    vertex_coord: npt.NDArray, root_coord: npt.NDArray, max_distance: float
) -> int:
    """Vertices have larger prizes when they are further away from the root vertex"""
    return int(
        1 + np.floor((99.0 / max_distance) * np.linalg.norm(root_coord - vertex_coord, ord=2))
    )
