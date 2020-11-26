"""Setup script for tspwplib"""

from distutils.core import setup

setup(
    author="Patrick O'Hara",
    author_email="pohara@turing.ac.uk",
    description="Library of instances for TSP with Profits",
    install_requires=["tsplib95"],
    name="tspwplib",
    packages=["tspwplib"],
    python_requires=">=3.6",
    version="0.1",
)
