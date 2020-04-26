from util.graph import Graph
from util.boykov_kolmogorov import Boykov_Kolmogorov as bk

my_graph = Graph.read_graph("../test_graphs/test1.graph")
my_bk = bk(my_graph)
print(my_bk.max_flow())


