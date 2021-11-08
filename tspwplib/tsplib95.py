"""Fixes for tsplib95"""

from tsplib95 import fields, transformers


class TupleT(transformers.ContainerT):
    """Transformer for tuples"""

    def pack(self, items):
        return tuple(items)

    def unpack(self, container):
        return tuple(container)


class TempAdjacencyListField(fields.TransformerField):
    """Field for an adjacency list."""

    default = dict

    @classmethod
    def build_transformer(cls):
        """Build transformer"""
        return transformers.MapT(
            key=transformers.FuncT(func=int),
            value=transformers.ListT(value=transformers.FuncT(func=int), terminal="-1"),
            sep="\n",
            terminal="-1",
        )


class TempEdgeListField(fields.TransformerField):
    """Field for a list of edges."""

    default = list

    @classmethod
    def build_transformer(cls):
        edge = TupleT(value=transformers.FuncT(func=int), size=2)
        return transformers.ListT(value=edge, terminal="-1", sep="\n")


class TempEdgeDataField(fields.TransformerField):
    """Field for edge data."""

    default = dict

    @classmethod
    def build_transformer(cls):
        adj_list = TempAdjacencyListField.build_transformer()
        edge_list = TempEdgeListField.build_transformer()
        return transformers.UnionT(edge_list, adj_list)
