"""Test weight generation functions"""

import numpy as np
from tspwplib.weights import generation_three_prize_map

def test_generation_three_prize_map():
    """Test generation three prizes are generated correctly"""
    vertex_coords = np.array([
        [0, 0],
        [5, 0],
        [1, 1],
    ])
    prizes = generation_three_prize_map(vertex_coords)
    assert False
    assert prizes[0][0] == 1
