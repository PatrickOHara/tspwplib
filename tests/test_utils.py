"""Tests for the utils module"""

from tspwplib import build_path_to_oplib_instance, build_path_to_tsplib_instance


def test_build_path_to_oplib_instance(oplib_root, generation, graph_name):
    """Test path building"""
    assert build_path_to_oplib_instance(oplib_root, generation, graph_name).exists()


def test_build_path_to_tsplib_instance(tsplib_root, graph_name):
    """Test path building for tsplib"""
    assert build_path_to_tsplib_instance(tsplib_root, graph_name).exists()
