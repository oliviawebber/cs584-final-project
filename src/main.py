from util.graph import Graph
from util.boykov_kolmogorov import Boykov_Kolmogorov as bk
from util.edmonds_karp import Edmonds_Karp as ek
from util.goldberg_tarjan import Goldberg_Tarjan as gt
from util.enums import Storage
from timeit import timeit
import os
import shutil

TESTS = 10
data_structures = [Storage.queue, Storage.stack, Storage.multi_queue, Storage.multi_stack]
parameters = [True, False]
graph_path = "../test_graphs"
complete_path = "../complete_tests"
results = "../results/"

for g in os.listdir(graph_path):
    print("Working on graph %s" % g)
    test_graph = Graph.read_graph(graph_path + '/' + g)
    print("Starting Edmond-Karp Test...", end=" ")
    with open(results + 'edmond_karp_results', 'a') as f:
        ek_test_instance = ek(test_graph)
        f.write(g + ',')
        f.write(str(timeit(ek_test_instance.max_flow, number = TESTS) / TESTS))
        f.write('\n')
    print("done")
    print("Starting Goldberg-Tarjan Test...", end=" ")
    with open(results + 'goldberg_tarjan_results', 'a') as f:
        gt_test_instance = gt(test_graph)
        f.write(g + ',')
        f.write(str(timeit(gt_test_instance.max_flow, number = TESTS) / TESTS))
        f.write('\n')
    print("done")
    for data_structure in data_structures:
        for store_parent_info in parameters:
            for perfect_info in parameters:
                for store_child_info in parameters:
                    print("Starting Boykov-Kolmogorov (%s,%s,%s,%s) Test..." % (data_structure, store_parent_info, perfect_info, store_child_info), end=" ")
                    with open(results + 'boykov_kolmogorov_%s_%s%s%s_results' % (data_structure, store_parent_info, perfect_info, store_child_info), 'a') as f:
                        bk_test_instance = bk(test_graph, data_structure, data_structure, store_parent_info, perfect_info, store_child_info)
                        f.write(g + ',')
                        f.write(str(timeit(bk_test_instance.max_flow, number = TESTS) / TESTS))
                        f.write('\n')
                    print("done")
    print("Done with graph %s" % g)
    shutil.move(graph_path + '/' + g, complete_path + '/' + g)
