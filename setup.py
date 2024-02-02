"""Setup script for tspwplib"""

from setuptools import setup

setup(
    author="Patrick O'Hara",
    author_email="patrick.h.o-hara@warwick.ac.uk",
    url="https://github.com/PatrickOHara/tspwplib",
    description="Library of instances for TSP with Profits",
    install_requires=[
        "networkx>=3.0.0",
        "numpy>=1.26.0",
        "pandas>=2.0.0",
        "pydantic>=2.5.3",
        "pyyaml>=6.0",
        "tsplib95@git+https://github.com/ben-hudson/tsplib95.git",
    ],
    name="tspwplib",
    packages=["tspwplib"],
    python_requires=">=3.10",
    license="MIT",
    classifiers=[
        "Programming Language :: Python",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3.12",
        "Programming Language :: Python :: 3 :: Only",
        "Operating System :: OS Independent",
    ],
    use_scm_version=True,
    setup_requires=["setuptools_scm"],
)
