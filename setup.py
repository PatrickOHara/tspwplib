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
    classifiers=[
        'Programming Language :: Python',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3 :: Only',
        'Operating System :: OS Independent',
        'License :: MIT License',
    ],
)
