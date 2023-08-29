"""
This module provides a class for a Graph with path related methods
"""

from typing import Callable, Dict, List, Optional, Tuple

from networkx import Graph
from networkx.algorithms.shortest_paths import shortest_path_length


class PathGraph(Graph):
    """This class provides a number of path related methods"""

    def add_weighted_edges_from_map(self, edges: Dict[str, Dict[str, int]]) -> None:
        """Add weighted edges to self from a map"""

        for node1 in edges:
            for node2 in edges[node1]:
                self.add_edge(str(node1), str(node2),
                              weight=edges[node1][node2])

    def add_weighted_edges_for_complete(self, weight_function: Callable[[str, str], int]) -> None:
        """Add weighted edges to a graph, creating a complete graph"""

        nodes = list(self.nodes)
        for i, node in enumerate(nodes):
            for j in range(i+1, len(nodes)):
                self.add_edge(node, nodes[j],
                              weight=weight_function(node, nodes[j]))

    def get_length_of_path(self, path: List[str]) -> int:
        """Find the total length of a given path through the graph"""

        return sum(self.edges[path[i], path[i+1]]['weight'] for i in range(len(path)-1))

    def complete_hamiltonian_paths(self, start: Optional[str] = None,
                                   end: Optional[str] = None, cycle: bool = False
                                   ) -> List[Tuple[int, List[str]]]:
        """
        Find all complete Hamiltonian paths or cycles in this graph
        with optionally provided start and end nodes
        """

        if cycle and start is not None and end is not None and start != end:
            raise ValueError('A cycle must start and end at the same node')

        if start is not None and end is not None and start == end:
            cycle = True

        nodes = list(self.nodes)
        if start is not None:
            nodes.remove(start)
            start = [start]
        else:
            start = []

        if end is not None:
            if cycle:
                end = start
            else:
                nodes.remove(end)
                end = [end]
        else:
            if cycle:
                end = start
            else:
                end = []

        ret_val = []
        for perm in nodes:
            path = start + list(perm) + end
            length = self.get_length_of_path(path)
            ret_val.append((length, path))
        return ret_val

    def complete_travelling_salesman(self, start: Optional[str] = None,
                                     end: Optional[str] = None, max_: bool = False
                                     ) -> List[str]:
        """
        Find the shortest or longest complete Hamiltonian path in the graph
        with optionally provided start and end nodes
        """

        if max_:
            rv = max(self.complete_hamiltonian_paths(start, end))
        else:
            rv = min(self.complete_hamiltonian_paths(start, end))
        return rv[1]


class CompleteGraph(Graph):
    """
    Subclass of networkx.Graph providing additional features to create
    complete graphs
    """

    def fill_missing_edges(self):
        """
        Fill in any missing edges between nodes with the shortest path length
        to create a complete graph
        """
        for node_1 in self.nodes:
            shortest = shortest_path_length(self, source=node_1)
            for node_2 in self.nodes:
                if node_1 == node_2 or node_1 in self[node_2]:
                    continue
                self.add_edge(node_1, node_2, weight=shortest[node_2])
