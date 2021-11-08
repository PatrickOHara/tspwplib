"""Tests for the pydantic representation of a TSP"""

import pytest
from tsplib95.models import StandardProblem
from tspwplib import BaseTSP, GraphName, build_path_to_tsplib_instance


def test_get_weighted_full_matrix(tsplib_root, graph_name):
    """Test weighted adjacency matrix"""
    tsp_path = build_path_to_tsplib_instance(tsplib_root, graph_name)
    problem = StandardProblem.load(tsp_path)
    tsp = BaseTSP.from_tsplib95(problem)
    weights = tsp.get_weighted_full_matrix()
    for i, u in enumerate(problem.get_nodes()):
        for j, v in enumerate(problem.get_nodes()):
            assert weights[i, j] == problem.get_weight(u, v)


@pytest.mark.parametrize("gname", list(GraphName))
def test_from_tsplib95(tsplib_root, gname):
    """Test tsplib95 problems can be read into BaseTSP"""
    # only load problems with less than 1000 vertices
    n_nodes = int("".join(filter(str.isdigit, gname.value)))
    if n_nodes < 1000:
        tsp_path = build_path_to_tsplib_instance(tsplib_root, gname)
        assert tsp_path.exists()
        problem = StandardProblem.load(tsp_path)
        tsp = BaseTSP.from_tsplib95(problem)
        assert len(tsp.edge_data) == len(list(problem.get_edges()))
        for edge, weight in tsp.edge_weights.items():
            assert weight == problem.get_weight(edge[0], edge[1])


@pytest.mark.parametrize("gname", list(GraphName))
def test_to_tsplib95(tsplib_root, gname):
    """Test going to tsplib"""
    # only load problems with less than 1000 vertices
    n_nodes = int("".join(filter(str.isdigit, gname.value)))
    if n_nodes < 1000:
        tsp_path = build_path_to_tsplib_instance(tsplib_root, gname)
        assert tsp_path.exists()
        og_problem = StandardProblem.load(tsp_path)
        tsp = BaseTSP.from_tsplib95(og_problem)
        new_problem = tsp.to_tsplib95()
        # pylint: disable=not-an-iterable,unsupported-membership-test
        for u, v in og_problem.edge_data:
            assert (u, v) in new_problem.edge_data
            assert og_problem.get_weight(u, v) == new_problem.get_weight(u, v)
