"""Functions and classes for datasets"""

from typing import Dict
import networkx as nx
import tsplib95
from .types import VertexFunctionName


class ProfitsProblem(tsplib95.models.StandardProblem):
    """TSP with Profits Problem"""

    # Maximum distance of the total route in a OP.
    cost_limit = tsplib95.fields.IntegerField("COST_LIMIT")
    # The scores of the nodes of a OP are given in the form (per line)
    node_score = tsplib95.fields.DemandsField("NODE_SCORE_SECTION")
    # The optimal solution to the TSP
    tspsol = tsplib95.fields.IntegerField("TSPSOL")

    def get_graph(self, normalize: bool = False) -> nx.Graph:
        """Return a networkx graph instance representing the problem.

        Args:
            normalize: rename nodes to be zero-indexed
        """
        graph: nx.Graph = super().get_graph(normalize=normalize)
        nx.set_node_attributes(
            graph, self.get_node_score(), name=VertexFunctionName.prize
        )
        return graph

    def get_cost_limit(self) -> int:
        """Get the cost limit for a TSP with Profits problem

        Returns:
            Cost limit
        """
        return self.cost_limit

    def get_node_score(self) -> Dict[int, int]:
        """Get the node scores (profits)

        Returns:
            Mapping from node to node score (profit)
        """
        return self.node_score

    def get_tsp_optimal_value(self) -> int:
        """Get the value of the optimal solution to TSP

        Returns:
            TSP optimal value
        """
        return self.tspsol
