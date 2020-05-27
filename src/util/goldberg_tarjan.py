from collections import deque
from copy import deepcopy

class Goldberg_Tarjan:
    def __init__(self,g):
        self.g = deepcopy(g)
        self.flow = dict()
        self.source = g.get_source()
        self.target = g.get_target()
        sz = self.g.dim()
        # setup preflow
        for i in range(1, sz + 1):
            for j in range(1, sz + 1):
                self.flow[(i,j)] = 0
                self.flow[(j,i)] = 0
        for v,capacity in g.get_out_neighbors(self.source):
            if capacity == -1:
                self.flow[(self.source, v)] = 0
                self.flow[(v, self.source)] = 0
            else:
                self.flow[(self.source, v)] = capacity
                self.flow[(v, self.source)] = -capacity

        # setup labels and excesses
        self.label = {self.source: sz}
        self.excess = dict()
        for i in range(1, sz + 1):
            if i != self.source:
                self.label[i] = 0
                self.excess[i] = self.flow[(self.source,i)]

        # setup edge sets
        self.edge_set = dict()
        self.first_edge = dict()
        for i in range(1, sz + 1):
            self.edge_set[i] = deque(g.get_out_neighbors(i))
            try:
                self.first_edge[i] = self.edge_set[i][0]
            except IndexError:
                self.first_edge[i] = None


    def push(self, v, w):
        delta = min([self.excess[v], self.g.get_edge(v, w) - self.flow[(v,w)]])
        self.flow[(v,w)] += delta
        self.flow[(w,v)] -= delta
        self.excess[v] -= delta
        self.excess[w] += delta
        if self.excess[v] <= 0:
            self.active[v] = False
        if self.excess[w] > 0 and w != self.target and w != self.source:
            self.active[w] = True
            self.Q.append(w)

    def relabel(self, v):
        try:
            min_labeling = min([self.label[w] for w,capacity in self.g.get_out_neighbors(v) if capacity - self.flow[(v,w)] > 0])
        except ValueError:
            self.active[v] = False
            self.label[v] += 1
            return
        self.label[v] = min_labeling + 1
        if self.label[v] == self.g.dim():
            self.active[v] = False

    def push_relabel(self, v):
        current_edge = self.edge_set[v][0]
        w,capacity = current_edge
        if self.active[v] and capacity - self.flow[(v,w)] > 0 and self.label[v] == self.label[w] + 1:
            self.push(v, w)
        else:
            old_edge = self.edge_set[v].popleft()
            self.edge_set[v].append(old_edge)
            if self.edge_set[v][0] == self.first_edge[v]:
                self.relabel(v)

    def discharge(self):
        self.Q = deque()
        self.active = dict()
        # setup initial active nodes
        for node in self.g.get_intermediate_nodes():
            if self.g.get_edge(self.source, node) > 0:
                self.Q.append(node)
                self.active[node] = True
            else:
                self.active[node] = False

        while len(self.Q):
            current_node = self.Q.popleft()
            current_label = self.label[current_node]
            while self.excess[current_node] > 0 and current_label == self.label[current_node]:
                self.push_relabel(current_node)
            if self.active[current_node]:
                self.Q.append(current_node)

    def max_flow(self):
        self.discharge()
        maximum_flow = 0
        for i in range(1, self.g.dim() + 1):
            maximum_flow += self.flow[(i, self.target)]
        return maximum_flow

