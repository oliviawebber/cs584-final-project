from util.graph import Graph
from util.boykov_kolmogorov import Boykov_Kolmogorov as bk
from util.enums import Storage

my_graph = Graph.read_graph("../test_graphs/test_random.graph")
my_bk = bk(my_graph, Storage.multi_queue, Storage.multi_queue)
print("BK max-flow: " + str(my_bk.max_flow()))
print("Actual max-flow: " + str(my_graph.get_max_flow()))


