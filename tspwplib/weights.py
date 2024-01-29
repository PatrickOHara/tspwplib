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


def generation_three_prize_list(
    vertex_coords: npt.ArrayLike,
    root_vertex_index: int = 0,
) -> List[int]:
    """Generate a prize map from the vertex coordinates using the generation three prize function"""
    # get the distance from the root vertex to every other vertex
    root_coord = vertex_coords[root_vertex_index]

    def __euclidean_distance_oplib(coord2: npt.NDArray) -> int:
        xd = root_coord[0] - coord2[0]
        yd = root_coord[1] - coord2[1]
        return np.sqrt( xd*xd + yd*yd) + 0.5

    # distance_v = np.vectorize(__euclidean_distance_oplib)
    # max_distance = np.max(distance_v(vertex_coords))
        # FIXME there is a bug here somewhere, see Section 2.1 of https://github.com/bcamath-ds/OPLib/tree/master/instances
    max_distance = int(np.max(np.linalg.norm(vertex_coords - root_coord, ord=2, axis=1) + 0.5))
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
        1 + np.floor((99 / max_distance) * np.linalg.norm(root_coord - vertex_coord, ord=2))
    )
