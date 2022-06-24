# Course: CS261 - Data Structures
# Author: Sam Cain
# Assignment: 6
# Description: Creates functionality for a directed graph, including the ability to add edges/nodes, remove edges, and
#    search through the graph in different ways, including finding the shortest path to a node using dijkstra algorithm.


class DirectedGraph:
    """
    Class to implement directed weighted graph
    - duplicate edges not allowed
    - loops not allowed
    - only positive edge weights
    - vertex names are integers
    """

    def __init__(self, start_edges=None):
        """
        Store graph info as adjacency matrix
        DO NOT CHANGE THIS METHOD IN ANY WAY
        """
        self.v_count = 0
        self.adj_matrix = []

        # populate graph with initial vertices and edges (if provided)
        # before using, implement add_vertex() and add_edge() methods
        if start_edges is not None:
            v_count = 0
            for u, v, _ in start_edges:
                v_count = max(v_count, u, v)
            for _ in range(v_count + 1):
                self.add_vertex()
            for u, v, weight in start_edges:
                self.add_edge(u, v, weight)

    def __str__(self):
        """
        Return content of the graph in human-readable form
        DO NOT CHANGE THIS METHOD IN ANY WAY
        """
        if self.v_count == 0:
            return 'EMPTY GRAPH\n'
        out = '   |'
        out += ' '.join(['{:2}'.format(i) for i in range(self.v_count)]) + '\n'
        out += '-' * (self.v_count * 3 + 3) + '\n'
        for i in range(self.v_count):
            row = self.adj_matrix[i]
            out += '{:2} |'.format(i)
            out += ' '.join(['{:2}'.format(w) for w in row]) + '\n'
        out = f"GRAPH ({self.v_count} vertices):\n{out}"
        return out

    # ------------------------------------------------------------------ #

    """
    MY CODE STARTS HERE!
    """

    def add_vertex(self) -> int:
        """
        Adds a vertex to the graph
        """
        self.v_count += 1
        new_vertex = []

        # Have to make each list one longer to account for the new node
        for list in self.adj_matrix:
            list.append(0)

        for x in range(self.v_count):
            new_vertex.append(0)
        self.adj_matrix.append(new_vertex)
        return self.v_count

    def add_edge(self, src: int, dst: int, weight=1) -> None:
        """
        Adds an edge between two nodes after making sure the two nodes are valid and not the same.
        """
        if weight <= 0:
            return
        if src < 0 or src >= len(self.adj_matrix):
            return
        if dst < 0 or dst >= len(self.adj_matrix):
            return
        if dst == src:
            return

        self.adj_matrix[src][dst] = weight

    def remove_edge(self, src: int, dst: int) -> None:
        """
        Removes an edge from a graph after making sure the given vertices are valid.
        """
        if src < 0 or src >= len(self.adj_matrix):
            return
        if dst < 0 or dst >= len(self.adj_matrix):
            return

        self.adj_matrix[src][dst] = 0

    def get_vertices(self) -> []:
        """
        Returns a list of all the vertices in the graph.
        """
        vertex_list = []
        vertex = 0
        for x in range(self.v_count):
            vertex_list.append(vertex)
            vertex += 1

        return vertex_list

    def get_edges(self) -> []:
        """
        Returns a list of all the edges in the graph as a tuple (source, destination, weight)
        """
        source = 0
        edge_list = []

        # Since vertices are just in numerical order, a simple counter keeps track of source and destination
        for x in self.adj_matrix:
            destination = 0
            for weight in x:
                if weight != 0:
                    edge_list.append((source, destination, weight))
                destination += 1
            source += 1

        return edge_list

    def is_valid_path(self, path: []) -> bool:
        """
        Returns 'True' if you can traverse through a given list of vertices in order by traveling along edges. Returns
            'False' otherwise.
        """
        index = 1

        # Edge cases for short path lists
        if len(path) == 0:
            return True
        if len(path) == 1:
            if 0 <= path[0] < len(self.adj_matrix):
                return True
            else:
                return False

        # Checking if each vertex in 'path' has a weighted edge with the previous vertex (and that the vertex is valid)
        while index != len(path):
            if len(self.adj_matrix) <= path[index] < 0:
                return False
            if len(self.adj_matrix) <= path[index - 1] < 0:
                return False
            if self.adj_matrix[path[index - 1]][path[index]] == 0:
                return False
            index += 1

        return True

    def dfs(self, v_start, v_end=None) -> []:
        """
        Uses depth-first-search to return a list of all connected vertices from a source vertex.
        """
        def dfs_rec(stack, vertex, end=None):
            """
            Helper function for dfs. Decided to go recursive this time. Seemed easier.
            """

            # Check if we hit the end-vertex
            if vertex == end:
                return

            # Adding vertex to the stack if it hasn't already been added
            if vertex not in stack:
                stack.append(vertex)

            # Going through and recurring when we find an edge to a new vertex.
            counter = 0
            for x in self.adj_matrix[vertex]:
                if x != 0:
                    if counter not in stack:
                        stack.append(counter)
                        dfs_rec(stack, counter, end)
                counter += 1

        # Setting up and recalling the recursive function
        stack = []
        dfs_rec(stack, v_start, v_end)

        # I feel like I was supposed to use the stack to make a different list, but that didn't work and this did, so
        #   please don't be mad. Probably a slightly faster way to do this.
        return stack

    def bfs(self, v_start, v_end=None) -> []:
        """
        Uses depth-first-search to return a list of all connected vertices from a source vertex.
        """

        def bfs_rec(queue, list, end=None):
            """
            Helper function for 'bfs'.
            """

            # Stop everything if the queue is empty
            if len(queue) <= 0:
                return

            vertex = queue.pop(0)

            # Checking if we've reached the end point
            if vertex == end:
                return

            # Adding vertex to the list if it isn't there yet
            if vertex not in list:
                list.append(vertex)

            # Making a list of all connected vertices, adding them to a queue, then recurring
            counter = 0
            sort_list = []
            for x in self.adj_matrix[vertex]:
                if x != 0:
                    if counter not in list:
                        sort_list.append(counter)
                counter += 1
            sort_list.sort()
            for el in sort_list:
                queue.append(el)
            bfs_rec(queue, list, end)

        # Returning a blank list if we have an invalid v_start
        if v_start < 0 or v_start >= len(self.adj_matrix):
            return []

        # Setting up and recalling the recursive function
        queue = [v_start]
        list = []
        bfs_rec(queue, list, v_end)

        return list

    def has_cycle(self):
        """
        Checking if the graph contains a cycle, then returns 'True' if it does, and 'False' if it does not.
        """

        # Making my own deep-copy of our graph list ('self.adj_matrix')
        list_copy = []
        counter = 0
        for x in self.adj_matrix:
            list_copy.append([])
            for y in x:
                list_copy[counter].append(y)
            counter += 1

        # Going through and removing all vertices with only one or zero connections from the copy. If values still,
        #   then they are part of a cycle. If none remain, then the graph has no cycle.
        counter = 0
        while len(list_copy) > 0:

            # Checking if we've reached the end of the list without removing anything
            if counter == len(list_copy):
                return True

            # Counting the number of connections
            connections = 0
            for y in list_copy[counter]:
                if y != 0:
                    connections += 1

            # If there are not enough connections, remove the vertex and it's edge-weight value from all lists
            if connections < 1:
                list_copy.pop(counter)
                for x in list_copy:
                    x.pop(counter)

                # We start from the beginning after a removal to re-check all vertices
                counter = 0
            else:
                counter += 1
        return False

    def dijkstra(self, src: int) -> []:
        """
        Returns a list of all the shortest weights to get to each vertex from a source.
        """
        visited = []

        # Filling all values with 'inf' in case the vertices can't be reached
        for x in range(self.v_count):
            visited.append(float('inf'))
        priority_queue = [(src, 0)]

        # Using dijkstra's formula to add up the shortest distances from the source
        while len(priority_queue) != 0:
            v = priority_queue.pop(0)

            # Was having some trouble with higher weights overwriting, but this inequality statement wasn't in the
            #   pseudocode, so I hope  its not cheating
            if visited[v[0]] == float('inf') or visited[v[0]] > v[1]:
                visited[v[0]] = v[1]
                index = 0
                for el in self.adj_matrix[v[0]]:
                    if el != 0:
                        priority_queue.append((index, el + v[1]))
                    index += 1

        return visited


    """
    MY CODE ENDS HERE!
    """


