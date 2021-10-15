"""Type hinting and names"""

from datetime import datetime, timezone
from enum import Enum, IntEnum
from typing import Any, Dict, List, Tuple, Union

# vertex data structures
Vertex = int
VertexFunction = Dict[Vertex, int]
VertexList = List[Vertex]
VertexLookup = Dict[Vertex, Vertex]
VertexProperties = Dict[Vertex, Dict[str, Any]]

# edge data structures
Edge = Tuple[Vertex, Vertex]
MultiEdge = Tuple[Vertex, Vertex, int]
EdgeList = List[Union[Edge, MultiEdge]]
EdgeFunction = Dict[Union[Edge, MultiEdge], int]
EdgeProperties = Dict[Union[Edge, MultiEdge], Dict[str, Any]]

# path data structures
DisjointPaths = Tuple[VertexList, VertexList]

# pylint: disable=invalid-name,too-few-public-methods


class StrEnumMixin:
    """When the `str(...)` method is called on this mixin, return the value of the Enum."""

    def __str__(self):
        try:
            return self.value()
        except TypeError:
            return self


class EdgeWeightType(StrEnumMixin, str, Enum):
    """Specifies how the edge weights (or distances) are given"""

    EXPLICIT = "EXPLICIT"  # Weights are listed explicitly in the corresponding section
    EUC_2D = "EUC_2D"  # Weights are Euclidean distances in 2-D
    EUC_3D = "EUC_3D"  # Weights are Euclidean distances in 3-D
    MAX_2D = "MAX_2D"  # Weights are maximum distances in 2-D
    MAX_3D = "MAX_3D"  # Weights are maximum distances in 3-D
    MAN_2D = "MAN_2D"  # Weights are Manhattan distances in 2-D
    MAN_3D = "MAN_3D"  # Weights are Manhattan distances in 3-D
    CEIL_2D = "CEIL_2D"  # Weights are Euclidean distances in 2-D rounded up
    GEO = "GEO"  # Weights are geographical distances
    ATT = "ATT"  # Special distance function for problems att48 and att532
    XRAY1 = (
        "XRAY1"  # Special distance function for crystallography problems (Version 1)
    )
    XRAY2 = (
        "XRAY2"  # Special distance function for crystallography problems (Version 2)
    )
    SPECIAL = "SPECIAL"  # There is a special distance function documented elsewhere


class EdgeWeightFormat(StrEnumMixin, str, Enum):
    """Describes the format of the edge weights if they are given explicitly"""

    FUNCTION = "FUNCTION"  # Weights are given by a function (see above)
    FULL_MATRIX = "FULL_MATRIX"  # Weights are given by a full matrix
    UPPER_ROW = (
        "UPPER_ROW"  # Upper triangular matrix (row-wise without diagonal entries)
    )
    LOWER_ROW = (
        "LOWER_ROW"  # Lower triangular matrix (row-wise without diagonal entries)
    )
    UPPER_DIAG_ROW = "UPPER_DIAG_ROW"  # Upper triangular matrix
    LOWER_DIAG_ROW = "LOWER_DIAG_ROW"  # Lower triangular matrix
    UPPER_COL = (
        "UPPER_COL"  # Upper triangular matrix (column-wise without diagonal entries)
    )
    LOWER_COL = (
        "LOWER_COL"  # Lower triangular matrix (column-wise without diagonal entries)
    )
    UPPER_DIAG_COL = "UPPER_DIAG_COL"  # Upper triangular matrix
    LOWER_DIAG_COL = "LOWER_DIAG_COL"  # Lower triangular matrix


class EdgeDataFormat(StrEnumMixin, str, Enum):
    """How the edges are listed.

    Notes:
        This does not include edge attributes. It is only the edge IDs.
    """

    EDGE_LIST = "EDGE_LIST"
    ADJ_LIST = "ADJ_LIST"


class NodeCoordType(StrEnumMixin, str, Enum):
    """How node co-ordinates are represented"""

    TWOD_COORDS = "TWOD_COORDS"  # Nodes are specified by coordinates in 2-D
    THREED_COORDS = "THREED_COORDS"  # Nodes are specified by coordinates in 3-D
    NO_COORDS = "NO_COORDS"  # The nodes do not have associated coordinates


