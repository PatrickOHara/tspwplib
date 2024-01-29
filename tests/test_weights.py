"""Test weight generation functions"""

import numpy as np
import pytest
from tspwplib import build_path_to_oplib_instance, build_path_to_tsplib_instance, ProfitsProblem
from tspwplib.problem import PrizeCollectingTSP, BaseTSP
from tspwplib.weights import generation_three_prize, generation_three_prize_list
from tspwplib.types import NodeCoordType, Generation


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

def test_gen3_prize_is_same(oplib_root, tsplib_root, graph_name):
    """Test an OP instance can be parsed"""
    op_filepath = build_path_to_oplib_instance(oplib_root, Generation.gen3, graph_name)
    profits_problem = ProfitsProblem.load(op_filepath)
    op_problem = PrizeCollectingTSP.from_tsplib95(profits_problem)

    tsp_filepath = build_path_to_tsplib_instance(tsplib_root, graph_name)
    tsp_problem = BaseTSP.from_tsplib95(ProfitsProblem().load(tsp_filepath))
    assert op_problem.node_coord_type == tsp_problem.node_coord_type
    if op_problem.node_coord_type == NodeCoordType.TWOD_COORDS:
        coords = np.array(list(tsp_problem.node_coords.values()))
        assert list(profits_problem.get_node_score().values()) == generation_three_prize_list(coords)
