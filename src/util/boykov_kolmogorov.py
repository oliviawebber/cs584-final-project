from collections import deque
from copy import copy
from util.data_structure import DataStructure

class Boykov_Kolmogorov:
    def __init__(self, g, active_storage_type, orphan_storage_type):
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
        self.parent = {g.get_source(): None, g.get_target(): None}

        self.S = set([g.get_source()])
        self.T = set([g.get_target()])
        self.A = DataStructure(active_storage_type, [g.get_source(), g.get_target()])
        self.O = DataStructure(orphan_storage_type)

    def path(self, s_node, t_node):
        s_path = [s_node]
        s_start = self.g.get_source()
        p = s_path[0]
        while p != s_start:
            p = self.parent[p]
            s_path.append(p)

        t_path = [t_node]
        t_end = self.g.get_target()
        p = t_path[0]
        while p != t_end:
            p = self.parent[p]
            t_path.append(p)

        s_path.reverse()
        return s_path + t_path

    def grow(self):
        while self.A.length():
            p = self.A.get()
            if p in self.S:
                neighbors = self.g_res.get_out_neighbors(p)
                current_tree = self.S
                other_tree = self.T
            else:
                neighbors = self.g_res.get_in_neighbors(p)
                current_tree = self.T
                other_tree = self.S
            for q, capacity in neighbors:
                if capacity > 0:
                    if q not in self.S and q not in self.T:
                        current_tree.add(q)
                        self.parent[q] = p
                        self.A.add(q)
                    if q in other_tree:
                        self.A.add(p)
                        if current_tree == self.S:
                            return self.path(p, q)
                        else:
                            return self.path(q, p)
        return None

    def augment(self, P):
        pairs = [(P[i], P[i+1]) for i in range(len(P)-1)]
        delta = min([self.g_res.get_edge(p, q) for p,q in pairs])
        self.flow += delta
        for p, q in pairs:
            new_capacity = self.g_res.get_edge(p, q) - delta
            self.g_res.add_edge(p, q, new_capacity)
            new_residual = self.g_res.get_edge(q,p) + delta
            self.g_res.add_edge(q, p, new_residual)
            if p in self.S and q in self.S and new_capacity == 0:
                self.parent[q] = None
                self.O.add(q)
            if p in self.T and q in self.T and new_capacity == 0:
                self.parent[p] = None
                self.O.add(p)

    def rooted(self, n):
        source = self.g.get_source()
        target = self.g.get_target()
        while n != None and n != source and n != target:
            n = self.parent[n]
        return n != None

    def adopt(self):
        while self.O.length():
            p = self.O.get()
            if p in self.S:
                current_tree = self.S
                neighbors = self.g_res.get_in_neighbors(p)
            else:
                current_tree = self.T
                neighbors = self.g_res.get_out_neighbors(p)
            for q, capacity in neighbors:
                if q in current_tree and capacity > 0 and self.rooted(q):
                    self.parent[p] = q
            if self.parent[p] == None:
                for q, capacity in neighbors:
                    if q in current_tree:
                        if capacity > 0:
                            if q not in self.A:
                                self.A.add(q)
                        if self.parent[q] == p:
                            self.parent[q] = None
                            self.O.add(q)
                current_tree.remove(p)
                if p in self.A:
                    self.A.remove(p)

    def max_flow(self):
        while True:
            P = self.grow()
            if P is None:
                break
            self.augment(P)
            self.adopt()
        return self.flow
