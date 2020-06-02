from collections import deque
from copy import deepcopy
# This class implements the Edmonds Karp algorithm for Max-Flow/Min-Cut. It is
# based off the psuedo-code for this algorithm found in Introduction to Algorithms
# 3rd Edition by Cormen, Leiserson, Rivest, Stein.

class Edmonds_Karp:
    def __init__(self, g):
        self.g = deepcopy(g)
        self.g_res = deepcopy(g)
        sz = self.g_res.dim()
        # Initialize backwards edges in the residual graph
        for i in range(1, sz + 1):
            for j in range(1, sz + 1):
                forward_edge = self.g_res.get_edge(i, j)
                backward_edge = self.g_res.get_edge(j, i)
                if forward_edge != -1 and backward_edge == -1:
                    self.g_res.add_edge(j, i, 0)
                if forward_edge == -1 and backward_edge != -1:
                    self.g_res.add_edge(i, j, 0)

        self.flow = 0

    def BFS(self):
        # Performs breadth first search between the source and target nodes, in
        # the residual graph
        v = self.g_res.get_source()
        target = self.g_res.get_target()
        parent = {v: None}
        visited = set([v])
        q = deque([v])
        while len(q) != 0:
            current_node = q.pop()
            if current_node == target:
                # Create the path by tracing back through parents until we reach
                # the source
                p = []
                while current_node != None:
                    p.append(current_node)
                    current_node = parent[current_node]
                p.reverse()
                return p

            # Search along our outgoing edges for a neighbor
            for neighbor, capacity in self.g_res.get_out_neighbors(current_node):
                if neighbor not in visited and capacity > 0:
                    parent[neighbor] = current_node
                    visited.add(neighbor)
                    q.appendleft(neighbor)
        return None

    def augment(self, p):
        pairs = [(p[i], p[i+1]) for i in range(len(p)-1)]
        # delta is the maximum flow we can push along the augmenting path
        # we have found
        delta = min([self.g_res.get_edge(p, q) for p, q in pairs])
        self.flow += delta
        # for each edge in the augmenting path, push delta flow towards the
        # target and delta flow back along the residual edges
        for p, q in pairs:
            new_capacity = self.g_res.get_edge(p, q) - delta
            self.g_res.add_edge(p, q, new_capacity)
            new_residual = self.g_res.get_edge(q, p) + delta
            self.g_res.add_edge(q, p, new_residual)

    def max_flow(self):
        while True:
            p = self.BFS()
            # If we can't find an augmenting path we're done
            if p is None:
                break
            self.augment(p)
        assert self.flow == self.g.get_max_flow()
        return self.flow
