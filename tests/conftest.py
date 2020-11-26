"""Fixtures for testing"""

import pytest
from pathlib import Path
from tspwplib.types import Alpha, Generation, InstanceName


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


@pytest.fixture(scope="function", params=[InstanceName.vm1748])
def instance_name(request) -> InstanceName:
    """Loop through valid instance names"""
    return request.param
