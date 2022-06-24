# Course: CS261 - Data Structures
# Author: Sam Cain
# Assignment: 6
# Description: Creates functionality for an undirected graph, including the ability to add/remove edges/nodes and
#   search through the graph in different ways.

class UndirectedGraph:
    """
    Class to implement undirected graph
    - duplicate edges not allowed
    - loops not allowed
    - no edge weights
    - vertex names are strings
    """

    def __init__(self, start_edges=None):
        """
        Store graph info as adjacency list
        DO NOT CHANGE THIS METHOD IN ANY WAY
        """
        self.adj_list = dict()

        # populate graph with initial vertices and edges (if provided)
        # before using, implement add_vertex() and add_edge() methods
        if start_edges is not None:
            for u, v in start_edges:
                self.add_edge(u, v)

    def __str__(self):
        """
        Return content of the graph in human-readable form
        DO NOT CHANGE THIS METHOD IN ANY WAY
        """
        out = [f'{v}: {self.adj_list[v]}' for v in self.adj_list]
        out = '\n  '.join(out)
        if len(out) < 70:
            out = out.replace('\n  ', ', ')
            return f'GRAPH: {{{out}}}'
        return f'GRAPH: {{\n  {out}}}'

    # ------------------------------------------------------------------ #

    """
    MY CODE STARTS HERE!
    """

    def add_vertex(self, v: str) -> None:
        """
        Add new vertex to the graph. Does nothing if the vertex already exists.
        """
        if v in self.adj_list:
            return

        self.adj_list[v] = []
        
    def add_edge(self, u: str, v: str) -> None:
        """
        Adds an edge between two vertices in the graph.
        """

        # Does nothing if the two vertices given are the same
        if u == v:
            return

        # If the vertices don't yet exist, we add them to the graph
        if u not in self.adj_list:
            self.add_vertex(u)
        if v not in self.adj_list:
            self.add_vertex(v)

        # If this edge already exists, does nothing
        if u in self.adj_list[v]:
            return

        self.adj_list[u].append(v)
        self.adj_list[v].append(u)

    def remove_edge(self, v: str, u: str) -> None:
        """
        Remove edge from the graph.
        """

        # If either vertex does not exist, does nothing
        if u not in self.adj_list:
            return
        if v not in self.adj_list:
            return

        # If the edge does not exist, does nothing
        if u not in self.adj_list[v]:
            return

        self.adj_list[u].remove(v)
        self.adj_list[v].remove(u)

    def remove_vertex(self, v: str) -> None:
        """
        Remove vertex and all connected edges
        """

        # If vertex doesn't exist, does nothing
        if v not in self.adj_list:
            return

        # Goes through every vertex and removes every connection to the soon-to-be-removed vertex
        for key in self.adj_list:
            if v in self.adj_list[key]:
                self.adj_list[key].remove(v)

        # Removing the vertex
        del self.adj_list[v]

    def get_vertices(self) -> []:
        """
        Return list of vertices in the graph (any order)
        """
        v_list = []

        for key in self.adj_list:
            v_list.append(key)

        return v_list

    def get_edges(self) -> []:
        """
        Return list of edges in the graph (any order)
        """
        e_list = []
        # Going through the whole graph and adding all edges to the list
        for key in self.adj_list:
            for el in self.adj_list[key]:
                if (el, key) not in e_list:
                    e_list.append((key, el))
        
        return e_list

    def is_valid_path(self, path: []) -> bool:
        """
        Return true if provided path is valid, False otherwise
        """
        counter = 1
        for vertex in path:

            # If any vertex doesn't exist, obviously not a valid path
            if vertex not in self.adj_list:
                return False

            # If we have reached the lat node, it is a valid path
            if counter == len(path):
                return True

            # If we can't move from one node to the next, it is not a valid path
            if path[counter] not in self.adj_list[vertex]:
                return False

            counter += 1

        return True

    def dfs(self, v_start, v_end=None) -> []:
        """
        Return list of vertices visited during DFS search
        Vertices are picked in alphabetical order
        """

        dfs_list = []
        dfs_stack = [v_start]

        # sort_list just gets added to the stack, it's  just here to get sorted for the alphabetical order
        sort_list = []

        # If start vertex isn't on the graph, return an empty list
        if v_start not in self.adj_list:
            return []

        while len(dfs_stack) > 0:
            # Removing from the end of the list (top of the stack for us)
            cur = dfs_stack.pop(len(dfs_stack) - 1)

            # Adding the vertex if it hasn't been added, and checking if we've reached our end-point
            if cur not in dfs_list:
                dfs_list.append(cur)
                if cur == v_end:
                    return dfs_list

            # Filling up the list to be sorted
            for vertex in self.adj_list[cur]:
                if vertex not in dfs_list:
                    sort_list.append(vertex)

            # Sorting the list then reversing it. I can probably do this with one function can't I?
            sort_list.sort()
            sort_list.reverse()

            # Adding sorted values to the stack
            for vertex in sort_list:
                dfs_stack.append(vertex)
            sort_list.clear()

        return dfs_list

    def bfs(self, v_start, v_end=None) -> []:
        """
        Return list of vertices visited during BFS search
        Vertices are picked in alphabetical order
        """

        bfs_list = []
        bfs_queue = [v_start]

        # Same function as dfs sorted list
        sort_list = []

        # If start vertex isn't on the graph, return an empty list
        if v_start not in self.adj_list:
            return []

        while len(bfs_queue) > 0:
            # Since we append from the end of the queue, we remove from the start
            cur = bfs_queue.pop(0)

            # Adding the vertex if it hasn't been added, and checking if we've reached our end-point
            if cur not in bfs_list:
                bfs_list.append(cur)
                if cur == v_end:
                    return bfs_list

                # Adding values to the sort list, then sorting them, then adding them to the queue
                for vertex in self.adj_list[cur]:
                    sort_list.append(vertex)
                sort_list.sort()
                for vertex in sort_list:
                    bfs_queue.append(vertex)
                sort_list.clear()

        return bfs_list

    def count_connected_components(self):
        """
        Return number of connected components in the graph
        """
        vertex_list = []
        result = 0

        # Creating a modifiable copy of self.adj_list
        for vertex in self.adj_list:
            vertex_list.append(vertex)

        while len(vertex_list) > 0:
            for vertex in vertex_list:

                # Creating a new list with all connected vertices using bfs, then removing those from our list of total
                #   number of vertices. The number of times we have to do this is the number of connected components.
                new_list = self.bfs(vertex)
                for el in new_list:
                    if el in vertex_list:
                        vertex_list.remove(el)
                if vertex in vertex_list:
                    vertex_list.remove(vertex)
                result += 1

        return result

    def has_cycle(self):
        """
        Return True if graph contains a cycle, False otherwise
        """

        vertex_list = []
        new_list = []
        banned_list = []

        # Creating a copy of self.adj_list
        for vertex in self.adj_list:
            vertex_list.append(vertex)

        # We go through and one by one remove all vertices that have 0 or one connection (since those can't help with a
        #   loop). If we have an empty list, there is no loop. If there are still nodes remaining after all nodes with 1
        #   or 0 connections have been removed, then they form a loop.
        while len(vertex_list) > 0:

            # new_list is used to check if we've gone through our whole list yet
            if len(new_list) >= len(vertex_list):
                return True

            # banned_list is subtracted from the number of connects, because the banned list contains vertices removed
            #   for not being part of a loop
            for vertex in vertex_list:
                score = len(self.adj_list[vertex])
                for el in banned_list:
                    if el in self.adj_list[vertex]:
                        score -= 1

                # Removing node if it is not part of the loop and clearing the new_list that checks for the loop
                if score <= 1:
                    vertex_list.remove(vertex)
                    banned_list.append(vertex)
                    new_list.clear()
                # Adding another value to the new_list, whose length will be checked above if we have a loop
                else:
                    new_list.append(vertex)

        return False

    """
    MY CODE ENDS HERE!
    """

