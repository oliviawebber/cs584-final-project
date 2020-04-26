from util.graph import Graph
from util.boykov_kolmogorov import Boykov_Kolmogorov as bk
from util.enums import Storage

my_graph = Graph.read_graph("../test_graphs/test1.graph")
my_bk = bk(my_graph, Storage.stack)
print(my_bk.max_flow())


