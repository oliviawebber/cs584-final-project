import random
from ortools.graph import pywrapgraph

NUM_NODES = 1000
DENSITY = 0
RANDOM_SEED = 5
MAX_CAPACITY = 20

random.seed(RANDOM_SEED)
with open('../test_graphs/test_random.graph', 'w') as f:
    source = random.randint(1, NUM_NODES)
    target = random.randint(1, NUM_NODES)
    f.write(str(NUM_NODES) + '\n')
    f.write(str(source) + '\n')
    f.write(str(target) + '\n')
    num_edges = random.randint(1,10)*NUM_NODES*((NUM_NODES*DENSITY) + 1)
    start_nodes = list([0]*num_edges)
    end_nodes = list([0]*num_edges)
    capacities = list([0]*num_edges)
    for i in range(num_edges):
        s = random.randint(1, NUM_NODES)
        e = random.randint(1, NUM_NODES)
        while s == e:
            s = random.randint(1, NUM_NODES)
            e = random.randint(1, NUM_NODES)
        start_nodes[i] = s
        end_nodes[i] = e
        capacities[i] = random.randint(1, NUM_NODES)

    max_flow = pywrapgraph.SimpleMaxFlow()
    for s, e, c in zip(start_nodes, end_nodes, capacities):
        max_flow.AddArcWithCapacity(s, e, c)

    max_flow.Solve(source, target)
    f.write(str(max_flow.OptimalFlow()) + '\n')

    for s, e, c in zip(start_nodes, end_nodes, capacities):
        f.write(str(s) + ' ' + str(e) + ' ' + str(c) + '\n')
