"""Functions and classes for datasets"""

from typing import List
import networkx as nx
import tsplib95
from .types import Vertex, VertexFunctionName, VertexLookup


class ProfitsProblem(tsplib95.models.StandardProblem):
    """TSP with Profits Problem"""

    # Maximum distance of the total route in a OP.
    cost_limit = tsplib95.fields.IntegerField("COST_LIMIT")
    # The scores of the nodes of a OP are given in the form (per line)
    node_score = tsplib95.fields.DemandsField("NODE_SCORE_SECTION")
    # The optimal solution to the TSP
    tspsol = tsplib95.fields.IntegerField("TSPSOL")

    def __set_edge_attributes(self, graph: nx.Graph, names: VertexLookup) -> None:
        """Set edge attributes"""
        # add every edge with some associated metadata
        for u, v in self.get_edges():
            weight: int = self.get_weight(u, v)
            # pylint: disable=unsupported-membership-test
            # is_fixed: bool = (u, v) in self.fixed_edges
            graph.add_edge(names[u], names[v], weight=weight)

    def __set_graph_attributes(self, graph: nx.Graph) -> None:
        """Set attributes of the graph such as the name"""
        graph.graph["name"] = self.name
        graph.graph["comment"] = self.comment
        graph.graph["type"] = self.type
        graph.graph["dimension"] = self.dimension
        graph.graph["capacity"] = self.capacity
        # pylint: disable=unsubscriptable-object
        graph.graph["root"] = self.depots[0]

    def __set_node_attributes(self, graph: nx.Graph, names: VertexLookup) -> None:
        """Add node attributes"""
        for vertex in list(self.get_nodes()):
            # NOTE pyintergraph cannot handle bool, so we remove some attributes:
            # is_depot, demand, display
            # pylint: disable=unsupported-membership-test,no-member
            # is_depot = vertex in self.depots
            coord: List[int] = self.node_coords.get(vertex)
            graph.add_node(
                names[vertex],
                x=coord[0],
                y=coord[1],
                # is_depot=is_depot,
            )
            # demand: int = self.demands.get(vertex)
            # display = self.display_data.get(vertex)
            # if not demand is None:
            # graph[vertex]["demand"] = demand
            # if not display is None:
            # graph[vertex]["display"] = display
        nx.set_node_attributes(
            graph, self.get_node_score(), name=VertexFunctionName.prize
        )

    def get_graph(self, normalize: bool = False) -> nx.Graph:
        """Return a networkx graph instance representing the problem.

        Args:
            normalize: rename nodes to be zero-indexed
        """
        # directed graphs are fundamentally different
        graph: nx.Graph = nx.Graph() if self.is_symmetric() else nx.DiGraph()

        # add basic graph metadata
        self.__set_graph_attributes(graph)

        # set up a map from original node name to new node name
        nodes: List[Vertex] = list(self.get_nodes())
        if normalize:
            names = {n: i for i, n in enumerate(nodes)}
        else:
            names = {n: n for n in nodes}

        self.__set_node_attributes(graph, names)
        self.__set_edge_attributes(graph, names)
        return graph

    def get_cost_limit(self) -> int:
        """Get the cost limit for a TSP with Profits problem

        Returns:
            Cost limit
        """
        return self.cost_limit

    def get_node_score(self) -> VertexLookup:
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
