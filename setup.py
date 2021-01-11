"""Setup script for tspwplib"""

from setuptools import setup

setup(
    author="Patrick O'Hara",
    author_email="patrick.h.o-hara@warwick.ac.uk",
    url="https://github.com/PatrickOHara/tspwplib",
    description="Library of instances for TSP with Profits",
    install_requires=[
        "pandas>=1.0.0",
        "tsplib95>=0.7.1",
    ],
    name="tspwplib",
    packages=["tspwplib"],
    python_requires=">=3.6",
    license="MIT",
    classifiers=[
        "Programming Language :: Python",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3 :: Only",
        "Operating System :: OS Independent",
    ],
    use_scm_version=True,
    setup_requires=["setuptools_scm"],
)
