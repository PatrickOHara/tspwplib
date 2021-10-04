"""Exceptions for Travelling Salesman Problem with Profits"""

from networkx import exception as ex


class EdgesNotAdjacentException(ex.AmbiguousSolution):
    """An edge list has been given non-adjacent edges which is ambiguous"""


class NotSimpleException(ex.NetworkXException):
    """A path, cycle or walk is not simple"""


class NotSimpleCycleException(NotSimpleException):
    """The walk was not a simple cycle"""


class NotSimplePathException(NotSimpleException):
    """The walk was not a simple path"""


class UnexpectedSelfLoopException(ex.NetworkXException):
    """A self loop was found where it wasn't exprected"""
