from collections import deque
from copy import copy
from util.data_structure import DataStructure

class Boykov_Kolmogorov:
    def __init__(self, g, active_storage_type, orphan_storage_type, store_parent_info, perfect_info, store_child_info):
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
        self.store_parent_info = store_parent_info
        if self.store_parent_info:
            self.parent_info = {g.get_source(): 0, g.get_target(): 0}

        self.store_child_info = store_child_info
        if self.store_child_info:
            self.child_info = dict()
            for i in range(1, self.g.dim()+1):
                self.child_info[i] = set()

        self.S = set([g.get_source()])
        self.T = set([g.get_target()])
        self.A = DataStructure(active_storage_type, [g.get_source(), g.get_target()])
        self.O = DataStructure(orphan_storage_type)

        self.perfect_info = perfect_info

    def set_distance_to_origin(self, n, distance):
        q = deque([n])
        self.parent_info[n] = distance
        visited = set([n])
        if n in self.S:
            current_tree = self.S
        else:
            current_tree = self.T
        while len(q) != 0:
            current_node = q.pop()
            if self.store_child_info:
                children = self.child_info[current_node]
            else:
                children = [k for k, v in self.parent.items() if v == current_node]
            for child in children:
                if child not in visited:
                    q.appendleft(child)
                    visited.add(child)
                    if distance == -1:
                        self.parent_info[child] = -1
                    else:
                        self.parent_info[child] = self.parent_info[current_node] + 1

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
                        if self.store_child_info:
                            self.child_info[p].add(q)
                        if self.store_parent_info:
                            if self.perfect_info:
                                self.set_distance_to_origin(q, self.parent_info[p] + 1)
                            else:
                                self.parent_info[q] = self.parent_info[p] + 1
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
                if self.store_child_info:
                    self.child_info[self.parent[q]].remove(q)
                self.parent[q] = None
                if self.store_parent_info:
                    self.set_distance_to_origin(q, -1)
                self.O.add(q)
            if p in self.T and q in self.T and new_capacity == 0:
                if self.store_child_info:
                    self.child_info[self.parent[p]].remove(p)
                self.parent[p] = None
                if self.store_parent_info:
                    self.set_distance_to_origin(p, -1)
                self.O.add(p)

    def rooted(self, n):
        source = self.g.get_source()
        target = self.g.get_target()
        if self.store_parent_info:
            try:
                distance_to_parent = self.parent_info[n]
                return distance_to_parent != -1
            except:
                return False
        else:
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
            new_parent = None
            for q, capacity in neighbors:
                if q in current_tree and capacity > 0 and self.rooted(q):
                    if self.store_parent_info:
                        if new_parent == None:
                            new_parent = q
                        if self.parent_info[q] < self.parent_info[new_parent] and self.parent_info[q] != -1:
                            new_parent = q
                    else:
                        new_parent = q
                        break
            self.parent[p] = new_parent
            if self.store_parent_info and self.perfect_info and new_parent != None:
                self.set_distance_to_origin(p, self.parent_info[new_parent] + 1)
            if self.store_child_info and new_parent != None:
                self.child_info[new_parent].add(p)
            if self.parent[p] == None:
                for q, capacity in neighbors:
                    if q in current_tree:
                        if capacity > 0:
                            if q not in self.A:
                                self.A.add(q)
                        if self.parent[q] == p:
                            if self.store_child_info:
                                self.child_info[p].remove(q)
                            self.parent[q] = None
                            if self.store_parent_info and self.perfect_info:
                                self.set_distance_to_origin(q, -1)
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