class DisplayDataType(StrEnumMixin, str, Enum):
    """How visualisation should be done."""

    COORD_DISPLAY = "COORD_DISPLAY"  # Display is generated from the node coordinates
    TWOD_DISPLAY = "TWOD_DISPLAY"  # Explicit coordinates in 2-D are given
    NO_DISPLAY = "NO_DISPLAY"  # No graphical display is possible


# NodeCoords = Dict[Vertex, Union[Tuple[float, float], Tuple[float, float, float]]]
NodeCoords = Dict[Vertex, Tuple[float, float]]


class VertexFunctionName(StrEnumMixin, str, Enum):
    """Valid names of functions on vertices"""

    demand = "demand"
    prize = "prize"


class EdgeFunctionName(StrEnumMixin, str, Enum):
    """Valid names of functions on edges"""

    cost = "cost"
    weight = "weight"


class GraphName(StrEnumMixin, str, Enum):
    """Names of TSPlib instances"""

    a280 = "a280"
    ali535 = "ali535"
    att48 = "att48"
    att532 = "att532"
    bayg29 = "bayg29"
    bays29 = "bays29"
    berlin52 = "berlin52"
    bier127 = "bier127"
    brazil58 = "brazil58"
    brd14051 = "brd14051"
    brg180 = "brg180"
    burma14 = "burma14"
    ch130 = "ch130"
    ch150 = "ch150"
    d198 = "d198"
    d493 = "d493"
    d657 = "d657"
    d1291 = "d1291"
    d1655 = "d1655"
    d2103 = "d2103"
    d15112 = "d15112"
    d18512 = "d18512"
    dantzig42 = "dantzig42"
    dsj1000 = "dsj1000"
    eil51 = "eil51"
    eil76 = "eil76"
    eil101 = "eil101"
    fl417 = "fl417"
    fl1400 = "fl1400"
    fl1577 = "fl1577"
    fl3795 = "fl3795"
    fnl4461 = "fnl4461"
    fri26 = "fri26"
    gil262 = "gil262"
    gr17 = "gr17"
    gr21 = "gr21"
    gr24 = "gr24"
    gr48 = "gr48"
    gr96 = "gr96"
    gr120 = "gr120"
    gr137 = "gr137"
    gr202 = "gr202"
    gr229 = "gr229"
    gr431 = "gr431"
    gr666 = "gr666"
    hk48 = "hk48"
    kroA100 = "kroA100"
    kroB100 = "kroB100"
    kroC100 = "kroC100"
    kroD100 = "kroD100"
    kroE100 = "kroE100"
    kroA150 = "kroA150"
    kroB150 = "kroB150"
    kroA200 = "kroA200"
    kroB200 = "kroB200"
    lin105 = "lin105"
    lin318 = "lin318"
    linhp318 = "linhp318"
    nrw1379 = "nrw1379"
    p654 = "p654"
    pa561 = "pa561"
    pcb442 = "pcb442"
    pcb1173 = "pcb1173"
    pcb3038 = "pcb3038"
    pla7397 = "pla7397"
    pla33810 = "pla33810"
    pla85900 = "pla85900"
    pr76 = "pr76"
    pr107 = "pr107"
    pr124 = "pr124"
    pr136 = "pr136"
    pr144 = "pr144"
    pr152 = "pr152"
    pr226 = "pr226"
    pr264 = "pr264"
    pr299 = "pr299"
    pr439 = "pr439"
    pr1002 = "pr1002"
    pr2392 = "pr2392"
    rat99 = "rat99"
    rat195 = "rat195"
    rat575 = "rat575"
    rat783 = "rat783"
    rd100 = "rd100"
    rd400 = "rd400"
    rl1304 = "rl1304"
    rl1323 = "rl1323"
    rl1889 = "rl1889"
    rl5915 = "rl5915"
    rl5934 = "rl5934"
    rl11849 = "rl11849"
    si175 = "si175"
    si535 = "si535"
    si1032 = "si1032"
    st70 = "st70"
    swiss42 = "swiss42"
    ts225 = "ts225"
    tsp225 = "tsp225"
    u159 = "u159"
    u574 = "u574"
    u724 = "u724"
    u1060 = "u1060"
    u1432 = "u1432"
    u1817 = "u1817"
    u2152 = "u2152"
    u2319 = "u2319"
    ulysses16 = "ulysses16"
    ulysses22 = "ulysses22"
    usa13509 = "usa13509"
    vm1084 = "vm1084"
    vm1748 = "vm1748"


