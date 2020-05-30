from util.graph import Graph
from util.boykov_kolmogorov import Boykov_Kolmogorov as bk
from util.edmonds_karp import Edmonds_Karp as ek
from util.goldberg_tarjan import Goldberg_Tarjan as gt
from util.enums import Storage
from timeit import timeit
import os

TESTS = 10
data_structures = [Storage.queue, Storage.stack, Storage.multi_queue, Storage.multi_stack]
parameters = [True, False]
graph_path = "../test_graphs"

for g in os.listdir(graph_path):
    test_graph = Graph.read_graph(graph_path + '/' + g)
    with open('edmond_karp_results', 'a') as f:
        ek_test_instance = ek(test_graph)
        f.write(g + ',')
        f.write(timeit(ek_test_instance.max_flow, number = TESTS) / TESTS)
        f.write('\n')
    with open('goldberg_tarjan_results', 'a') as f:
        gt_test_instance = gt(test_graph)
        f.write(g + ',')
        f.write(timeit(gt_test_instance.max_flow, number = TESTS) / TESTS)
        f.write('\n')
    for data_structure in data_structures:
        for store_parent_info in parameters:
            for perfect_info in parameters:
                for store_child_info in parameters:
                    with open('boykov_kolmogorov_%s_%s%s%s_results' % (data_structure, store_parent_info, perfect_info, store_child_info), 'a') as f:
                        bk_test_instance = bk(test_graph, data_structure, data_structure, store_parent_info, perfect_info, store_child_info)
                        f.write(g + ',')
                        f.write(timeit(bk_test_instance.max_flow, number = TESTS) / TESTS)
                        f.write('\n')



#my_graph = Graph.read_graph("../test_graphs/test0-c50-n300-e72120.graph")
#my_graph = Graph.read_graph("../test_graphs/test1.graph")
#my_bk = bk(my_graph, Storage.multi_queue, Storage.multi_queue, False, False, False)
#my_ek = ek(my_graph)
#my_gt = gt(my_graph)
#print(my_bk.max_flow())
#print("BK time: " + str(timeit(my_bk.max_flow, number = TESTS) / TESTS))
#print("EK time: " + str(timeit(my_ek.max_flow, number = 1000) / 1000))

#print("GT time: " + str(timeit(my_gt.max_flow, number = TESTS) / TESTS))

#my_gt.max_flow()
#my_bk.max_flow()
