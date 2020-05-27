from collections import deque
from copy import deepcopy
from util.data_structure import DataStructure
# This class implements the Boykov-Kolmogorov algorithm for Min-Cut/Max-Flow.
# The psuedo-code this algorithm is based on is found in the paper An
# Experimental Comparison of Min-Cut/Max-Flow Algorithms for Energy Minimization
# in Vision by Yuri Boykov and Vladimir Kolmogorov

# g: the graph we want to find the max flow of
# active_storage_type: the data structure that we should use for the set of active
#   nodes in the algorithm
# orphan_storage_type: the data structure that we should use for the set of
#   orphaned nodes in the algorithm
# store_parent_info: a boolean value indicating if we should store information
#   about how far a parent node is from the source or target node, depending
#   on if it is in the source tree or target tree
# perfect_info: a boolean value indicating whether the information stored when
#   store_parent_info is True should be perfect. If True, we gurantee that the
#   information stored about a parent's distance to a root node is always optimal
#   if false, we only gurantee that this information is correct but not optimal
# store_child_info: a boolean value indicating whether we should be a set of
#   child nodes for each parent. If true, each parent has immediate access
#   to its set of children. If false, the parent dictionary has to be used
#   to reconstruct this information.

class Boykov_Kolmogorov:
    def __init__(self, g, active_storage_type, orphan_storage_type, store_parent_info, perfect_info, store_child_info):
        self.g = deepcopy(g)
        self.g_res = deepcopy(g)
        sz = self.g_res.dim()
        # Setup the reverse edges in our residual graph
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

        # S and T are the sets of nodes belonging to the trees rooted by the source
        # and target nodes respectively
        self.S = set([g.get_source()])
        self.T = set([g.get_target()])
        self.A = DataStructure(active_storage_type, [g.get_source(), g.get_target()])
        self.O = DataStructure(orphan_storage_type)

        self.perfect_info = perfect_info

    # Sets the distance from node n to the root of the tree it belongs to to
    # distance. We perform the update by doing BFS from n to any nodes that are
    # flagged as n's children
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
            # If we store the child set, use it. Otherwise we need to construct
            # it from the parent dictionary
            if self.store_child_info:
                children = self.child_info[current_node]
            else:
                children = [k for k, v in self.parent.items() if v == current_node]
            for child in children:
                if child not in visited:
                    q.appendleft(child)
                    visited.add(child)
                    # -1 is used as a flag of invalid distance so it should be
                    # set directly, otherwise the child is now 1 step further
                    # than its parent
                    if distance == -1:
                        self.parent_info[child] = -1
                    else:
                        self.parent_info[child] = self.parent_info[current_node] + 1

    # Returns the path from source to target, where s_node and t_node provide
    # the edge linking the S set section of the path with the T set section
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

    # Both trees S and T attempt to grow by adding active nodes to their sets
    # this process repeats until the two tree encounter one another
    def grow(self):
        while self.A.length():
            p = self.A.get()
            if p in self.S:
                # if p is in the source tree, we look at its outgoing neighbors
                # to find new nodes
                neighbors = self.g_res.get_out_neighbors(p)
                current_tree = self.S
                other_tree = self.T
            else:
                # if p is in the target tree, we look at its incoming neighbors
                # to find new nodes
                neighbors = self.g_res.get_in_neighbors(p)
                current_tree = self.T
                other_tree = self.S
            for q, capacity in neighbors:
                if capacity > 0:
                    # Found a free node with spare capacity, so add it to our tree
                    if q not in self.S and q not in self.T:
                        current_tree.add(q)
                        self.parent[q] = p
                        if self.store_child_info:
                            self.child_info[p].add(q)
                        if self.store_parent_info:
                            # if we store perfect info, this update may need to
                            # be pushed to all children of q
                            if self.perfect_info:
                                self.set_distance_to_origin(q, self.parent_info[p] + 1)
                            else:
                                self.parent_info[q] = self.parent_info[p] + 1
                        self.A.add(q)
                    # Encountered the other tree, so return an augmenting path
                    if q in other_tree:
                        # we may not have fully explored p, so it will still
                        # be active
                        self.A.add(p)
                        if current_tree == self.S:
                            return self.path(p, q)
                        else:
                            return self.path(q, p)
        return None

    # Given an augmenting path P, push as much flow across this path as we can
    # Turn any nodes that are part of saturated edges into orphans
    def augment(self, P):
        pairs = [(P[i], P[i+1]) for i in range(len(P)-1)]
        delta = min([self.g_res.get_edge(p, q) for p,q in pairs])
        self.flow += delta
        for p, q in pairs:
            # push our new flow along edges
            new_capacity = self.g_res.get_edge(p, q) - delta
            self.g_res.add_edge(p, q, new_capacity)
            new_residual = self.g_res.get_edge(q,p) + delta
            self.g_res.add_edge(q, p, new_residual)
            # In source tree, the target of an edge is the orphan
            if p in self.S and q in self.S and new_capacity == 0:
                if self.store_child_info:
                    self.child_info[self.parent[q]].remove(q)
                self.parent[q] = None
                if self.store_parent_info:
                    self.set_distance_to_origin(q, -1)
                self.O.add(q)
            # In target tree, the source side of an edge is the orphan
            if p in self.T and q in self.T and new_capacity == 0:
                if self.store_child_info:
                    self.child_info[self.parent[p]].remove(p)
                self.parent[p] = None
                if self.store_parent_info:
                    self.set_distance_to_origin(p, -1)
                self.O.add(p)

    # Checks whether a node n has a connection back to the root of a tree,
    # either source or target
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