class LondonaqGraphName(StrEnumMixin, str, Enum):
    """Names of graphs with London air quality forecasts"""

    laqkxA = "laqkxA"
    laqtinyA = "laqtinyA"


class LondonaqTimestamp(Enum):
    """Timestamps of the forecasts for London air quality forecasts"""

    A = datetime(2021, 10, 13, 8, 0, 0, tzinfo=timezone.utc)  # 9am BST


class LondonaqLocation(StrEnumMixin, str, Enum):
    """Names of locations that the London air quality graph is centered upon"""

    bb = "Big Ben"
    kx = "King's Cross"
    tiny = "King's Cross"
    ro = "Royal Observatory Greenwich"
    ws = "Wembley Stadium"


class LondonaqLocationShort(StrEnumMixin, str, Enum):
    """Short codes for londonaq locations"""

    bb = "bb"
    kx = "kx"
    tiny = "tiny"
    ro = "ro"
    ws = "ws"


class Generation(StrEnumMixin, str, Enum):
    """Generations of TSPwP problem instances"""

    gen1 = "gen1"
    gen2 = "gen2"
    gen3 = "gen3"
    gen4 = "gen4"


class Alpha(IntEnum):
    """Ratio between profit/cost limit and profit/cost of TSP solution"""

    fifty = 50


class OptimalSolutionTSP(IntEnum):
    """Value of optimal solutions to TSP instances"""

    a280 = 2579
    ali535 = 202339
    att48 = 10628
    att532 = 27686
    bayg29 = 1610
    bays29 = 2020
    berlin52 = 7542
    bier127 = 118282
    brazil58 = 25395
    brd14051 = 469385
    brg180 = 1950
    burma14 = 3323
    ch130 = 6110
    ch150 = 6528
    d198 = 15780
    d493 = 35002
    d657 = 48912
    d1291 = 50801
    d1655 = 62128
    d2103 = 80450
    d15112 = 1573084
    d18512 = 645238
    dantzig42 = 699
    dsj1000 = 18659688  # (EUC_2D)
    # dsj1000 = 18660188 # (CEIL_2D)    # NOTE breaks keys
    eil51 = 426
    eil76 = 538
    eil101 = 629
    fl417 = 11861
    fl1400 = 20127
    fl1577 = 22249
    fl3795 = 28772
    fnl4461 = 182566
    fri26 = 937
    gil262 = 2378
    gr17 = 2085
    gr21 = 2707
    gr24 = 1272
    gr48 = 5046
    gr96 = 55209
    gr120 = 6942
    gr137 = 69853
    gr202 = 40160
    gr229 = 134602
    gr431 = 171414
    gr666 = 294358
    hk48 = 11461
    kroA100 = 21282
    kroB100 = 22141
    kroC100 = 20749
    kroD100 = 21294
    kroE100 = 22068
    kroA150 = 26524
    kroB150 = 26130
    kroA200 = 29368
    kroB200 = 29437
    lin105 = 14379
    lin318 = 42029
    linhp318 = 41345
    nrw1379 = 56638
    p654 = 34643
    pa561 = 2763
    pcb442 = 50778
    pcb1173 = 56892
    pcb3038 = 137694
    pla7397 = 23260728
    pla33810 = 66048945
    pla85900 = 142382641
    pr76 = 108159
    pr107 = 44303
    pr124 = 59030
    pr136 = 96772
    pr144 = 58537
    pr152 = 73682
    pr226 = 80369
    pr264 = 49135
    pr299 = 48191
    pr439 = 107217
    pr1002 = 259045
    pr2392 = 378032
    rat99 = 1211
    rat195 = 2323
    rat575 = 6773
    rat783 = 8806
    rd100 = 7910
    rd400 = 15281
    rl1304 = 252948
    rl1323 = 270199
    rl1889 = 316536
    rl5915 = 565530
    rl5934 = 556045
    rl11849 = 923288
    si175 = 21407
    si535 = 48450
    si1032 = 92650
    st70 = 675
    swiss42 = 1273
    ts225 = 126643
    tsp225 = 3916
    u159 = 42080
    u574 = 36905
    u724 = 41910
    u1060 = 224094
    u1432 = 152970
    u1817 = 57201
    u2152 = 64253
    u2319 = 234256
    ulysses16 = 6859
    ulysses22 = 7013
    usa13509 = 19982859
    vm1084 = 239297
    vm1748 = 336556
