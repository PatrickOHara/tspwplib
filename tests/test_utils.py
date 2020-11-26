"""Tests for the utils module"""

from tspwplib.utils import build_path_to_oplib_instance


def test_build_path_to_oplib_instance(oplib_root, generation, instance_name, alpha):
    """Test path building"""
    assert build_path_to_oplib_instance(
        oplib_root, generation, instance_name, alpha=alpha
    ).exists()
