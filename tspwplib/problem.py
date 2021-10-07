"""Functions and classes for datasets"""

import random
import re
from typing import List
import networkx as nx
import tsplib95
from .types import EdgeFunction, EdgeList, Vertex, VertexFunctionName, VertexLookup
from .walk import is_simple_cycle, walk_from_edge_list, total_prize

from tsplib95 import transformers
from tsplib95.fields import TransformerField

class PrizesField(TransformerField):
    """Field for demands."""

    default = dict

    @classmethod
    def build_transformer(cls):
        node = transformers.FuncT(func=int)
        demand = transformers.FuncT(func=float)
        return transformers.MapT(key=node, value=demand, sep='\n')

class ProfitsProblem(tsplib95.models.StandardProblem):
    """TSP with Profits Problem

    You can set `edge_removal_probability` to remove edges with this probability.
    """

    # Maximum distance of the total route in a OP.
    cost_limit = tsplib95.fields.IntegerField("COST_LIMIT")
    # The scores of the nodes of a OP are given in the form (per line)
    node_score = PrizesField("NODE_SCORE_SECTION")
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

    def get_edges(self, normalize: bool = False) -> EdgeList:   # pylint: disable=arguments-differ
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

    def _create_wfunc(self, special=None):
        """Overwrite create weight function"""
        if self.is_explicit() and self.edge_weight_format == "EDGE_LIST_WEIGHTS":
            return lambda i, j: self.edge_weights[(i, j)]
        return super()._create_wfunc(special=special)

    def render(self):
        # render each value by keyword
        rendered = self.as_name_dict()
        for name in list(rendered):
            value = rendered.pop(name)
            field = self.__class__.fields_by_name[name]
            if self.is_explicit() and self.edge_weight_format == "EDGE_LIST_WEIGHTS" and name == "edge_weights":
                rendered["EDGE_WEIGHT_SECTION"] = render_edge_list_weights(self.edge_weights)

            elif name in self.__dict__ or value != field.get_default_value():
                rendered[field.keyword] = field.render(value)

        # build keyword-value pairs with the separator
        kvpairs = []
        for keyword, value in rendered.items():
            sep = ':\n' if '\n' in value else ': '
            kvpairs.append(f'{keyword}{sep}{value}')
        kvpairs.append('EOF')

        # join and return the result
        return '\n'.join(kvpairs)

    @classmethod
    def parse(cls, text: str, **options):
        """Parse text into a problem instance.

        Any keyword options are passed to the class constructor. If a keyword
        argument has the same name as a field then they will collide and cause
        an error.

        Args:
            text: problem text
            options: any keyword arguments to pass to the constructor

        Returns:
            problem instance
        """
        # prepare the regex for all known keys
        keywords = '|'.join(cls.fields_by_keyword)
        sep = r'''\s*:\s*|\s*\n'''
        pattern = f'({keywords}|EOF)(?:{sep})'

        # split the whole text by known keys
        regex = re.compile(pattern, re.M)
        __, *results = regex.split(text)

        # pair keys and values
        field_keywords = results[::2]
        field_values = results[1::2]

        # parse into a dictionary
        is_edge_list_weights = False
        data = {}
        for keyword, value in zip(field_keywords, field_values):
            if keyword != 'EOF':
                field = cls.fields_by_keyword[keyword]
                name = cls.names_by_keyword[keyword]
                field_value = field.parse(value.strip())
                if name == "EDGE_WEIGHT_TYPE" and field_value == "EDGE_LIST_WEIGHTS":
                    is_edge_list_weights = True
                if name == "EDGE_WEIGHT_SECTION" and is_edge_list_weights:
                    field_value = parse_edge_list_weights(value.strip())
                data[name] = field_value

        # return as a model, letting options and field data potentially collide
        return cls(**data, **options)


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

def parse_edge_list_weights(text: str) -> EdgeFunction:
    print(text)
    return {}

def render_edge_list_weights(edge_weights: EdgeFunction) -> str:
    """Render edge weight dictionary to a string

    Args:
        edge_weights: Keys are edge tuples. Values are the weight of the edge.

    Returns:
        String representation of edge weights, including new lines.
    """
    render = ""
    for (u, v), weight in edge_weights.items():
        render += f"{u} {v} {weight}\n"
    return render
