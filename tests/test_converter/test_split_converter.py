"""Tests for splitting edges"""

from tspwplib.converter import (
    split_edges,
    split_graph_from_properties,
    lookup_from_split,
    lookup_to_split,
)


def test_split_edges():
    """Test split edges"""
    edge_list = [(0, 1), (1, 2), (0, 2)]
    splits = split_edges(edge_list)
    assert len(splits) == len(edge_list) * 2
    assert (0, -1) in splits
    assert (0, -3) in splits

    # test lookups
    from_split = lookup_from_split(edge_list, splits)
    assert from_split[(0, -1)] == (0, 1)
    assert from_split[(-1, 1)] == (0, 1)
    assert from_split[(0, -3)] == (0, 2)

    to_split = lookup_to_split(edge_list, splits)
    assert to_split[(0, 1)] == ((0, -1), (-1, 1))
    assert to_split[(1, 2)] == ((1, -2), (-2, 2))


def test_split_graph_from_properties():
    """Test split graph"""
    properties = {
        (0, 1): {"weight": 5, "cost": 3},
        (1, 2): {"weight": 1, "cost": 10},
        (0, 2): {"weight": 2, "cost": 5},
    }
    G = split_graph_from_properties(properties)
    for _, _, data in G.edges(data=True):
        old_edge = data["old_edge"]
        assert data["cost"] == float(properties[old_edge]["cost"]) / 2.0
