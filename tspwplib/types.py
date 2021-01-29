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