if __name__ == '__main__':

    print("\nPDF - method add_vertex() / add_edge example 1")
    print("----------------------------------------------")
    g = UndirectedGraph()
    print(g)

    for v in 'ABCDE':
        g.add_vertex(v)
    print(g)

    g.add_vertex('A')
    print(g)

    for u, v in ['AB', 'AC', 'BC', 'BD', 'CD', 'CE', 'DE', ('B', 'C')]:
        g.add_edge(u, v)
    print(g)

    print("\nPDF - method remove_edge() / remove_vertex example 1")
    print("----------------------------------------------------")
    g = UndirectedGraph(['AB', 'AC', 'BC', 'BD', 'CD', 'CE', 'DE'])
    g.remove_vertex('DOES NOT EXIST')
    g.remove_edge('A', 'B')
    g.remove_edge('X', 'B')
    print(g)
    g.remove_vertex('D')
    print(g)

    print("\nPDF - method get_vertices() / get_edges() example 1")
    print("---------------------------------------------------")
    g = UndirectedGraph()
    print(g.get_edges(), g.get_vertices(), sep='\n')
    g = UndirectedGraph(['AB', 'AC', 'BC', 'BD', 'CD', 'CE'])
    print(g.get_edges(), g.get_vertices(), sep='\n')

    print("\nPDF - method is_valid_path() example 1")
    print("--------------------------------------")
    g = UndirectedGraph(['AB', 'AC', 'BC', 'BD', 'CD', 'CE', 'DE'])
    test_cases = ['ABC', 'ADE', 'ECABDCBE', 'ACDECB', '', 'D', 'Z']
    for path in test_cases:
        print(list(path), g.is_valid_path(list(path)))

    print("\nPDF - method dfs() and bfs() example 1")
    print("--------------------------------------")
    edges = ['AE', 'AC', 'BE', 'CE', 'CD', 'CB', 'BD', 'ED', 'BH', 'QG', 'FG']
    g = UndirectedGraph(edges)
    test_cases = 'ABCDEGH'
    for case in test_cases:
        print(f'{case} DFS:{g.dfs(case)} BFS:{g.bfs(case)}')
    print('-----')
    for i in range(1, len(test_cases)):
        v1, v2 = test_cases[i], test_cases[-1 - i]
        print(f'{v1}-{v2} DFS:{g.dfs(v1, v2)} BFS:{g.bfs(v1, v2)}')

    print("\nPDF - method count_connected_components() example 1")
    print("---------------------------------------------------")
    edges = ['AE', 'AC', 'BE', 'CE', 'CD', 'CB', 'BD', 'ED', 'BH', 'QG', 'FG']
    g = UndirectedGraph(edges)
    test_cases = (
        'add QH', 'remove FG', 'remove GQ', 'remove HQ',
        'remove AE', 'remove CA', 'remove EB', 'remove CE', 'remove DE',
        'remove BC', 'add EA', 'add EF', 'add GQ', 'add AC', 'add DQ',
        'add EG', 'add QH', 'remove CD', 'remove BD', 'remove QG')
    for case in test_cases:
        command, edge = case.split()
        u, v = edge
        g.add_edge(u, v) if command == 'add' else g.remove_edge(u, v)
        print(g.count_connected_components(), end=' ')
    print()

    print("\nPDF - method has_cycle() example 1")
    print("----------------------------------")
    edges = ['AE', 'AC', 'BE', 'CE', 'CD', 'CB', 'BD', 'ED', 'BH', 'QG', 'FG']
    g = UndirectedGraph(edges)
    test_cases = (
        'add QH', 'remove FG', 'remove GQ', 'remove HQ',
        'remove AE', 'remove CA', 'remove EB', 'remove CE', 'remove DE',
        'remove BC', 'add EA', 'add EF', 'add GQ', 'add AC', 'add DQ',
        'add EG', 'add QH', 'remove CD', 'remove BD', 'remove QG',
        'add FG', 'remove GE')
    for case in test_cases:
        command, edge = case.split()
        u, v = edge
        g.add_edge(u, v) if command == 'add' else g.remove_edge(u, v)
        print('{:<10}'.format(case), g.has_cycle())
