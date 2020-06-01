import random
from ortools.graph import pywrapgraph
RANDOM_SEED = 5
random.seed(RANDOM_SEED)

# This file generates all of the test graphs that are used for testing the
# empirical performance of the Boykov-Kolmogorov algorithm

capacities = [1, 5, 10, 50, 100]
number_of_nodes = list(range(500, 1000, 100))
number_of_tests = 30

for C in capacities:
    for V in number_of_nodes:
        # We use 2|V| as the lower bound on the number of edges to approximate
        # the sparse case. Using|V| directly gives many graphs that contain
        # no path between the source and target, so 2|V| helps combat this
        # while still maintaining that |E| in O(|V|) so the graph is sparse.
        number_of_edges = range(2*V, V*V, int((V*V - 2*V) / 10))
        for E in number_of_edges:
            for test_number in range(number_of_tests):
                with open('../test_graphs/test%i-c%i-n%i-e%i.graph' % (test_number, C, V, E), 'w') as f:
                    source = random.randint(1, V)
                    target = source
                    while target == source:
                        target = random.randint(1, V)
                    f.write('%i\n%i\n%i\n' % (V, source, target))

                    # We take a random sample of all possible edges to form
                    # our graph. We intentionally skip edges that don't make
                    # sense in the context of a flow graph: self edges, edges
                    # that end at the source, and edges that begin at the target
                    all_edges = list()
                    for i in range(1, V):
                        for j in range(1, V):
                            if i != j and j != source and i != target:
                                all_edges.append((i,j))
                    edges = random.sample(all_edges, E)

                    start_nodes = list([0]*E)
                    end_nodes = list([0]*E)
                    capacities = list([0]*E)

                    for i in range(E):
                        start_nodes[i], end_nodes[i] = edges[i]
                        capacities[i] = random.randint(1, C)

                    # Use the OR tools solver to find the max flow. We will
                    # use this later to validate our algorithm
                    max_flow = pywrapgraph.SimpleMaxFlow()
                    for s, e, c in zip(start_nodes, end_nodes, capacities):
                        max_flow.AddArcWithCapacity(s, e, c)
                    max_flow.Solve(source, target)
                    f.write('%i\n' % max_flow.OptimalFlow())

                    for s, e, c in zip(start_nodes, end_nodes, capacities):
                        f.write('%i %i %i\n' % (s, e, c))

