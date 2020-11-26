"""Type hinting and names"""

from enum import Enum


class InstanceName(str, Enum):
    """Names of TSPlib instances"""

    eil76 = "eil76"
    rat195 = "rat195"
    st70 = "st70"
    vm1748 = "vm1748"


class Generation(Enum):
    """Generations of TSPwP problem instances"""

    one = "gen1"
    two = "gen2"
    three = "gen3"
    four = "gen4"


class Alpha(Enum):
    """Ratio between profit/cost limit and profit/cost of TSP solution"""

    fifty = 50
