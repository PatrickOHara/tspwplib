"""Tests for the utils module"""

import itertools
import networkx as nx
import pytest
from tspwplib import (
    londonaq_graph_name,
    LondonaqGraphName,
    LondonaqLocation,
    LondonaqTimestamp,
    build_path_to_oplib_instance,
    build_path_to_tsplib_instance,
    rename_edge_attributes,
    rename_node_attributes,
)


def test_build_path_to_oplib_instance(oplib_root, generation, graph_name):
    """Test path building"""
    assert build_path_to_oplib_instance(oplib_root, generation, graph_name).exists()


def test_build_path_to_tsplib_instance(tsplib_root, graph_name):
    """Test path building for tsplib"""
    assert build_path_to_tsplib_instance(tsplib_root, graph_name).exists()


def test_rename_edge_attributes():
    """Test edge attributes are renamed"""
    G = nx.from_edgelist([(0, 1), (1, 2)])
    nx.set_edge_attributes(G, 1, "weight")
    rename_edge_attributes(G, {"weight": "cost"})
    for _, _, data in G.edges(data=True):
        assert "weight" in data
        assert "cost" in data
        assert data["weight"] == data["cost"]

    # now copy the graph and delete the old edge attribute
    new_graph = rename_edge_attributes(
        G, {"weight": "length", "cost": "height"}, copy_graph=True, del_old_attr=True
    )
    for _, _, data in new_graph.edges(data=True):
        assert not "weight" in data
        assert not "cost" in data
        assert "length" in data
        assert "height" in data
        assert data["length"] == data["height"]
    for _, _, data in G.edges(data=True):
        assert "weight" in data
        assert "cost" in data
        assert not "length" in data
        assert not "height" in data


def test_rename_node_attributes():
    """Test node attributes are renamed"""
    G = nx.from_edgelist([(0, 1), (1, 2)])
    nx.set_node_attributes(G, 1, "weight")
    rename_node_attributes(G, {"weight": "cost"})
    for _, data in G.nodes(data=True):
        assert "weight" in data
        assert "cost" in data
        assert data["weight"] == data["cost"]

    # now copy the graph and delete the old node attribute
    new_graph = rename_node_attributes(
        G, {"weight": "length", "cost": "height"}, copy_graph=True, del_old_attr=True
    )
    for _, data in new_graph.nodes(data=True):
        assert not "weight" in data
        assert not "cost" in data
        assert "length" in data
        assert "height" in data
        assert data["length"] == data["height"]
    for _, data in G.nodes(data=True):
        assert "weight" in data
        assert "cost" in data
        assert not "length" in data
        assert not "height" in data


@pytest.mark.parametrize(
    "location,timestamp", itertools.product(LondonaqLocation, LondonaqTimestamp)
)
def test_londonaq_graph_name(location, timestamp):
    """Test every combination of location and timestamp yields a valid graph name"""
    assert londonaq_graph_name(location, timestamp) in LondonaqGraphName
