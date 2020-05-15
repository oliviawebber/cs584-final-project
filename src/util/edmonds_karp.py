from collections import deque
from copy import copy

class Edmonds_Karp:
    def __init__(self, g):
        self.g = g
        self.g_res = copy(g)
        sz = self.g_res.dim()
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
        v = self.g_res.get_source()
        target = self.g_res.get_target()
        parent = {v: None}
        visited = set([v])
        q = deque([v])
        while len(q) != 0:
            current_node = q.pop()
            if current_node == target:
                p = []
                while current_node != None:
                    p.append(current_node)
                    current_node = parent[current_node]
                p.reverse()
                return p

            for neighbor, capacity in self.g_res.get_out_neighbors(current_node):
                if neighbor not in visited and capacity > 0:
                    parent[neighbor] = current_node
                    visited.add(neighbor)
                    q.appendleft(neighbor)
        return None

    def augment(self, p):
        pairs = [(p[i], p[i+1]) for i in range(len(p)-1)]
        delta = min([self.g_res.get_edge(p, q) for p, q in pairs])
        self.flow += delta
        for p, q in pairs:
            new_capacity = self.g_res.get_edge(p, q) - delta
            self.g_res.add_edge(p, q, new_capacity)
            new_residual = self.g_res.get_edge(q, p) + delta
            self.g_res.add_edge(q, p, new_residual)

    def max_flow(self):
        while True:
            p = self.BFS()
            if p is None:
                break
            self.augment(p)
        return self.flow
