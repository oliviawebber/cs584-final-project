# Defines a class to implement a Graph G = (V,E), where V and E are a vertex
# and an edge set. Our implementation assumes nodes labels of the form i where
# i is a number in [1,n]. We implement the edge set using an adjacency matrix.
class Graph:
    def __init__(self, n):
        self.adjacency_matrix = [[-1 for x in range(n)] for x in range(n)]
        self.size = n
        self.source = 0
        self.target = 0

    def __str__(self):
        return self.adjacency_matrix.__str__()

    def dim(self):
        return self.size

    def add_edge(self, start, end, capacity):
        start -= 1 # convert from node number to array index
        end -= 1

        if start < 0 or start >= self.size or end < 0 or end >= self.size:
            return
        self.adjacency_matrix[start][end] = capacity

    def get_edge(self, start, end):
        start -= 1 # convert from node number to array index
        end -= 1

        if start < 0 or start >= self.size or end < 0 or end >= self.size:
            return None
        return self.adjacency_matrix[start][end]

    def set_source(self, n):
        if n < 1 or n > self.size:
            return None
        self.source = n

    def get_source(self):
        return self.source

    def set_target(self, n):
        if n < 1 or n > self.size:
            return None
        self.target = n

    def get_target(self):
        return self.target

    def get_out_neighbors(self, node):
        node -= 1 # convert from node number to array index
        if node < 0 or node >= self.size:
            return
        return [(i+1, self.adjacency_matrix[node][i]) for i in range(self.size) if self.adjacency_matrix[node][i] >= 0]

    def get_in_neighbors(self, node):
        node -= 1 # convert from node number to array index
        if node < 0 or node >= self.size:
            return
        return [(i+1, self.adjacency_matrix[i][node]) for i in range(self.size) if self.adjacency_matrix[i][node] >= 0]

    def set_max_flow(self, mf):
        self.max_flow = mf

    def get_max_flow(self):
        return self.max_flow

    @staticmethod
    def read_graph(file_name):
        with open(file_name, 'r') as f:
            try:
                num_vertices = int(f.readline())
                source = int(f.readline())
                target = int(f.readline())
                max_flow = int(f.readline())
            except:
                print("Bad file, check formatting\n")

            g = Graph(num_vertices)
            g.set_source(source)
            g.set_target(target)
            g.set_max_flow(max_flow)
            for line in f:
                try:
                    edge = [int(x) for x in line.split(" ")]
                except:
                    print("Bad file, check edge formatting\n")
                n1, n2, capacity = edge
                g.add_edge(n1, n2, capacity)
        return g

    def write_graph(self, file_name):
        # write graph using .dot file format, used for debugging graphs
        with open(file_name, 'w') as f:
            f.write("digraph G {\n")
            for i in range(self.size):
                for j in range(self.size):
                    if self.adjacency_matrix[i][j] > 0:
                        f.write('\t%i -> %i [label="%i"];\n' % (i+1, j+1, self.adjacency_matrix[i][j]))
            f.write('\t%i [label="source"];\n' % self.source)
            f.write('\t%i [label="target"];\n' % self.target)
            f.write("}")

