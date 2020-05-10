import random
from ortools.graph import pywrapgraph

NUM_NODES = 500
DENSE = True
RANDOM_SEED = 5
MAX_CAPACITY = 20

random.seed(RANDOM_SEED)
with open('../test_graphs/test_random.graph', 'w') as f:
    source = random.randint(1, NUM_NODES)
    target = random.randint(1, NUM_NODES)
    f.write(str(NUM_NODES) + '\n')
    f.write(str(source) + '\n')
    f.write(str(target) + '\n')

    all_edges = list()
    for i in range(1, NUM_NODES):
        for j in range(1, NUM_NODES):
            if i != j and j != source and i != target:
                all_edges.append((i,j))
    num_edges = random.randint(NUM_NODES, len(all_edges))
    if not DENSE:
        num_edges = int(num_edges / NUM_NODES)

    edges = random.sample(all_edges, num_edges)

    start_nodes = list([0]*num_edges)
    end_nodes = list([0]*num_edges)
    capacities = list([0]*num_edges)
    for i in range(num_edges):
        s, e = edges[i]
        start_nodes[i] = s
        end_nodes[i] = e
        capacities[i] = random.randint(1, MAX_CAPACITY)

    max_flow = pywrapgraph.SimpleMaxFlow()
    for s, e, c in zip(start_nodes, end_nodes, capacities):
        max_flow.AddArcWithCapacity(s, e, c)

    if max_flow.Solve(source, target) == max_flow.OPTIMAL:
        f.write(str(max_flow.OptimalFlow()) + '\n')
    else:
        print("there was an issue")

    for s, e, c in zip(start_nodes, end_nodes, capacities):
        f.write(str(s) + ' ' + str(e) + ' ' + str(c) + '\n')
