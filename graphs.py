
from networkx import Graph
from typing import List,Any,Dict,Callable
from itertools import permutations

class PathGraph(Graph):

    def add_weighted_edges_from_map(self,edges:Dict[str,Dict[str,int]]) -> None:
        for node1 in edges:
            for node2 in edges[node1]:
                self.add_edge(str(node1),str(node2), weight=edges[node1][node2])

    def add_weighted_edges_for_complete(self,weight_function:Callable[[str,str],int]) -> None:
        nodes = list(self.nodes)
        for i in range(len(nodes)):
            for j in range(i+1, len(nodes)):
                self.add_edge(nodes[i],nodes[j],weight=weight_function(nodes[i],nodes[j]))
                
    def get_length_of_path(self,path:List[str]) -> int:
        return sum([self.edges[path[i],path[i+1]]['weight'] for i in range(len(path)-1)])

    def complete_hamiltonian_paths(self,start=None,end=None,cycle=False):
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

        return [(self.get_length_of_path(start + list(perm) + end), start + list(perm) + end) for perm in permutations(nodes)]

    def complete_travelling_salesman(self,start=None,end=None,max_=False):
        if max_:
            rv = max(self.complete_hamiltonian_paths(start,end))
        else:
            rv = min(self.complete_hamiltonian_paths(start,end))
        return rv[1]


G = PathGraph()
