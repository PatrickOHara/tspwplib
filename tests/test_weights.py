"""Test weight generation functions"""

import numpy as np
import pytest
from tspwplib.weights import generation_three_prize, generation_three_prize_list


def test_generation_three_prize_map():
    """Test generation three prizes are generated correctly"""
    vertex_coords = np.array(
        [
            [0, 0],
            [5, 0],
            [1, 1],
        ]
    )
    prizes = generation_three_prize_list(vertex_coords)
    assert prizes[0] == 1
    assert prizes[1] == 100
    assert prizes[2] == 29


@pytest.mark.parametrize(
    ["vertex_coord", "root_coord", "max_distance", "expected_prize"],
    [
        (np.array([0.0, 0.0]), np.array([0.0, 0.0]), 5.0, 1),
        (np.array([0.0, 5.0]), np.array([0.0, 0.0]), 5.0, 100),
        (np.array([1.0, 1.0]), np.array([0.0, 0.0]), 5.0, 29),
    ],
)
def test_generation_three_prize(vertex_coord, root_coord, max_distance, expected_prize):
    """Test generation three prizes are generated correctly"""
    assert (
        generation_three_prize(vertex_coord, root_coord, max_distance) == expected_prize
    )
