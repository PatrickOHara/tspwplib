"""Test types"""

from tspwplib import GraphName, OptimalSolutionTSP


def test_no_missing_graphs():
    """Iterate through all graph names and check they have a solution"""
    for graph_name in GraphName:
        assert graph_name.name == graph_name.value
        assert graph_name.name in OptimalSolutionTSP.__members__
        assert OptimalSolutionTSP[graph_name.name] > 0
