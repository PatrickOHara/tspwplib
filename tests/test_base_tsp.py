"""Tests for the pydantic representation of a TSP"""

import pytest
from tsplib95.models import StandardProblem
from tspwplib import BaseTSP, GraphName, build_path_to_tsplib_instance


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
