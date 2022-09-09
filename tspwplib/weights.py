"""Functions for calculating edge and vertex weights"""

import numpy as np
import numpy.typing as npt
from .types import Vertex, VertexFunction

def generation_one_prize() -> int:
    """Returns 1 for every vertex"""
    return 1

def generation_two_prize(vertex: Vertex) -> int:
    """Returns a prize that relatively random"""
    return 1 + (7141 * vertex + 73) % 100

def generation_three_prize_map(
    vertex_coords: npt.ArrayLike,
    root_vertex_index: int = 0,
) -> VertexFunction:
    """Generate a prize map from the vertex coordinates using the generation three prize function"""
    # get the distance from the root vertex to every other vertex
    root_coord = vertex_coords[root_vertex_index]
    def get_distance(x):
        return np.linalg.norm(root_coord - x)
    distance_vectorized = np.vectorize(get_distance)
    distances = distance_vectorized(vertex_coords)
    print(distances)
    max_distance = np.max(distances)
    return [1 + np.floor((99 / max_distance)) * vertex_distance for vertex_distance in distances]

def generation_three_prize(
    vertex_coord: npt.NDArray,
    root_coord: npt.NDArray,
    max_distance: float
) -> int:
    """Vertices have larger prizes when they are further away from the root vertex"""
    return 1 + np.floor((99 / max_distance) * np.linalg.norm(root_coord - vertex_coord))
