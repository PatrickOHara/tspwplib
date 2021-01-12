"""Functions and classes for datasets"""

from typing import List
import graph_tool as gt
import networkx as nx
import tsplib95
from .types import Vertex, VertexLookup


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
            cost: int = self.get_weight(u, v)
            # pylint: disable=unsupported-membership-test
            # is_fixed: bool = (u, v) in self.fixed_edges
            graph.add_edge(names[u], names[v], cost=cost)

    def __set_graph_attributes(self, graph: nx.Graph) -> None:
        """Set attributes of the graph such as the name"""
        graph.graph["name"] = self.name
        graph.graph["comment"] = self.comment
        graph.graph["type"] = self.type
        graph.graph["dimension"] = self.dimension
        graph.graph["capacity"] = self.capacity
        graph.graph["root"] = self.get_root_vertex()

    def __set_node_attributes(self, graph: nx.Graph, names: VertexLookup) -> None:
        """Add node attributes"""
        node_score = self.get_node_score()
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
                prize=node_score[vertex],
                # is_depot=is_depot,
            )
            # demand: int = self.demands.get(vertex)
            # display = self.display_data.get(vertex)
            # if not demand is None:
            # graph[vertex]["demand"] = demand
            # if not display is None:
            # graph[vertex]["display"] = display
        # nx.set_node_attributes(
        #     graph, self.get_node_score(), name=VertexFunctionName.prize
        # )

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

    def get_graph_tool(self, normalize: bool = True) -> gt.Graph:
        """Return a graph tools undirected graph

        Args:
            normalize: rename nodes to be zero-indexed
        """
        graph = gt.Graph(directed=not self.is_symmetric())

        # by default normalize because graph tools index starts at zero
        nodes: List[Vertex] = list(self.get_nodes())
        if normalize:
            names = {n: i for i, n in enumerate(nodes)}
        else:
            names = {n: n for n in nodes}

        # create list of edges
        edges = []
        for u, v in self.get_edges():
            if u <= v or not self.is_symmetric():
                edges.append((names[u], names[v], self.get_weight(u, v)))

        # assign cost to edges
        cost_property = graph.new_edge_property("int")
        graph.add_edge_list(edges, eprops=[cost_property])
        graph.ep.cost = cost_property

        # assign prize to vertices
        prize_property = graph.new_vertex_property("int")
        node_score = self.get_node_score()
        prize_list = [node_score[v + 1] for v in graph.get_vertices()]
        prize_property.a = prize_list
        graph.vertex_properties.prize = prize_property

        return graph

    def get_total_prize(self) -> int:
        """Get the sum of prize over all vertices

        Returns:
            Total prize
        """
        # pylint: disable=no-member
        return sum([value for _, value in self.get_node_score().items()])

    def get_quota(self, alpha: int) -> int:
        """The quota is alpha percent of the total prize

        Args:
            alpha: Percent of the total prize

        Returns:
            quota
        """
        if alpha > 100:
            raise ValueError("Cannot have a percent over 100 for alpha")
        if alpha < 0:
            raise ValueError("Cannot have a negative percent for alpha")
        return int(float(alpha * self.get_total_prize()) / 100.0)

    def number_of_nodes(self) -> int:
        """Get the number of nodes in the problem

        Returns:
            Number of nodes in graph
        """
        return len(list(self.get_nodes()))

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

    def get_root_vertex(self, normalize: bool = False) -> Vertex:
        """Get the root vertex

        Args:
            normalize: If true, vertices start at index 0

        Returns:
            The first depot in the list

        Raises:
            ValueError: If the list of depots is empty
        """
        nodes: List[Vertex] = list(self.get_nodes())
        if normalize:
            names = {n: i for i, n in enumerate(nodes)}
        else:
            names = {n: n for n in nodes}
        try:
            # pylint: disable=unsubscriptable-object
            return names[self.depots[0]]
        except KeyError as key_error:
            raise ValueError("The list of depots is empty") from key_error
