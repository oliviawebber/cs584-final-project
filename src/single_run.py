from util.graph import Graph
from util.goldberg_tarjan import Goldberg_Tarjan as gt


g = Graph.read_graph('../test_graphs/test0-c50-n300-e600.graph')
my_gt = gt(g)
my_gt.max_flow()
