"""Fixtures for testing"""

from pathlib import Path
import pytest
from tspwplib.types import Alpha, Generation, InstanceName

@pytest.fixture(scope="function")
def tsplib_root() -> Path:
    """Root of tsplib95 data"""
    return Path("/Users/pohara/data/tsplib95")

@pytest.fixture(scope="function")
def oplib_root() -> Path:
    """Root of the cloned OP lib"""
    return Path("/Users/pohara/data/oplib")


@pytest.fixture(
    scope="function",
    params=[
        Generation.one,
        Generation.two,
        Generation.three,
    ],
)
def generation(request) -> Generation:
    """Loop through valid generations"""
    # NOTE generation 4 has different alpha values
    return request.param


@pytest.fixture(scope="function", params=[Alpha.fifty])
def alpha(request) -> Alpha:
    """Alpha values"""
    return request.param


@pytest.fixture(
    scope="function",
    params=[
        InstanceName.eil76,
        InstanceName.st70,
        InstanceName.vm1748,
    ]
)
def instance_name(request) -> InstanceName:
    """Loop through valid instance names"""
    return request.param