if __name__ == '__main__':

    print("\nPDF - method add_vertex() / add_edge example 1")
    print("----------------------------------------------")
    g = DirectedGraph()
    print(g)
    for _ in range(5):
        g.add_vertex()
    print(g)

    edges = [(0, 1, 10), (4, 0, 12), (1, 4, 15), (4, 3, 3),
             (3, 1, 5), (2, 1, 23), (3, 2, 7)]
    for src, dst, weight in edges:
        g.add_edge(src, dst, weight)
    print(g)

    print("\nPDF - method get_edges() example 1")
    print("----------------------------------")
    g = DirectedGraph()
    print(g.get_edges(), g.get_vertices(), sep='\n')
    edges = [(0, 1, 10), (4, 0, 12), (1, 4, 15), (4, 3, 3),
             (3, 1, 5), (2, 1, 23), (3, 2, 7)]
    g = DirectedGraph(edges)
    print(g.get_edges(), g.get_vertices(), sep='\n')

    print("\nPDF - method is_valid_path() example 1")
    print("--------------------------------------")
    edges = [(0, 1, 10), (4, 0, 12), (1, 4, 15), (4, 3, 3),
             (3, 1, 5), (2, 1, 23), (3, 2, 7)]
    g = DirectedGraph(edges)
    test_cases = [[0, 1, 4, 3], [1, 3, 2, 1], [0, 4], [4, 0], [], [2]]
    for path in test_cases:
        print(path, g.is_valid_path(path))

    print("\nPDF - method dfs() and bfs() example 1")
    print("--------------------------------------")
    edges = [(0, 1, 10), (4, 0, 12), (1, 4, 15), (4, 3, 3),
             (3, 1, 5), (2, 1, 23), (3, 2, 7)]
    g = DirectedGraph(edges)
    for start in range(5):
        print(f'{start} DFS:{g.dfs(start)} BFS:{g.bfs(start)}')

    print("\nPDF - method has_cycle() example 1")
    print("----------------------------------")
    edges = [(0, 1, 10), (4, 0, 12), (1, 4, 15), (4, 3, 3),
             (3, 1, 5), (2, 1, 23), (3, 2, 7)]
    g = DirectedGraph(edges)

    edges_to_remove = [(3, 1), (4, 0), (3, 2)]
    for src, dst in edges_to_remove:
        g.remove_edge(src, dst)
        print(g.get_edges(), g.has_cycle(), sep='\n')

    edges_to_add = [(4, 3), (2, 3), (1, 3), (4, 0)]
    for src, dst in edges_to_add:
        g.add_edge(src, dst)
        print(g.get_edges(), g.has_cycle(), sep='\n')
    print('\n', g)

    print("\nPDF - dijkstra() example 1")
    print("--------------------------")
    edges = [(0, 1, 10), (4, 0, 12), (1, 4, 15), (4, 3, 3),
             (3, 1, 5), (2, 1, 23), (3, 2, 7)]
    g = DirectedGraph(edges)
    for i in range(5):
        print(f'DIJKSTRA {i} {g.dijkstra(i)}')
    g.remove_edge(4, 3)
    print('\n', g)
    for i in range(5):
        print(f'DIJKSTRA {i} {g.dijkstra(i)}')
