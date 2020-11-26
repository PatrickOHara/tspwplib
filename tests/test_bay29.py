from pathlib import Path
import networkx as nx
from tspwplib.dataset import load_tsplib_dataset


def test_bay29():
    name = "brg180"
    root = Path("/Users/pohara/data/tsplib95")
    problem = load_tsplib_dataset(root, name)
    graph = problem.get_graph()
    assert nx.complete_graph(graph)
