"""Functions and classes for datasets"""

import random
from typing import List, Optional, Union

import networkx as nx
import pandas as pd
import pydantic
import tsplib95

from .types import (
    DisplayDataType,
    EdgeDataFormat,
    EdgeFunction,
    EdgeList,
    EdgeWeightFormat,
    EdgeWeightType,
    NodeCoords,
    NodeCoordType,
    Vertex,
    VertexFunction,
    VertexFunctionName,
    VertexList,
    VertexLookup,
)
from .utils import edge_attribute_names, node_attribute_names
from .walk import is_simple_cycle, walk_from_edge_list, total_prize

# pylint: disable=too-few-public-methods


class BaseTSP(pydantic.BaseModel):
    """A pydantic model for tsplib95.

    Each field is validated with type hinting.
    """

    # pylint: disable=too-many-arguments

    capacity: Optional[Union[int, float]]
    comment: str
    demands: Optional[VertexFunction]
    depots: VertexList
    dimension: int
    display_data: Optional[NodeCoords]
    display_data_type: DisplayDataType
    edge_data: EdgeList
    edge_data_format: EdgeDataFormat
    edge_weights: Optional[EdgeFunction]
    edge_weight_format: EdgeWeightFormat
    edge_weight_type: EdgeWeightType
    fixed_edges: EdgeList
    name: str
    node_coords: Optional[NodeCoords]
    node_coord_type: NodeCoordType
    problem_type: str
    tours: Optional[List[VertexList]]

    class Config:
        """Pydantic configuration"""

        arbitrary_types_allowed = True

    @classmethod
    def from_networkx(
        cls,
        name: str,
        comment: str,
        problem_type: str,
        G: nx.Graph,
        capacity: Optional[Union[int, float]] = None,
        display_data: Optional[NodeCoords] = None,
        display_data_type: DisplayDataType = DisplayDataType.NO_DISPLAY,
        edge_weight_format: EdgeWeightFormat = EdgeWeightFormat.FULL_MATRIX,
        weight_attr_name: str = "weight",
    ):
        """Get a base TSP model from a networkx graph"""
        edge_attr_names = edge_attribute_names(G)
        node_attr_names = node_attribute_names(G)
        if weight_attr_name not in edge_attr_names:
            message = f"{weight_attr_name} is required to be an edge attribute, "
            message += "but was not found in graph. "
            message += "This function only supports an explicit weight function. "
            raise NotImplementedError(message)
        is_2d = "x" in node_attr_names and "y" in node_attr_names
        is_3d = is_2d and "z" in node_attr_names
        if is_3d:
            raise NotImplementedError("3D coords are not supported")
            # node_coord_type = NodeCoordType.THREED_COORDS
            # node_coords = {
            #     node: (float(data["x"]), float(data["y"]), float(data["z"]))
            #     for node, data in G.nodes(data=True)
            # }
        if is_2d:
            node_coord_type = NodeCoordType.TWOD_COORDS
            node_coords = {
                node: (float(data["x"]), float(data["y"]))
                for node, data in G.nodes(data=True)
            }
        else:
            node_coord_type = NodeCoordType.NO_COORDS
            node_coords = {}

        demands = None
        if "demand" in node_attr_names:
            demands = nx.get_node_attributes(G, "demand")
        if display_data_type == DisplayDataType.COORD_DISPLAY:
            display_data = node_coords

        fixed_edges = []
        if "is_fixed" in edge_attr_names:
            fixed_edges = [
                edge for edge, data in G.edges(data=True) if data["is_fixed"]
            ]

        depots = []
        if "is_depot" in node_attr_names:
            depots = [node for node, data in G.nodes(data=True) if data["is_depot"]]
        edge_data = list(G.edges())
        edge_weights = nx.get_edge_attributes(G, weight_attr_name)
        return cls(
            capacity=capacity,
            comment=comment,
            demands=demands,
            depots=depots,
            dimension=G.number_of_nodes(),
            display_data=display_data,
            display_data_type=display_data_type,
            edge_data=edge_data,
            edge_data_format=EdgeDataFormat.EDGE_LIST,
            edge_weights=edge_weights,
            edge_weight_format=edge_weight_format,
            edge_weight_type=EdgeWeightType.EXPLICIT,
            fixed_edges=fixed_edges,
            name=name,
            node_coords=node_coords,
            node_coord_type=node_coord_type,
            problem_type=problem_type,
            tours=None,
        )

    @classmethod
    def from_dataframes(
        cls,
        name: str,
        comment: str,
        problem_type: str,
        edges_df: pd.DataFrame,
        nodes_df: pd.DataFrame,
        capacity: Optional[Union[int, float]] = None,
        display_data: Optional[NodeCoords] = None,
        display_data_type: DisplayDataType = DisplayDataType.NO_DISPLAY,
        edge_weight_format: EdgeWeightFormat = EdgeWeightFormat.FULL_MATRIX,
    ):
        """Get a TSP base model from edge and node dataframes

        Notes:
            Essential edge columns: [source, target, weight].
            Optional edge columns: [is_fixed].
            Essential node columns: [node, is_depot].
            Optional node columns: [x, y, z, demand].
            The edge weight function is explicitly given by the 'weight' column.
        """
        if "weight" not in edges_df:
            message = "'weight' is not a column in edges_df. "
            message += "This function only supports an explicit weight function. "
            message += "If you have a column that can be used as the weight function, "
            message += "please rename the column to 'weight'."
            raise NotImplementedError(message)
        is_2d = "x" in nodes_df.columns and "y" in nodes_df.columns
        is_3d = is_2d and "z" in nodes_df.columns
        if is_3d:
            raise NotImplementedError("3D coords not supported")
        if is_2d:
            node_coord_type = NodeCoordType.TWOD_COORDS
            node_coords = dict(zip(nodes_df["node"], zip(nodes_df["x"], nodes_df["y"])))
        else:
            node_coord_type = NodeCoordType.NO_COORDS
            node_coords = {}

        demands = None
        if "demand" in nodes_df.columns:
            demands = dict(zip(nodes_df["node"], nodes_df["demand"]))

        if display_data_type == DisplayDataType.COORD_DISPLAY:
            display_data = node_coords

        fixed_edges = []
        if "is_fixed" in edges_df.columns:
            fixed_edges_df = edges_df.loc[edges_df["is_fixed"]]
            fixed_edges = list(zip(fixed_edges_df["source"], fixed_edges_df["target"]))

        depots = nodes_df.loc[nodes_df["is_depot"]]["node"].to_list()
        edge_data = list(zip(edges_df["source"], edges_df["target"]))
        edge_weights = dict(zip(edge_data, edges_df["weight"]))
        return cls(
            capacity=capacity,
            comment=comment,
            demands=demands,
            depots=depots,
            dimension=len(nodes_df["node"]),
            display_data=display_data,
            display_data_type=display_data_type,
            edge_data=edge_data,
            edge_data_format=EdgeDataFormat.EDGE_LIST,
            edge_weights=edge_weights,
            edge_weight_format=edge_weight_format,
            edge_weight_type=EdgeWeightType.EXPLICIT,
            fixed_edges=fixed_edges,
            name=name,
            node_coords=node_coords,
            node_coord_type=node_coord_type,
            problem_type=problem_type,
            tours=None,
        )

    @classmethod
    def from_tsplib95(cls, problem: tsplib95.models.StandardProblem):
        """Get a TSP base model from a StandardProblem object"""

        display_data_type = (
            problem.display_data_type
            if problem.display_data_type
            else DisplayDataType.NO_DISPLAY
        )
        edge_data_format = (
            problem.edge_data_format
            if problem.edge_data_format
            else EdgeDataFormat.EDGE_LIST
        )
        edge_weight_type = problem.edge_weight_type

        # edge weight format
        edge_weight_format = problem.edge_weight_format
        if (
            not edge_weight_format
            and edge_weight_type in EdgeWeightType.__members__
            and edge_weight_type != EdgeWeightType.EXPLICIT
        ):
            edge_weight_format = EdgeWeightFormat.FUNCTION
        elif not edge_weight_format and edge_weight_type == EdgeWeightType.EXPLICIT:
            raise ValueError(
                "Edge weight type is set to EXPLICIT but no edge weight format is given"
            )
        elif not edge_weight_format:
            raise ValueError(
                "Edge weight format in StandardProblem is not set - cannot assign edge weights."
            )

        node_coord_type = (
            problem.node_coord_type
            if problem.node_coord_type
            else NodeCoordType.NO_COORDS
        )
        node_coords = None
        if node_coord_type == NodeCoordType.TWOD_COORDS:
            node_coords = {i: problem.node_coords.get(i) for i in problem.get_nodes()}
        elif node_coord_type == NodeCoordType.THREED_COORDS:
            raise NotImplementedError("3D coords not yet supported")

        return cls(
            capacity=problem.capacity,
            comment=problem.comment if problem.comment else "",
            demands=problem.demands,
            depots=problem.depots,
            dimension=problem.dimension,
            display_data=problem.display_data,
            display_data_type=display_data_type,
            edge_data=list(problem.get_edges()),
            edge_data_format=edge_data_format,
            edge_weights={
                (i, j): problem.get_weight(i, j) for i, j in problem.get_edges()
            },
            edge_weight_format=edge_weight_format,
            edge_weight_type=edge_weight_type,
            fixed_edges=problem.fixed_edges,
            name=problem.name,
            node_coords=node_coords,
            node_coord_type=node_coord_type,
            problem_type=problem.type,
            tours=problem.tours,
        )

    def to_tsplib95(self) -> tsplib95.models.StandardProblem:
        """Convert to a tsplib95 standard model"""
        weights = self.edge_weights
        if self.edge_weight_type == EdgeWeightType.EXPLICIT:
            # create a graph
            G = nx.Graph(incoming_graph_data=self.edge_data)
            nx.set_edge_attributes(G, self.edge_weights, name="weight")
            # then get the weighted adjacency matrix
            weights = nx.to_numpy_array(
                G, nodelist=list(G.nodes()).sort(), weight="weight", dtype=int
            )

        return tsplib95.models.StandardProblem(
            # capacity=self.capacity,
            comment=self.comment,
            demands=self.demands,
            depots=self.depots,
            dimension=self.dimension,
            # display_data=self.display_data,
            display_data_type=self.display_data_type,
            edge_data=self.edge_data,
            edge_data_format=self.edge_data_format,
            edge_weights=weights,
            edge_weight_format=self.edge_weight_format,
            edge_weight_type=self.edge_weight_type,
            # fixed_edges=self.fixed_edges,
            name=self.name,
            node_coords=self.node_coords,
            node_coord_type=self.node_coord_type,
            type=self.problem_type,
            # tours=self.tours,
        )

    def __set_graph_attributes(self, graph: nx.Graph) -> None:
        """Set graph attributes such as 'name' and 'comment'"""
        graph.graph["name"] = self.name
        graph.graph["comment"] = self.comment
        graph.graph["problem_type"] = self.problem_type
        graph.graph["dimension"] = self.dimension
        if not self.capacity is None:
            graph.graph["capacity"] = self.capacity

    def __set_node_attributes(self, graph: nx.Graph) -> None:
        """Set node attributes"""
        for vertex in graph.nodes():
            graph.nodes[vertex]["is_depot"] = vertex in self.depots
            if self.demands:
                graph.nodes[vertex]["demand"] = self.demands[vertex]
            if self.display_data:
                graph.nodes[vertex]["display"] = self.display_data[vertex]
            if self.node_coords:
                coords = self.node_coords[vertex]
                graph.nodes[vertex]["x"] = coords[0]
                graph.nodes[vertex]["y"] = coords[1]

    def __add_edges(self, graph: nx.Graph) -> None:
        """Add edges from edge data

        Args:
            graph: Input graph
        """
        for edge in self.edge_data:
            graph.add_edge(edge[0], edge[1])

    def __set_edge_attributes(self, graph: nx.Graph) -> None:
        """Set edge attributes for 'weight' and 'is_fixed'

        Args:
            graph: Input graph
        """
        nx.set_edge_attributes(graph, self.edge_weights, name="weight")
        fixed = {(u, v): (u, v) in self.fixed_edges for u, v in graph.edges()}
        nx.set_edge_attributes(graph, fixed, name="is_fixed")

    def get_graph(self) -> nx.Graph:
        """Get a networkx graph

        Returns:
            Undirected networkx graph with node attributes such as 'is_depot'
            and edge attributes such as 'weight' and 'is_fixed'.
        """
        G = nx.Graph()
        self.__set_graph_attributes(G)
        self.__add_edges(G)
        self.__set_edge_attributes(G)
        self.__set_node_attributes(G)
        return G


