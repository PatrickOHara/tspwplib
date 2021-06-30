"""Exceptions for Travelling Salesman Problem with Profits"""

from networkx import exception as ex


class EdgesNotAdjacentException(ex.AmbiguousSolution):
    """An edge list has been given non-adjacent edges which is ambiguous"""
