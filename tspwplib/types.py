"""Type hinting and names"""

from enum import Enum, IntEnum
from typing import Dict, List, Tuple

# vertex data structures
Vertex = int
VertexFunction = Dict[Vertex, int]
VertexList = List[Vertex]
VertexLookup = Dict[Vertex, Vertex]

# edge data structures
Edge = Tuple[Vertex, Vertex]
EdgeList = List[Edge]
EdgeFunction = Dict[Vertex, VertexFunction]

# path data structures
DisjointPaths = Tuple[VertexList, VertexList]


class VertexFunctionName(str, Enum):
    """Valid names of functions on vertices"""

    demand = "demand"
    prize = "prize"


class EdgeFunctionName(str, Enum):
    """Valid names of functions on edges"""

    cost = "cost"
    weight = "weight"


class GraphName(str, Enum):
    """Names of TSPlib instances"""

    eil76 = "eil76"
    rat195 = "rat195"
    st70 = "st70"
    vm1748 = "vm1748"


class Generation(str, Enum):
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