class PrizeCollectingTSP(BaseTSP):
    """Prize-collecting TSP pydantic model"""

    def get_root_vertex(self) -> Vertex:
        """Get the root vertex from the 'depots' attribute

        Returns:
            Root vertex

        Raises:
            ValueError: If the number of depots to choose from is zero or greater than 1
        """
        if len(self.depots) > 1:
            raise ValueError(
                "More than 1 depot to choose from: which depot should I choose?"
            )
        try:
            # pylint: disable=unsubscriptable-object
            return self.depots[0]
        except KeyError as key_error:
            raise ValueError("The list of depots is empty") from key_error

    def get_total_prize(self) -> Union[int, float]:
        """ "Get the total prize (demand) of all vertices"""
        if self.demands:
            return sum(self.demands.values())
        return 0


class ProfitsProblem(tsplib95.models.StandardProblem):
    """TSP with Profits Problem

    You can set `edge_removal_probability` to remove edges with this probability.
    """

    # Maximum distance of the total route in a OP.
    cost_limit = tsplib95.fields.IntegerField("COST_LIMIT")
    # The scores of the nodes of a OP are given in the form (per line)
    node_score = tsplib95.fields.DemandsField("NODE_SCORE_SECTION")
    # The optimal solution to the TSP
    tspsol = tsplib95.fields.IntegerField("TSPSOL")

    def __init__(
        self, edge_removal_probability: float = 0.0, seed: int = 0, special=None, **data
    ):
        super().__init__(special=special, **data)
        self._edge_removal_probability = edge_removal_probability
        self._seed = seed

    @property
    def edge_removal_probability(self) -> float:
        """Probability of removing an edge from the graph.

        Returns:
            Edge removal probability.

        Notes:
            It is strongly recommended to only set this value in the constructor.
        """
        return self._edge_removal_probability

    def __set_edge_attributes(self, graph: nx.Graph, names: VertexLookup) -> None:
        """Set edge attributes"""
        # add every edge with some associated metadata
        for edge in self.get_edges():
            cost: int = self.get_weight(edge[0], edge[1])
            # pylint: disable=unsupported-membership-test
            # is_fixed: bool = (u, v) in self.fixed_edges
            graph.add_edge(names[edge[0]], names[edge[1]], cost=cost)

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
            # pylint: disable=unsupported-membership-test,no-member
            is_depot = vertex in self.depots
            graph.add_node(
                names[vertex],
                prize=node_score[vertex],
                is_depot=is_depot,
            )
            demand: int = self.demands.get(vertex)
            display = self.display_data.get(vertex)
            if not demand is None:
                graph[vertex]["demand"] = demand
            if not display is None:
                graph[vertex]["display"] = display
            if self.node_coords:
                coord = self.node_coords.get(vertex)
                graph.nodes[names[vertex]]["x"] = coord[0]
                graph.nodes[names[vertex]]["y"] = coord[1]

    def get_graph(self, normalize: bool = False) -> nx.Graph:
        """Return a networkx graph instance representing the problem.

        Args:
            normalize: rename nodes to be zero-indexed
        """
        # directed graphs are fundamentally different
        graph: nx.Graph = nx.Graph() if self.is_symmetric() else nx.DiGraph()

        # set up a map from original node name to new node name
        nodes: List[Vertex] = list(self.get_nodes())
        if normalize:
            names = {n: i for i, n in enumerate(nodes)}
        else:
            names = {n: n for n in nodes}

        self.__set_node_attributes(graph, names)
        self.__set_edge_attributes(graph, names)

        # add basic graph metadata
        self.__set_graph_attributes(graph)
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
        score_dict: VertexLookup = {}
        for key, value in self.node_score.items():  # pylint: disable=no-member
            score_dict[key] = value
        return score_dict

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

    # pylint: disable=arguments-differ
    def get_edges(self, normalize: bool = False) -> EdgeList:
        """Get a list of edges in the graph

        If the `edge_removal_probability` is set in the constructor,
        then edges will be randomly removed

        Args:
            normalize: If true use the normalized vertex ids

        Returns:
            List of edges in the graph
        """
        if normalize:
            raise NotImplementedError("Normalizing edges not yet implemented")
        edges: EdgeList = list(super().get_edges())
        edges_copy = edges.copy()
        random.seed(self._seed)
        for edge in edges:
            # do not remove self-loops
            if (
                random.random() < self.edge_removal_probability
                and edge[0] != edge[1]
                and edge in edges_copy
            ):
                if self.is_symmetric() and edge[0] < edge[1]:
                    # remove both (u,v) and (v,u) in undirected case
                    edges_copy.remove(edge)
                    edges_copy.remove((edge[1], edge[0]))
                else:
                    # remove just (u,v) in directed case
                    edges_copy.remove(edge)
        return edges_copy


def is_pctsp_yes_instance(
    graph: nx.Graph, quota: int, root_vertex: Vertex, edge_list: EdgeList
) -> bool:
    """Returns true if the list of edges is a solution to the instance
    of the Prize collecting Travelling Salesman Problem.

    Args:
        graph: Undirected graph with cost function on edges and prize function on vertices
        quota: The salesman must collect at least the quota in prize money
        root_vertex: Start and finish vertex of the tour
        edge_list: Edges in the solution of the instance

    Returns:
        True if the total prize of the tour is at least the quota and the tour is a simple
        cycle that starts and ends at the root vertex. False otherwise.
    """
    if len(edge_list) < 3:
        return False
    walk = walk_from_edge_list(edge_list)
    vertex_set = set(walk)
    return (
        is_simple_cycle(graph, walk)
        and total_prize(
            nx.get_node_attributes(graph, VertexFunctionName.prize.value), vertex_set
        )
        >= quota
        and root_vertex == walk[0]
        and root_vertex == walk[len(walk) - 1]
    )
