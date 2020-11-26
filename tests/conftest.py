"""Fixtures for testing"""

import os
from pathlib import Path
import pytest
from tspwplib.types import Alpha, Generation, InstanceName


def pytest_addoption(parser):
    """Add option to enable travis specific options"""
    parser.addoption(
        "--tsplib-root",
        default=os.environ.get("TSPLIB_ROOT"),
        required=False,
        type=str,
        help="Filepath to tsplib95 directory",
    )
    parser.addoption(
        "--oplib-root",
        default=os.environ.get("OPLIB_ROOT"),
        required=False,
        type=str,
        help="Filepath to oplib directory",
    )


@pytest.fixture(scope="function")
def tsplib_root(request) -> Path:
    """Root of tsplib95 data"""
    return Path(request.config.getoption("--tsplib-root"))


@pytest.fixture(scope="function")
def oplib_root(request) -> Path:
    """Root of the cloned OP lib"""
    return Path(request.config.getoption("--oplib-root"))


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
        InstanceName.rat195,
    ],
)
def instance_name(request) -> InstanceName:
    """Loop through valid instance names"""
    return request.param
